import sys

import python_githooks
from python_githooks.__main__ import main


def test_main_entry_point_exit(mocker, workspace_without_git):
    """main function should exit if ran in not valid git project"""
    python_githooks.__main__.__BASE_DIR__ = workspace_without_git.base
    python_githooks.__main__.__GITHOOKS_BASE_DIR__ = workspace_without_git.hooks
    mocked_sys_exit = mocker.patch("sys.exit")
    sys.argv = sys.argv[:1]
    main()
    mocked_sys_exit.assert_called_once_with(1)


def test_main_entry_point_config_file_creation(mocker, workspace_with_git):
    """main function should create config file if it doesn't exists"""
    python_githooks.__main__.__BASE_DIR__ = workspace_with_git.base
    python_githooks.__main__.__GITHOOKS_BASE_DIR__ = workspace_with_git.hooks
    python_githooks.__main__.__GITHOOKS_CONFIGFILE_PATH__ = workspace_with_git.config
    mocker.spy(python_githooks.__main__, "create_config_file")
    mocker.spy(python_githooks.__main__, "create_git_hooks")
    sys.argv = sys.argv[:1]
    main()
    assert python_githooks.__main__.create_config_file.call_count == 1
    assert python_githooks.__main__.create_git_hooks.call_count == 1


def test_main_entry_point_githook_execution(mocker, workspace_with_config):
    """main function should execute first argument as githook"""
    python_githooks.__main__.__BASE_DIR__ = workspace_with_config.base
    python_githooks.__main__.__GITHOOKS_BASE_DIR__ = workspace_with_config.hooks
    python_githooks.__main__.__GITHOOKS_CONFIGFILE_PATH__ = workspace_with_config.config
    mocked_sys_exit = mocker.patch("sys.exit")
    mocked_execute_git_hook = mocker.spy(python_githooks.__main__, "execute_git_hook")
    sys.argv = sys.argv[:1] + ["--activate", "pre-commit"]
    main()
    assert mocked_execute_git_hook.call_count == 1
    assert mocked_execute_git_hook.call_args[1]["hook_name"] == "pre-commit"
    mocked_sys_exit.assert_called_once_with(0)
