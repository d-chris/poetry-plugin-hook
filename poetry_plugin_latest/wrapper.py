import cleo.io.io
import cleo.io.outputs.output


class Output(cleo.io.outputs.output.Output):
    """
    Output class that redirect all messages to a List[str].
    """

    @classmethod
    def from_output(cls, output: cleo.io.outputs.output.Output) -> "Output":
        """
        Wrap an existing Output object.
        """
        return cls(
            verbosity=output.verbosity,
            decorated=output.is_decorated(),
            formatter=output.formatter,
        )

    def _write(self, message: str, new_line: bool = False) -> None:
        """
        Pipe all messeges to a List[str]
        """
        if new_line:
            message += "\n"

        try:
            self._stdout.append(message)
        except AttributeError:
            self._stdout = [message]

    def stdout(self) -> str:
        """
        Returns all messages as a string.
        """
        try:
            return "".join(self._stdout)
        except AttributeError:
            return ""


class IO(cleo.io.io.IO):
    """
    IO class that replaces the Output object to redirect messages to a List[str].
    """

    @classmethod
    def from_io(cls, io: cleo.io.io.IO) -> "IO":
        """
        Wrap an existing IO object and replace the Output object to redirect messages.
        """
        output = Output.from_output(io.output)

        return cls(
            input=io.input,
            output=output,
            error_output=io.error_output,
        )
