import os
import re
from pathlib import Path
from typing import Any

from cleo.helpers import option
from poetry.console.commands.version import VersionCommand


class PathNotFoundError(FileNotFoundError):
    def __init__(self, path: os.PathLike):
        errno = 2
        super().__init__(
            errno,
            os.strerror(errno),
            str(path),
        )


class BumpCommand(VersionCommand):
    name = "hook bump"
    description = "Update the version in pyproject.toml and synchronize it into files."
    help = """\
Update the version from package and also bumps __version__ strings in any given file.

    <info>poetry hook bump --next-phase patch --file __init__.py</>

The new version should ideally be a valid semver string or a valid bump rule:
patch, minor, major, prepatch, preminor, premajor, prerelease.

If no next-phase or version is provied the version from the pyproject.toml file will be
synced into the files.
"""

    _regex = re.compile(
        r"(?P<prefix>__version__\s*=\s*)(?P<quote>['\"])(?P<version>[^'\"]+)(?P=quote)",
        re.IGNORECASE,
    )

    _del_options = ["short"]

    @property
    def root_dir(self) -> Path:
        """
        Parent of the pyproject.toml file.
        """
        return self.poetry.pyproject_path.parent

    @property
    def package(self) -> Path:
        """
        Path to the package directory.
        """
        return self.root_dir / self.poetry.package.name.replace("-", "_")

    @property
    def version(self) -> str:
        """
        Package version from the pyproject.toml file.
        """

        content: dict[str, Any] = self.poetry.file.read()
        poetry_content = content["tool"]["poetry"]
        return poetry_content["version"]

    def substitute(self, file: Path, version: str) -> int:
        """
        Substitute the version in the file.
        """

        replacement = rf"\g<prefix>\g<quote>{version}\g<quote>"

        content = file.read_text()

        match = self._regex.search(content)

        if not match:
            self.line_error(
                f"- Skipped: <warning>{file.relative_to(self.root_dir)}</warning>"
            )
            return 1

        if not self.option("dry-run"):
            file.write_text(
                self._regex.sub(
                    replacement,
                    content,
                    count=1,
                ),
            )

        self.line(f"- Bumped : <info>{file.relative_to(self.root_dir)}</info>")

        return 0

    def resolve(self, filename: str) -> Path:
        """
        Resolve the file path to the package directory.
        """

        file = Path(filename)

        try:
            file = file.resolve(True)
        except FileNotFoundError:

            try:
                root = self.root_dir

                file = root.joinpath(filename).resolve(True)
            except FileNotFoundError:
                package = self.package

                file = package.joinpath(filename).resolve(True)

        finally:
            if not file.is_file():
                raise PathNotFoundError(file)

        return file

    def configure(self) -> None:
        """
        Modifiy all options from `poetry version` to fit the `poetry hook bump`
        command.
        """
        self.options = [
            option(
                "file",
                "f",
                description="Specify the files to update the __version__ string.",
                flag=False,
                multiple=True,
                default=["__init__.py"],
            )
        ] + [option for option in self.options if option.name not in self._del_options]

        super().configure()

    def handle(self) -> int:

        result = super().handle()

        if result:
            return result

        for file in self.option("file"):
            try:
                file = self.resolve(file)
            except PathNotFoundError as e:
                if self.io.is_verbose():
                    self.line_error(f"- Error  : <error>{e.filename}</error>")
                continue

            result += self.substitute(file, self.version)

        return 0
