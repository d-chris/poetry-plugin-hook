import contextlib
import re
from typing import Generator

import cleo.io.io
import cleo.io.outputs.output
from poetry.console.commands.show import ShowCommand
from poetry.plugins.application_plugin import ApplicationPlugin


class Output(cleo.io.outputs.output.Output):

    @classmethod
    def from_output(cls, output: cleo.io.outputs.output.Output) -> "Output":
        instance = cls(
            verbosity=output.verbosity,
            decorated=output.is_decorated(),
            formatter=output.formatter,
        )

        return instance

    def _write(self, message: str, new_line: bool = False) -> None:
        if new_line:
            message += "\n"

        try:
            self._stdout.append(message)
        except AttributeError:
            self._stdout = [message]

    def stdout(self) -> str:
        return "".join(self._stdout)


class IO(cleo.io.io.IO):

    @classmethod
    def from_io(cls, io: cleo.io.io.IO) -> "IO":
        output = Output.from_output(io.output)

        instance = cls(
            input=io.input,
            output=output,
            error_output=io.error_output,
        )

        return instance


class LatestCommand(ShowCommand):
    name = "latest"
    description = "Check if all top-level dependencies are up-to-date"

    _regex = re.compile(
        r"^(?P<package>\S+)\s+(?P<current>\S+)\s+(?P<latest>\S+)\s+(?P<comment>.*?)$",
        re.MULTILINE,
    )

    _true_options = ["latest", "outdated", "top-level"]

    def configure(self) -> None:
        """
        Modifiy all options from `poetry show` to fit the `poetry latest` command.

        Returns:
            None
        """

        remove_options = ["no-dev", "tree", "all", "why"]
        self.options = [opt for opt in self.options if opt.name not in remove_options]

        for opt in filter(lambda o: o.name in self._true_options, self.options):
            opt._description += " <warning>(option is always True)</warning>"

        super().configure()

    @contextlib.contextmanager
    def redirect_output(self) -> Generator[Output, None, None]:
        """
        Redirects output to a custom Output object.
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
