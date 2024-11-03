import re

from poetry.console.commands.show import ShowCommand

from poetry_plugin_hook.redirect import buffered_io, strip_ansi


class LatestCommand(ShowCommand):
    name = "hook latest"
    description = "Check if all top-level dependencies are up-to-date."
    help = """\
To check if all top-level dependencies of your package are up-to-date
    <info>poetry hook latest --only=main</>

If a specific package is outdated
    <info>poetry hook latest <package></>
"""

    _version = (
        r"([1-9][0-9]*!)?"
        r"(0|[1-9][0-9]*)"
        r"(\.(0|[1-9][0-9]*))*"
        r"((a|b|rc)(0|[1-9][0-9]*))?"
        r"(\.post(0|[1-9][0-9]*))?"
        r"(\.dev(0|[1-9][0-9]*))?"
    )
    """PEP 440 version regex."""

    _dependencies = re.compile(
        r"^(?P<package>.*?)\s+"
        rf"(?P<current>{_version})\s+"
        rf"(?P<latest>{_version})\s+"
        r"(?P<description>.*?)$",
        re.MULTILINE,
    )

    _true_options = ["latest", "outdated", "top-level"]
    _del_options = ["no-dev", "tree", "all", "why"]

    def configure(self) -> None:
        """
        Modifiy all options from `poetry show -o -T` to fit the `poetry hook latest`
        command.
        """

        self.options = [
            option for option in self.options if option.name not in self._del_options
        ]

        for opt in filter(lambda o: o.name in self._true_options, self.options):
            opt._description += " <warning>(option is always True)</warning>"

        super().configure()

    def handle(self) -> int:
        """
        Executes `poetry show -o -T` to check for outdated dependencies.

        Returns:
            int: Non-zero if there are outdated dependencies, zero otherwise.
        """

        # force options to True, `poetry show -o -T`
        for option in self._true_options:
            self.io.input.set_option(option, True)

        # check for certain package if specified
        package = self.io.input.argument("package")
        if package:
            self.io.input.set_argument("package", None)

        # redirect output to check for outdated dependencies
        with buffered_io(self) as io:
            super().handle()
            stdout = io.fetch_output()
            stderr = io.fetch_error()

        if stdout.strip() or stderr.strip():
            self.line(stdout)
            self.line_error(stderr)

        stdout = strip_ansi(stdout)

        if package is not None:
            return self._handle_package(package, stdout)

        return self._handle_outdated(stdout)

    def _handle_outdated(self, stdout: str) -> int:
        """
        Handles the output of the `poetry show -o -T` command to check for outdated
        dependencies.

        Prints a message if all top-level dependencies are up-to-date.

        Args:
            stdout (str): The standard output from the `poetry show -o -T` command.

        Returns:
            int: The number of outdated dependencies.
        """
        outdated = len(self._dependencies.findall(stdout))

        if outdated == 0:
            self.line("All top-level dependencies are up-to-date.", style="info")

        return outdated

    def _handle_package(self, package: str, stdout: str) -> int:
        """
        Handles the output of the `poetry show -o -T` command to check for the given
        package.

        Prints a message if the top-level package is not found in the output.

        Args:
            package (str): The name of the package to check.
            stdout (str): The standard output from the `poetry show -o -T` command.
        Returns:
            int: Returns 1 if the package is outdated otherwise returns 0.
        """

        _dependency = re.compile(
            re.escape(package),
        )

        for match in self._dependencies.finditer(stdout):
            _package = match.group("package").split()[0]
            if _dependency.fullmatch(_package):
                return 1

        self.line(f"Top-level {package=} is up-to-date.", style="info")
        return 0
