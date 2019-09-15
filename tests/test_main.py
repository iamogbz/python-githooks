import sys
from contextlib import contextmanager

import python_githooks
from python_githooks.__main__ import main


@contextmanager
def mock_properties(obj, mappings):
    initials = {}
    for name, value in mappings.items():
        initials[name] = getattr(obj, name)
        setattr(obj, name, value)
    yield obj
    for name, value in initials.items():
        setattr(obj, name, value)


def mock_githooks_main(workspace_paths):
    mappings = {
        "BASE_DIR": workspace_paths.base,
        "GITHOOKS_BASE_DIR": workspace_paths.hooks,
        "GITHOOKS_CONFIGFILE_PATH": workspace_paths.config,
    }
    return mock_properties(
        python_githooks.__main__,
        {"__{}__".format(name): value for name, value in mappings.items()},
    )


def test_main_entry_point_exit(mocker, no_sys_args, workspace_without_git):
    """main function should exit if ran in not valid git project"""
    with mock_githooks_main(workspace_without_git):
        mocked_sys_exit = mocker.patch("sys.exit")
        main()
        mocked_sys_exit.assert_called_once_with(1)


def test_main_entry_point_config_file_creation(mocker, no_sys_args, workspace_with_git):
    """main function should create config file if it doesn't exists"""
    with mock_githooks_main(workspace_with_git) as mocked_githooks_main:
        mocked_create_config = mocker.spy(mocked_githooks_main, "create_config_file")
        mocked_create_githooks = mocker.spy(mocked_githooks_main, "create_git_hooks")
        sys.argv = sys.argv[:1]
        main()
        assert mocked_create_config.call_count == 1
        assert mocked_create_githooks.call_count == 1


def test_main_entry_point_githook_execution(mocker, no_sys_args, workspace_with_config):
    """main function should execute first argument as githook"""
    with mock_githooks_main(workspace_with_config) as mocked_githooks_main:
        mocked_sys_exit = mocker.patch("sys.exit")
        mocked_execute_git_hook = mocker.spy(mocked_githooks_main, "execute_git_hook")
        sys.argv.extend(["--activate", "pre-commit"])
        main()
        assert mocked_execute_git_hook.call_count == 1
        assert mocked_execute_git_hook.call_args[1]["hook_name"] == "pre-commit"
        mocked_sys_exit.assert_called_once_with(0)
