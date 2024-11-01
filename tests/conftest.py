import subprocess

import pytest
from cleo.io.buffered_io import BufferedOutput
from cleo.io.inputs.argv_input import ArgvInput
from poetry.console.application import Application

import poetry_plugin_hook


@pytest.fixture(scope="session")
def poetry():
    """Run Poetry with the given arguments."""

    def wrapped(*args: str) -> subprocess.CompletedProcess:

        args = [__file__] + list(args)

        input = ArgvInput(args)
        stdout = BufferedOutput()
        stderr = BufferedOutput()

        try:
            result = Application().run(
                input=input,
                output=stdout,
                error_output=stderr,
            )
        except SystemExit as e:
            result = e.code

        return subprocess.CompletedProcess(
            args=args,
            returncode=result,
            stdout=stdout.fetch(),
            stderr=stderr.fetch(),
        )

    return wrapped


@pytest.fixture(scope="module")
def poetry_list(poetry):
    """List of available poetry commands."""

    yield poetry("list", "--no-ansi").stdout


@pytest.fixture(
    params=[getattr(poetry_plugin_hook, cls) for cls in poetry_plugin_hook.__all__],
    ids=lambda cls: cls.name,
)
def hook(request):
    """Get all classes from poetry_plugin_hook."""

    return request.param
