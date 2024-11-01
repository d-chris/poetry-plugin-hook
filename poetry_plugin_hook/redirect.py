import contextlib
import re
from abc import ABC, abstractmethod
from typing import Generator, List

from cleo.io.buffered_io import BufferedIO
from cleo.io.io import IO


class CommandCleo(ABC):  # pragma: no cover
    @property
    @abstractmethod
    def _io(self) -> IO:
        pass


def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape sequences from a string.

    Args:
        text (str): The string to remove ANSI escape sequences from.

    Returns:
        str: The string without ANSI escape sequences.
    """
    return re.sub(r"\x1B[@-_][0-?]*[ -/]*[@-~]", "", text)


@contextlib.contextmanager
def buffered_io(
    *args: CommandCleo,
    **kwargs,
) -> Generator[BufferedIO, None, None]:
    """
    Context manager that temporarily replaces the I/O of multiple Poetry commands with
    the same buffered I/O to capture their output.

    Args:
        *cmds (List[CommandCleo]): The Poetry commands whose I/O will be captured.
        **kwargs: Additional keyword arguments to pass to the BufferedIO constructor.

    Yields:
        BufferedIO: The buffered I/O object.

    Raises:
        ValueError: If any of the commands does not have an I/O attribute.

    Example:
        ```python
        with buffered_ios(cmd1, cmd2, decorated=False) as io:
            # Perform operations with the buffered I/O
            output = io.fetch_output()
        ```
    """

    # perform check if all commands have a `_io` attribute
    original: List[IO] = []

    for cmd in args:
        if not hasattr(cmd, "_io"):
            raise ValueError(f"Command {cmd} does not have an I/O attribute.")

        original.append(cmd._io)

    # create a new buffered I/O object
    io = BufferedIO(
        input=kwargs.pop("input", original[0].input),
        decorated=kwargs.pop("decorated", original[0].output.is_decorated()),
        **kwargs,
    )

    try:
        # assign the buffered I/O object to all commands
        for cmd in args:
            cmd._io = io

        yield io
    finally:
        # restore the original I/O objects
        for cmd, original_io in zip(args, original):
            cmd._io = original_io
