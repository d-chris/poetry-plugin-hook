import contextlib
import re
from typing import Generator

import cleo.io.buffered_io as cleo
import poetry.console.commands.command as poetry


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
    cmd: poetry.Command,
    **kwargs,
) -> Generator[cleo.BufferedIO, None, None]:
    """
    Context manager that temporarily replaces the I/O of a Poetry command with
    a buffered I/O to capture it's output.

    Args:
        cmd (poetry.Command): The Poetry command whose I/O will be captured.
        **kwargs: Additional keyword arguments to pass to the BufferedIO constructor.

    Yields:
        cleo.BufferedIO: The buffered I/O object.

    Example:
        ```python
        # get ansi output from a command
        with buffered_io(cmd, decorated=False) as io:
            # Perform operations with the buffered I/O
            output = io.fetch_output()
        ```
    """
    try:
        original = cmd.io

        cmd._io = cleo.BufferedIO(
            input=kwargs.pop(
                "input",
                original.input,
            ),
            decorated=kwargs.pop(
                "decorated",
                original.output.is_decorated(),
            ),
            **kwargs,
        )

        yield cmd.io
    finally:
        cmd._io = original
