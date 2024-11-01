from unittest.mock import MagicMock

import pytest
from cleo.io.buffered_io import BufferedIO


@pytest.fixture
def mock_latest_io(mocker):
    """Mock latest fixture"""

    def wrapped(output: str):
        """Mock the ShowCommand class from poetry."""

        mock_io = MagicMock(spec=BufferedIO)
        mock_io.fetch_output.return_value = output

        mock_context = MagicMock(return_value=mock_io)
        mock_context.__enter__.return_value = mock_io

        mocker.patch("poetry_plugin_hook.latest.buffered_io", return_value=mock_context)
        mocker.patch("poetry_plugin_hook.latest.ShowCommand.handle", return_value=None)

        return mock_context

    return wrapped


def test_latest_mocked(poetry, mock_latest_io):
    pass
