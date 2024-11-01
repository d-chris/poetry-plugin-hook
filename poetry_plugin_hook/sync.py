import re

from cleo.exceptions import CleoLogicError
from cleo.helpers import option
from poetry.console.commands.install import InstallCommand

from poetry_plugin_hook.redirect import buffered_io, strip_ansi


class SyncCommand(InstallCommand):
    name = "hook sync"
    description = (
        "Synchronize the environment with the locked packages and the specified groups."
    )
    help = ""

    _true_options = ["sync"]
    _del_options = ["no-dev", "remove-untracked", "compile"]
    _exit_codes = ["any", "installs", "updates", "removals"]

    _operations = re.compile(
        r"^Package operations: "
        r"(?P<installs>\d+)\D+"
        r"(?P<updates>\d+)\D+"
        r"(?P<removals>\d+)\D+"
        r"(?:(?P<skipped>\d+)\D+)?$",
        re.MULTILINE,
    )

    def configure(self) -> None:

        self.options = [
            option(
                "exit",
                description=(
                    "Specify the value to return as exitcode. "
                    f"<info>choices={str(self._exit_codes)}</info>"
                ),
                flag=False,
                default="any",
            )
        ] + [option for option in self.options if option.name not in self._del_options]

        for opt in filter(lambda o: o.name in self._true_options, self.options):
            opt._description += " <warning>(option is always True)</warning>"

        super().configure()

    def handle(self) -> int:

        # check if the exit option is valid
        exit = self.io.input.option("exit")
        if exit not in self._exit_codes:
            raise CleoLogicError(f"Invalid option: {exit=}")

        # force options to `poetry install --sync`
        for opt in self._true_options:
            self.io.input.set_option(opt, True)

        with buffered_io(
            self.installer.executor,
            self.installer,
            self,
        ) as io:
            super().handle()
            stdout = io.fetch_output()
            stderr = io.fetch_error()

        match = self._operations.search(strip_ansi(stdout))

        # retrive the exit code
        try:
            result = int(match.group(exit))
        except AttributeError:
            self.line("No dependencies to syncronize.", style="info")
            return 0
        except IndexError:
            pass

        if stdout.strip() or stderr.strip():
            self.line(stdout)
            self.line_error(stderr)

        result = 0

        for code in self._exit_codes:
            try:
                result += int(match.group(code))
            except IndexError:
                pass

        return result