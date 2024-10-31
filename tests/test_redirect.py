import pytest

from poetry_plugin_hook.redirect import buffered_io


def test_buffer_raises():
    with pytest.raises(ValueError):
        with buffered_io(None):
            pass
