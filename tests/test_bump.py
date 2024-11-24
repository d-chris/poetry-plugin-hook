import os
from typing import Callable
from unittest.mock import PropertyMock

import pytest
from cleo.io.buffered_io import BufferedIO

from poetry_plugin_hook.bump import BumpCommand


@pytest.fixture
def mock_version(mocker) -> Callable[[int], int]:
    """Mock version fixture"""

    def wrapped(
        return_value: int = 0,
    ):
        """Mock the VersionCommand class from poetry."""

        mocker.patch(
            "poetry_plugin_hook.bump.VersionCommand.handle",
            return_value=return_value,
        )

        mocker.patch(
            "poetry_plugin_hook.bump.Path.write_text",
            return_value=0,
        )

        return return_value

    return wrapped


@pytest.fixture
def mock_poetry(mocker, tmp_path):

    def wrapped(version: str = None):

        toml = tmp_path / "pyproject.toml"

        with toml.open("w") as f:
            f.write("[tool.poetry]\nname = 'package'\nversion = '0.0.0'\n")

        package = tmp_path / "package"
        package.mkdir()

        init = package / "__init__.py"
        init.touch()

        if version:
            with init.open("w") as f:
                f.write(f"__version__ = '{version}'\n")
        else:
            version = "0.0.0"

        mocker.patch(
            "poetry_plugin_hook.bump.BumpCommand.root_dir",
            new_callable=PropertyMock,
            return_value=tmp_path,
        )
        mocker.patch(
            "poetry_plugin_hook.bump.BumpCommand.package",
            new_callable=PropertyMock,
            return_value=package,
        )

        mocker.patch(
            "poetry_plugin_hook.bump.BumpCommand.version",
            new_callable=PropertyMock,
            return_value=version,
        )

        return tmp_path

    return wrapped


@pytest.fixture
def command(mock_poetry, mock_version):

    def wrapped(version: str = None):

        mock_version(0)
        mock_poetry(version)

        cmd = BumpCommand()
        cmd._io = BufferedIO()

        return cmd

    return wrapped


@pytest.mark.parametrize(
    "returncode",
    [
        0,
        123,
    ],
)
def test_bump_version(poetry, mock_version, returncode):

    mock_version(return_value=returncode)

    process = poetry(
        "hook bump",
        "0.0.0",
        "--file=__init__.py",
        "--file=__version__.py",
        "--dry-run",
        "-v",
    )

    assert process.returncode == returncode


@pytest.mark.parametrize(
    "file",
    [
        "__init__.py",
        "package/__init__.py",
        "pyproject.toml",
    ],
)
def test_bump_resolve(command, file):

    cmd = command()

    assert cmd.resolve(file).is_file()


def test_bump_resolve_raises(command):

    cmd = command()

    with pytest.raises(FileNotFoundError):
        cmd.resolve("non_existent_file.py")


@pytest.mark.parametrize(
    "file, expected",
    [
        ("__init__.py", 0),
        ("pyproject.toml", 1),
    ],
)
def test_bump_substitute(command, file, expected, tmp_path):

    cmd = command("0.0.0")
    try:
        cwd = os.getcwd()
        os.chdir(tmp_path)

        file = cmd.resolve(file)
        result = cmd.substitute(file, "0.0.0")
    finally:
        os.chdir(cwd)

    assert result == expected
