import pytest


def test_poetry_list(poetry_list, hook):
    """Test if the hook name is in the `poetry list`."""

    assert hook.name in poetry_list


def test_poetry_help(poetry_list, hook):
    """Test if the hook description is in the `poetry list`."""

    assert hook.description in poetry_list


def test_hook_help(poetry, hook):
    """Test if the hook help is working."""

    process = poetry(
        hook.name,
        "--no-ansi",
        "--help",
    )

    assert process.returncode == 0
    assert hook.description in process.stdout


@pytest.mark.skip(reason="Slow tests")
def test_hook(poetry, hook):
    """Execute the hookand check if the command exists."""

    process = poetry(
        hook.name,
        "--no-ansi",
    )

    assert process.stderr.strip() == ""
