# py-githooks

[![code linting: flake8](https://img.shields.io/badge/lint-flake8-blue.svg)](http://flake8.pycqa.org/) [![code quality: pytest](https://img.shields.io/badge/test-pytest-green.svg)](https://docs.pytest.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) [![Pypi](https://img.shields.io/pypi/v/py-githooks)](https://pypi.org/project/py-githooks/) [![CircleCI](https://circleci.com/gh/iamogbz/python-githooks.svg?style=svg)](https://circleci.com/gh/iamogbz/python-githooks)
[![Coverage Status](https://coveralls.io/repos/github/iamogbz/python-githooks/badge.svg?branch=master)](https://coveralls.io/github/iamogbz/python-githooks?branch=master)

> Create git hooks with ease using a simple configuration file in a git project

## Install

```bash
pip install py-githooks
```

## Usage

1. Create a `.githooks.ini` configuration file (If not provided a dummy configuration file will be created).
2. Add sections based on `git hooks names` followed by a `command` property with the shell code you want to run.
3. Run either `python -m python_githooks` or `githooks` in your virtual environment.

**Configuration file example**:

```ini
# .githooks.ini

[pre-commit]
command = pytest --cov

[pre-push]
command = pytest --cov && flake8
```

## Removing a hook

If you already created a hook and now want to remove it, just set the command value to empty, like this:

```ini
# .githooks.ini

[pre-commit]
command =
```

This will not actually physically remove the hook from the git local project, just will make it instantly exit with `0` status code.

## Unuse

1. Running `python -m python_githooks --deactivate` or `githooks --deactivate` will stop shimming git hooks but keep the commands in `.git/hooks`
2. Run `rm .githooks.ini` to remove the configuration file (optional).
3. `rm .git/hooks/pre-commit` or any other githook to stop them from executing (optional).
   e.g. `rm .git/hooks/*`

## License

py-githooks is [MIT-licensed](LICENSE).
