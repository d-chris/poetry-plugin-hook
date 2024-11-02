# poetry-plugin-hook

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poetry-plugin-hook)](https://pypi.org/project/poetry-plugin-hook/)
[![PyPI - Version](https://img.shields.io/pypi/v/poetry-plugin-hook)](https://pypi.org/project/poetry-plugin-hook/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/poetry-plugin-hook)](https://pypi.org/project/poetry-plugin-hook/)
[![PyPI - License](https://img.shields.io/pypi/l/poetry-plugin-hook)](https://raw.githubusercontent.com/d-chris/poetry-plugin-hook/main/LICENSE)
[![GitHub - Pytest](https://img.shields.io/github/actions/workflow/status/d-chris/poetry-plugin-hook/pytest.yml?logo=github&label=pytest)](https://github.com/d-chris/poetry-plugin-hook/actions/workflows/pytest.yml)
[![GitHub - Page](https://img.shields.io/website?url=https%3A%2F%2Fd-chris.github.io%2Fpoetry-plugin-hook&up_message=pdoc&logo=github&label=documentation)](https://d-chris.github.io/poetry-plugin-hook)
[![GitHub - Release](https://img.shields.io/github/v/tag/d-chris/poetry-plugin-hook?logo=github&label=github)](https://github.com/d-chris/poetry-plugin-hook)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://raw.githubusercontent.com/d-chris/poetry-plugin-hook/main/.pre-commit-config.yaml)
[![codecov](https://codecov.io/gh/d-chris/poetry-plugin-hook/graph/badge.svg?token=RNNV7TN8WZ)](https://codecov.io/gh/d-chris/poetry-plugin-hook)

---

[`poetry`](https://python-poetry.org/) plugin to register wrapped commands to use as [`pre-commit-hooks`](https://pre-commit.com/). all hook commands return zero on success and non-zero on failure.

## install

```shell
$ pip install poetry-plugin-hook
```

or with `poetry`

> Especially on [Windows](https://python-poetry.org/docs/cli/#self), self commands that update or remove packages may be problematic.

```shell
$ poetry self add poetry-plugin-hook
```

## hook latest

Wrapper for `poetry show -o -T` command.

Exit code represents the number of outdated packages.

```shell
$ poetry hook latest --help

  Description:
    Check if all top-level dependencies are up-to-date.

  Usage:
    hook latest [options] [--] [<package>]

  Arguments:
    package                    The package to inspect

  Options:
        --without=WITHOUT      The dependency groups to ignore. (multiple values allowed)
        --with=WITH            The optional dependency groups to include. (multiple values allowed)
        --only=ONLY            The only dependency groups to include. (multiple values allowed)
    -l, --latest               Show the latest version. (option is always True)
    -o, --outdated             Show the latest version but only for packages that are outdated. (option is always True)
    -T, --top-level            Show only top-level dependencies. (option is always True)
    -h, --help                 Display help for the given command. When no command is given display help for the list command.
    -q, --quiet                Do not output any message.
    -V, --version              Display this application version.
        --ansi                 Force ANSI output.
        --no-ansi              Disable ANSI output.
    -n, --no-interaction       Do not ask any interactive question.
        --no-plugins           Disables plugins.
        --no-cache             Disables Poetry source caches.
    -C, --directory=DIRECTORY  The working directory for the Poetry command (defaults to the current working directory).
    -v|vv|vvv, --verbose       Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.

  Help:
    poetry hook latest [options]
```

## hook sync

Wrapper for `poetry install --sync` command.

With `--exit` option, the command returns the corresponding value as exit code. With it's default `--exit=any` the sum of *installs*, *updates* and *removals* is returned.

```shell
$ poetry hook sync --help

  Description:
    Synchronize the environment with the locked packages and the specified groups.

  Usage:
    hook sync [options]

  Options:
        --exit=EXIT            Specify the value to return as exitcode. choices=['any', 'installs', 'updates', 'removals'] [default: "any"]
        --without=WITHOUT      The dependency groups to ignore. (multiple values allowed)
        --with=WITH            The optional dependency groups to include. (multiple values allowed)
        --only=ONLY            The only dependency groups to include. (multiple values allowed)
        --sync                 Synchronize the environment with the locked packages and the specified groups. (option is always True)
        --no-root              Do not install the root package (the current project).
        --no-directory         Do not install any directory path dependencies; useful to install dependencies without source code, e.g. for caching of Docker layers)
        --dry-run              Output the operations but do not execute anything (implicitly enables --verbose).
    -E, --extras=EXTRAS        Extra sets of dependencies to install. (multiple values allowed)
        --all-extras           Install all extra dependencies.
        --only-root            Exclude all dependencies.
    -h, --help                 Display help for the given command. When no command is given display help for the list command.
    -q, --quiet                Do not output any message.
    -V, --version              Display this application version.
        --ansi                 Force ANSI output.
        --no-ansi              Disable ANSI output.
    -n, --no-interaction       Do not ask any interactive question.
        --no-plugins           Disables plugins.
        --no-cache             Disables Poetry source caches.
    -C, --directory=DIRECTORY  The working directory for the Poetry command (defaults to the current working directory).
    -v|vv|vvv, --verbose       Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.

  Help:
    poetry hook sync [options]
```

## pre-commit-config

Add the following to your `.pre-commit-config.yaml` file.

```yaml
repos:
  - repo: https://github.com/d-chris/poetry-plugin-hook
    rev: v1.1.0
    hooks:
        - id: poetry-hook-latest
        - id: poetry-hook-sync
          args: [ "--dry-run" ]
```

### usage

1. Make sure pre-commit is installed, see [official documentation](https://pre-commit.com/#installation).
  ```shell
  $ pre-commit --version

    pre-commit 3.7.1
  ```
2. `cd` into your project and register hooks and install them. this may take a while.
  ```shell
  $ pre-commit install --install-hooks -t pre-commit -t pre-push

    pre-commit installed at .git\hooks\pre-commit
    pre-commit installed at .git\hooks\pre-push
  ```
3. Test the pre-push hook.
  ```shell
  $ pre-commit run poetry-hook-latest --all-files --hook-stage pre-push

    poetry-hook-latest.......................................................Failed
    - hook id: poetry-hook-latest
    - exit code: 1

    pytest-cov 5.0.0 6.0.0 Pytest plugin for measuring coverage.
  ```
4. Test the pre-commit hooks.
  ```shell
  $ pre-commit run poetry-hook-sync --all-files

    poetry-hook-sync.........................................................Failed
    - hook id: poetry-hook-sync
    - exit code: 1

    Installing dependencies from lock file

    Package operations: 0 installs, 1 update, 0 removals

      - Downgrading pytest-cov (6.0.0 -> 5.0.0)

    Installing the current project: poetry-plugin-hook (0.0.0)
  ```

## pre-commit-hooks

```yaml
- id: poetry-hook-latest
  name: poetry-hook-latest
  description: Check if all top-level dependencies are up-to-date.
  entry: poetry hook latest
  language: system
  pass_filenames: false
  always_run: true
  stages: [pre-push]
- id: poetry-hook-sync
  name: poetry-hook-sync
  description: Synchronize the environment with the locked packages and the specified groups.
  entry: poetry hook sync
  language: system
  pass_filenames: false
  files: ^(.*/)?(poetry\.lock|pyproject\.toml)$
```

## Dependencies

[![PyPI - cleo](https://img.shields.io/pypi/v/cleo?logo=pypi&logoColor=white&label=cleo)](https://pypi.org/project/cleo/)
[![PyPI - poetry](https://img.shields.io/pypi/v/poetry?logo=poetry&logoColor=white&label=poetry)](https://pypi.org/project/poetry/)

---
