import subprocess

import pytest

import poetry_plugin_hook


@pytest.fixture(scope="package")
def poetry_list():
    process = subprocess.run(
        [
            "poetry",
            "list",
            "--no-ansi",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    yield process.stdout


@pytest.fixture(
    params=[getattr(poetry_plugin_hook, cls) for cls in poetry_plugin_hook.__all__],
    ids=lambda cls: cls.name,
)
def hook(request):
    return request.param
