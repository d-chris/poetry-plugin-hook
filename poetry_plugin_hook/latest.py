import re

from poetry.console.commands.show import ShowCommand

from poetry_plugin_hook.redirect import buffered_io, strip_ansi


class LatestCommand(ShowCommand):
    name = "hook latest"
    description = "Check if all top-level dependencies are up-to-date."
    help = "poetry hook latest [options]"

    _dependencies = re.compile(
        r"^(?P<package>.*?)\s+"
        r"(?P<current>\d\.\d\.\d\S*)\s+"
        r"(?P<latest>\d\.\d\.\d\S*)\s+"
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

        # redirect output to check for outdated dependencies
        with buffered_io(self) as io:
            super().handle()
            stdout = io.fetch_output()
            stderr = io.fetch_error()

        if stdout.strip() or stderr.strip():
            self.line(stdout)
            self.line_error(stderr)

        # count outdated dependencies
        outdated = len(
            self._dependencies.findall(
                strip_ansi(stdout),
            )
        )

        if outdated == 0:
            self.line("All top-level dependencies are up-to-date.", style="info")

        return outdated
