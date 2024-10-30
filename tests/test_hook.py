import subprocess


def test_poetry_list(poetry_list, hook):

    assert hook.name in poetry_list


def test_poetry_help(poetry_list, hook):

    assert hook.description in poetry_list


def test_hook_help(hook):

    process = subprocess.run(
        [
            "poetry",
            hook.name,
            "--no-ansi",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )

    assert process.returncode == 0
    assert hook.description in process.stdout


def test_hook(hook):

    process = subprocess.run(
        [
            "poetry",
            hook.name,
            "--no-ansi",
        ],
        capture_output=True,
        encoding="utf-8",
    )

    assert process.stdout != ""
