import json
import warnings


def test_poetry_json(poetry, tmp_path):
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

    with warnings.catch_warnings(record=True):
        for cmd in commands:

            command = cmd.split()[1:] + [
                "--no-ansi",
                "-C",
                str(tmp_path),
            ]

            process = poetry(*command)

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

        with open("poetry.json", "w") as f:
            json.dump(log, f, indent=4)
