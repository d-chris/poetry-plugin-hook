import json
import subprocess
import warnings
from pathlib import Path
from tempfile import TemporaryDirectory

from cleo.io.buffered_io import BufferedOutput
from cleo.io.inputs.argv_input import ArgvInput
from poetry.console.application import Application


def application(*args: str) -> subprocess.CompletedProcess:
    """Run the poetry application with the given arguments."""

    args = [__file__] + [a for a in args if a.casefold() != "poetry"]

    input = ArgvInput(args)
    stdout = BufferedOutput()
    stderr = BufferedOutput()

    try:
        result = Application().run(
            input=input,
            output=stdout,
            error_output=stderr,
        )
    except SystemExit as e:
        result = e.code

    return subprocess.CompletedProcess(
        args=args,
        returncode=result,
        stdout=stdout.fetch(),
        stderr=stderr.fetch(),
    )


def load_mocks(hook):

    file = Path(__file__).with_name("mock_hooks.json")

    try:
        file.resolve(strict=True)
    except FileNotFoundError:
        save_mocks(file)

    with file.open() as f:
        data = json.load(f)

    return [d for d in data if hook in d["args"]]


def save_mocks(filename):

    commands = [
        "poetry --version",
        "poetry init -n",
        "poetry install --no-root",
        "poetry add pre-commit=4.0.0 --lock",
        "poetry hook sync --exit=installs --no-root --dry-run",
        "poetry hook sync --exit=removals --no-root --dry-run",
        "poetry hook sync --exit=updates --no-root --dry-run",
        "poetry hook sync --no-root --dry-run",
        "poetry hook latest",
        "poetry remove pre-commit",
        "poetry env remove --all",
    ]

    log = []

    with warnings.catch_warnings(record=True), TemporaryDirectory() as tmp_path:
        for cmd in commands:

            command = cmd.split()[1:] + [
                "--no-ansi",
                "-C",
                str(tmp_path),
            ]

            process = application(*command)

            if command[0] == "hook":
                log.append(
                    {
                        "args": command[:-3],
                        "returncode": process.returncode,
                        "stdout": process.stdout.split("\n"),
                        "stderr": process.stderr.split("\n"),
                    }
                )

            print(" ".join(["poetry"] + command[:-2]))
            print(process.stdout)
            print(process.stderr)

        with Path(filename).open("w") as f:
            json.dump(log, f, indent=4)
