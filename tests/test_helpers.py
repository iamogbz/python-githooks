import os
from configparser import ConfigParser
from python_githooks.constants import AVAILABLE_HOOKS, DEFAULT_COMMANDS
from python_githooks.helpers import (
    create_config_file,
    create_git_hooks,
    execute_git_hook,
)


def test_config_file_creation(workspace_without_git):
    """create_config_file helper function should create file"""
    configfile_path = os.path.join(workspace_without_git, ".githooks.ini")
    create_config_file(configfile_path=configfile_path)
    assert os.path.isfile(configfile_path)


def test_config_file_default_values(workspace_without_git):
    """create_config_file helper function should create file with defaults values"""
    configfile_path = os.path.join(workspace_without_git, ".githooks.ini")
    create_config_file(configfile_path=configfile_path)
    config = ConfigParser()
    config.read(configfile_path)
    assert config.sections() == sorted(AVAILABLE_HOOKS)
    assert config["pre-commit"]["command"] == DEFAULT_COMMANDS.get("pre-commit")


def test_git_hook_creation(workspace_with_git):
    """create_git_hooks helper function should create hooks files in the git hook folder"""
    githooks_dir = os.path.join(workspace_with_git, ".git/hooks")
    for hook_name in AVAILABLE_HOOKS:
        assert os.path.isfile(os.path.join(githooks_dir, hook_name)) is False

    configfile_path = os.path.join(workspace_with_git, ".githooks.ini")
    create_config_file(configfile_path=configfile_path)
    create_git_hooks(configfile_path=configfile_path, githooks_dir=githooks_dir)

    for hook_name in AVAILABLE_HOOKS:
        assert os.path.isfile(os.path.join(githooks_dir, hook_name)) is True
        with open(os.path.join(githooks_dir, hook_name), "r") as f:
            assert f.read() == "githooks {}".format(hook_name)


def test_git_hook_creation_permissions(workspace_with_git):
    """create_git_hooks helper function should create hooks files with correct permissions"""
    githooks_dir = os.path.join(workspace_with_git, ".git/hooks")
    configfile_path = os.path.join(workspace_with_git, ".githooks.ini")
    create_config_file(configfile_path=configfile_path)
    create_git_hooks(configfile_path=configfile_path, githooks_dir=githooks_dir)
    for hook_name in AVAILABLE_HOOKS:
        assert os.access(os.path.join(githooks_dir, hook_name), os.X_OK) is True


def test_git_hook_creation_exit(mocker, workspace_with_git):
    """create_git_hooks helper function should exit if not valid configuration file is provided"""
    mocked_sys_exit = mocker.patch("sys.exit")
    githooks_dir = os.path.join(workspace_with_git, ".git/hooks")
    create_git_hooks(configfile_path="wrong_config_file.ini", githooks_dir=githooks_dir)
    mocked_sys_exit.assert_called_once_with(1)


def test_git_hook_execution_no_config(mocker):
    """execute_git_hook helper function should exit with command successfully executed"""
    mocked_sys_exit = mocker.patch("sys.exit")
    execute_git_hook(hook_name="pre-commit", configfile_path="wrong_config_file.ini")
    mocked_sys_exit.assert_called_once_with(1)


def test_git_hook_execution_exit(mocker, workspace_with_config):
    """execute_git_hook helper function should exit with command successfully executed"""
    mocked_sys_exit = mocker.patch("sys.exit")
    configfile_path = os.path.join(workspace_with_config, ".githooks.ini")
    execute_git_hook(hook_name="pre-commit", configfile_path=configfile_path)
    mocked_sys_exit.assert_called_once_with(0)


def test_git_hook_execution_no_exit(mocker, workspace_with_config):
    """execute_git_hook helper function should exit with command successfully executed"""
    mocked_sys_exit = mocker.patch("sys.exit")
    configfile_path = os.path.join(workspace_with_config, ".githooks.ini")
    execute_git_hook(hook_name="no-commit", configfile_path=configfile_path)
    mocked_sys_exit.assert_not_called()
