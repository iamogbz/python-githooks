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
    create_config_file(configfile_path=workspace_without_git.config)
    assert os.path.isfile(workspace_without_git.config)


def test_config_file_default_values(workspace_without_git):
    """create_config_file helper function should create file with defaults values"""
    create_config_file(configfile_path=workspace_without_git.config)
    config = ConfigParser()
    config.read(workspace_without_git.config)
    assert config.sections() == sorted(AVAILABLE_HOOKS)
    assert config["pre-commit"]["command"] == DEFAULT_COMMANDS.get("pre-commit")


def test_git_hook_creation(workspace_with_git):
    """create_git_hooks helper function should create hooks files in the git hook folder"""
    for hook_name in AVAILABLE_HOOKS:
        assert not os.path.isfile(os.path.join(workspace_with_git.hooks, hook_name))

    create_config_file(configfile_path=workspace_with_git.config)
    create_git_hooks(
        configfile_path=workspace_with_git.config, githooks_dir=workspace_with_git.hooks
    )

    for hook_name in AVAILABLE_HOOKS:
        assert os.path.isfile(os.path.join(workspace_with_git.hooks, hook_name))
        with open(os.path.join(workspace_with_git.hooks, hook_name), "r") as f:
            assert f.read() == "githooks {}".format(hook_name)


def test_git_hook_preservation(workspace_with_git):
    """create_config_file helper function should preserve valid existing hook values"""
    with open(os.path.join(workspace_with_git.hooks, "pre-commit"), "w") as f:
        f.write("echo successfully preserved")
    with open(os.path.join(workspace_with_git.hooks, "post-commit"), "w") as f:
        f.write("githooks donotkeep")

    create_config_file(configfile_path=workspace_with_git.config)
    create_git_hooks(
        configfile_path=workspace_with_git.config, githooks_dir=workspace_with_git.hooks
    )
    config = ConfigParser()
    config.read(workspace_with_git.config)
    assert config["pre-commit"]["command"] == "echo successfully preserved"
    assert config["post-commit"]["command"] == ""


def test_git_hook_creation_permissions(workspace_with_git):
    """create_git_hooks helper function should create hooks files with correct permissions"""
    create_config_file(configfile_path=workspace_with_git.config)
    create_git_hooks(
        configfile_path=workspace_with_git.config, githooks_dir=workspace_with_git.hooks
    )
    for hook_name in AVAILABLE_HOOKS:
        assert os.access(os.path.join(workspace_with_git.hooks, hook_name), os.X_OK)


def test_git_hook_creation_exit(mocker, workspace_with_git):
    """create_git_hooks helper function should exit if not valid configuration file is provided"""
    mocked_sys_exit = mocker.patch("sys.exit")
    create_git_hooks(
        configfile_path="wrong_config_file.ini", githooks_dir=workspace_with_git.hooks
    )
    mocked_sys_exit.assert_called_once_with(1)


def test_git_hook_execution_no_config(mocker):
    """execute_git_hook helper function should exit with command successfully executed"""
    mocked_sys_exit = mocker.patch("sys.exit")
    execute_git_hook(hook_name="pre-commit", configfile_path="wrong_config_file.ini")
    mocked_sys_exit.assert_called_once_with(1)


def test_git_hook_execution_exit(mocker, workspace_with_config):
    """execute_git_hook helper function should exit with command successfully executed"""
    mocked_sys_exit = mocker.patch("sys.exit")
    execute_git_hook(
        hook_name="pre-commit", configfile_path=workspace_with_config.config
    )
    mocked_sys_exit.assert_called_once_with(0)


def test_git_hook_execution_no_exit(mocker, workspace_with_config):
    """execute_git_hook helper function should exit with command successfully executed"""
    mocked_sys_exit = mocker.patch("sys.exit")
    execute_git_hook(
        hook_name="no-commit", configfile_path=workspace_with_config.config
    )
    mocked_sys_exit.assert_not_called()
