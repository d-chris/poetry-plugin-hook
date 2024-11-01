import pytest

import poetry_plugin_hook

from . import application


@pytest.fixture(scope="session")
def poetry():
    """Run Poetry with the given arguments."""

    return application


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
