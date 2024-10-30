# poetry-plugin-hook

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poetry-plugin-hook)](https://pypi.org/project/poetry-plugin-hook/)
[![PyPI - Version](https://img.shields.io/pypi/v/poetry-plugin-hook)](https://pypi.org/project/poetry-plugin-hook/)
[![PyPI - License](https://img.shields.io/pypi/l/poetry-plugin-hook)](https://raw.githubusercontent.com/d-chris/poetry-plugin-hook/main/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://raw.githubusercontent.com/d-chris/poetry-plugin-hook/main/.pre-commit-config.yaml)
<!-- [![PyPI - Downloads](https://img.shields.io/pypi/dm/poetry-plugin-hook)](https://pypi.org/project/poetry-plugin-hook/) -->
<!-- [![GitHub - Release](https://img.shields.io/github/v/tag/d-chris/poetry-plugin-hook?logo=github&label=github)](https://github.com/d-chris/poetry-plugin-hook) -->
<!-- [![GitHub - Pytest](https://img.shields.io/github/actions/workflow/status/d-chris/poetry-plugin-hook/pytest.yml?logo=github&label=pytest)](https://github.com/d-chris/poetry-plugin-hook/actions/workflows/pytest.yml) -->
<!-- [![GitHub - Page](https://img.shields.io/website?url=https%3A%2F%2Fd-chris.github.io%2Fpoetry-plugin-hook&up_message=pdoc&logo=github&label=documentation)](https://d-chris.github.io/poetry-plugin-hook) -->
<!-- [![codecov](https://codecov.io/gh/d-chris/poetry-plugin-hook/graph/badge.svg?token=U7I9FYMRSR)](https://codecov.io/gh/d-chris/poetry-plugin-hook) -->

---

`poetry` plugin to register wrapped commands to use ase `pre-commit-hooks`. all hook commands return zero on success and non-zero on failure.

## install

```shell
$ pip install poetry-plugin-hook
```

or with `poetry`

```shell
$ poetry self add poetry-plugin-hook
```

## hook latest

Wrapper for `poetry show -o -T` command.

Exit code represents the number of outdated packages.

```bash
$ poetry hook latest && echo exit-code: $?

All top-level dependencies are up-to-date.
exit-code: 0
```

## hook sync

Wrapper for `poetry install --sync` command.

With `--exit` option, the command returns the corresponding value as exit code. With it's default `--exit=any` the sum of *installs*, *updates* and *removals* is returned.

```bash
$ poetry hook sync --dry-run && echo exit-code: $?

No dependencies to install or update.
exit-code: 0
```

## Dependencies

[![PyPI - cleo](https://img.shields.io/pypi/v/cleo?logo=pypi&logoColor=white&label=cleo)](https://pypi.org/project/cleo/)
[![PyPI - poetry](https://img.shields.io/pypi/v/poetry?logo=poetry&logoColor=white&label=poetry)](https://pypi.org/project/poetry/)

---
