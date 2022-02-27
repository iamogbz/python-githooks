import os
import sys
import stat
import subprocess
from configparser import ConfigParser

from .constants import (
    AVAILABLE_HOOKS,
    CONFIG_COMMAND_KEY,
    CONFIG_FILENAME,
    DEFAULT_COMMANDS,
    DEFAULT_CONFIGURATION,
    GITHOOKS_RELATIVE_DIR,
)


def _write_config_to_file(config, file_path):
    with open(file_path, "w") as configfile:
        config.write(configfile)


def create_config_file(configfile_path):
    config = ConfigParser()
    config.read_dict(DEFAULT_CONFIGURATION)
    _write_config_to_file(config, configfile_path)


def _get_config_file(configfile_path):
    if os.path.isfile(configfile_path):
        config = ConfigParser()
        config.read(configfile_path)
        return config


def _unable_to_find_config(exit=True):
    message = """
        Unable to find the ".githooks.ini" configuration file.
        Please, create it and try again.
        """
    print(message)
    if exit:
        sys.exit(1)


def _command_is_githook_shim(command):
    return command and command.startswith("githook")


def _create_git_hook(*, hook_name, config_section, githook_file):
    hook_command = (
        CONFIG_COMMAND_KEY in config_section and config_section[CONFIG_COMMAND_KEY]
    )
    is_default_hook = hook_command == DEFAULT_COMMANDS.get(hook_name)
    has_existing_hook_file = os.path.isfile(githook_file)
    existing_hook = None
    if has_existing_hook_file:
        with open(githook_file, "r") as f:
            existing_hook = "; ".join(f.read().strip().splitlines())

    if existing_hook and not _command_is_githook_shim(existing_hook):
        keep_existing = is_default_hook or not hook_command
        print("Using" if keep_existing else "Replacing", "existing hook command")
        if keep_existing:
            config_section[CONFIG_COMMAND_KEY] = existing_hook
            hook_command = existing_hook

    with open(githook_file, "w") as f:
        f.write("githooks {}".format(hook_name))

    st = os.stat(githook_file)
    os.chmod(githook_file, st.st_mode | stat.S_IEXEC)

    if hook_command:
        print(
            "{} hook successfully shimmed ↓↓↓".format(hook_name),
            "\n$> {}\n".format(hook_command),
        )


def create_git_hooks(*, configfile_path, githooks_dir):
    config = _get_config_file(configfile_path)
    if not config:
        return _unable_to_find_config()

    for section in config.sections():
        _create_git_hook(
            hook_name=section,
            config_section=config[section],
            githook_file=os.path.join(githooks_dir, section),
        )
    _write_config_to_file(config, configfile_path)


def _delete_git_hook(*, hook_name, config_section, githook_file):
    hook_command = (
        config_section[CONFIG_COMMAND_KEY]
        if CONFIG_COMMAND_KEY in config_section
        else ""
    )
    if not os.path.isfile(githook_file):
        if hook_command:
            print(
                "Skipping unshimming",
                hook_name,
                "because githook file '",
                githook_file,
                "' does not exist",
            )
        return

    with open(githook_file, "r") as f:
        existing_hook = f.read().strip()

    if _command_is_githook_shim(existing_hook):
        with open(githook_file, "w") as f:
            f.write(hook_command)

        if hook_command:
            print("\n{} hook successfully unshimmed ↓↓↓".format(hook_name))
            print("$> {}\n".format(hook_command))


def delete_git_hooks(*, configfile_path, githooks_dir):
    config = _get_config_file(configfile_path)
    try:
        if not config:
            return _unable_to_find_config()

        for hook in AVAILABLE_HOOKS:
            _delete_git_hook(
                hook_name=hook,
                config_section=config[hook] if config.has_section(hook) else None,
                githook_file=os.path.join(githooks_dir, hook),
            )
    finally:
        print(
            "Do not forget to remove",
            CONFIG_FILENAME,
            "file and hooks from",
            GITHOOKS_RELATIVE_DIR,
        )


def execute_git_hook(*, hook_name, configfile_path):
    action = "python-githooks > {}".format(hook_name)
    config = _get_config_file(configfile_path)
    if not config:
        print(action)
        return _unable_to_find_config(False)

    if config.has_option(hook_name, CONFIG_COMMAND_KEY):
        command = config[hook_name][CONFIG_COMMAND_KEY]
        if command:
            print(action)
            sys.exit(subprocess.call(command, shell=True))
