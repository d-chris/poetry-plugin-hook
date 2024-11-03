import subprocess


def indent(text: str, spaces: int = 2) -> str:
    """
    Indent each line of a text by the given number of spaces.

    Args:
        text (str): The text to indent.
        spaces (int): The number of spaces to indent by.

    Returns:
        str: The indented text.
    """
    prefix = " " * spaces

    return "\n".join(
        prefix + line.rstrip() if line.strip() else "" for line in text.splitlines()
    )


def shell(cmd: str) -> str:
    """
    Run a shell command and return its output.

    Args:
        cmd (str): The shell command to run.

    Returns:
        str: The output of the shell command.
    """
    process = subprocess.run(
        cmd,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
    )

    return f"$ {cmd}\n\n{indent(process.stdout.strip())}"


def main():
    """
    Render the README.md file using the README.md.jinja2 template.

    Requires following PyPi packages:
    - 'jinja2'
    - 'pathlibutil'

    Returns non-zero on failure.
    """

    try:
        from jinja2 import Environment
        from pathlibutil import Path

        with Path(__file__).parent as cwd:
            template = cwd / "README.md.jinja2"
            readme = (cwd / "../README.md").resolve()

        with template.open("r") as file:
            env = Environment(
                keep_trailing_newline=True,
            )
            env.filters["include"] = lambda f: Path(f).read_text().strip()
            env.filters["shell"] = shell

            template = env.from_string(file.read())

        with readme.open("w") as file:
            file.write(template.render())

    except Exception as e:
        print(f"{readme=} creation failed!\n\t{e}")
        return 1

    print(f"{readme=} created successfully!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
