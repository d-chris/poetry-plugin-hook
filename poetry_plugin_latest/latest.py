import contextlib
import re
from typing import Generator

from poetry.console.commands.show import ShowCommand
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_plugin_latest.wrapper import IO, Output


class LatestCommand(ShowCommand):
    name = "latest"
    description = "Check if all top-level dependencies are up-to-date."

    _regex = re.compile(
        r"^(?P<package>\S+)\s+(?P<current>\S+)\s+(?P<latest>\S+)\s+(?P<comment>.*?)$",
        re.MULTILINE,
    )

    _true_options = ["latest", "outdated", "top-level"]
    _del_options = ["no-dev", "tree", "all", "why"]

    def configure(self) -> None:
        """
        Modifiy all options from `poetry show` to fit the `poetry latest` command.

        Returns:
            None
        """

        self.options = [
            option for option in self.options if option.name not in self._del_options
        ]

        for opt in filter(lambda o: o.name in self._true_options, self.options):
            opt._description += " <warning>(option is always True)</warning>"

        super().configure()

    @contextlib.contextmanager
    def redirect_output(self) -> Generator[Output, None, None]:
        """
        Redirects output to a custom Output object.

        Yields:
            Output: The custom Output object to which the output is redirected.
        """

        try:
            io = self.io

            self._io = IO.from_io(io)

            yield self._io.output
        finally:
            self._io = io

    def handle(self) -> int:
        """
        Executes `poetry show -o -T` to check for outdated dependencies.

        Catches stdout to check for dependencies and returns non-zero.

        Returns:
            int: Non-zero if there are outdated dependencies, zero otherwise.
        """

        # force options to True, `poetry show -o -T`
        for option in self._true_options:
            self.io.input.set_option(option, True)

        with self.redirect_output() as redirect:
            super().handle()
            text = redirect.stdout()

        outdated = len(self._regex.findall(text))

        if outdated == 0:
            self.line("All top-level dependencies are up-to-date.")
        else:
            self.line(text)

        return outdated


def factory():
    return LatestCommand()


class LatestPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("latest", factory)
