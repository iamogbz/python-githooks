import os

# Supported git hooks
AVAILABLE_HOOKS = {
    "applypatch-msg",
    "commit-msg",
    "pre-applypatch",
    "pre-auto-gc",
    "pre-commit",
    "pre-push",
    "pre-rebase",
    "pre-receive",
    "prepare-commit-msg",
    "post-applypatch",
    "post-commit",
    "post-checkout",
    "post-merge",
    "post-receive",
    "post-rewrite",
    "post-update",
    "update",
}
# Git hooks relative dir
GITHOOKS_RELATIVE_DIR = os.path.join(".git", "hooks")
# Githooks configuration
CONFIG_FILENAME = ".githooks.ini"
CONFIG_COMMAND_KEY = "command"
DEFAULT_COMMANDS = {"pre-commit": "echo Replace this line with your own command"}
DEFAULT_CONFIGURATION = {
    hook: {CONFIG_COMMAND_KEY: DEFAULT_COMMANDS.get(hook, "")}
    for hook in sorted(AVAILABLE_HOOKS)
}
