import pytest

from poetry_plugin_hook.redirect import BufferedIO, buffered_io


@pytest.fixture
def command():
    class Base:
        _io = BufferedIO()

    class Child(Base):
        base = Base()

    return Child()


def test_buffer_raises():
    with pytest.raises(ValueError):
        with buffered_io(None):
            pass  # pragma: no cover


def test_buffer(command):

    with buffered_io(command) as io:
        assert isinstance(io, BufferedIO)


def test_buffers(command):

    with buffered_io(command, command.base) as io:
        assert isinstance(io, BufferedIO)
