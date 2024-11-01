import re
from unittest.mock import MagicMock

import pytest
from cleo.io.buffered_io import BufferedIO

from . import load_mocks


@pytest.fixture
def mock_sync_io(mocker):
    """Mock latest fixture"""

    def wrapped(
        stdout: str = "",
        stderr: str = "",
        **kwargs,
    ):
        """Mock the InstallCommand class from poetry."""

        mock_io = MagicMock(spec=BufferedIO)
        mock_io.fetch_output.return_value = stdout
        mock_io.fetch_error.return_value = stderr

        mock_context = MagicMock(return_value=mock_io)
        mock_context.__enter__.return_value = mock_io

        mocker.patch("poetry_plugin_hook.sync.buffered_io", return_value=mock_context)
        mocker.patch("poetry_plugin_hook.sync.InstallCommand.handle", return_value=None)

        return mock_context

    return wrapped


def test_exit_invalid(poetry):
    """Test if the exit option is invalid."""

    process = poetry(
        "hook",
        "sync",
        "--exit",
        "unknown",
    )

    assert re.search(r"Invalid option: exit='(?P<exit>.*?)'", process.stderr)
    assert process.returncode == 1


@pytest.mark.parametrize(
    "mock",
    load_mocks("sync"),
    ids=lambda m: " ".join(m["args"]),
)
def test_sync_mocked(poetry, mock_sync_io, mock):
    mock_sync_io(
        "\n".join(mock["stdout"]),
        "\n".join(mock["stderr"]),
    )

    process = poetry(*mock["args"])

    assert process.returncode == mock["returncode"]
