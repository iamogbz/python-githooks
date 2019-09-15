import os
import shutil
import pytest
from collections import namedtuple
from python_githooks.helpers import create_config_file

__BASE_DIR__ = os.path.join(os.environ["PWD"], "tmp")
__GITHOOKS_BASE_DIR__ = os.path.join(__BASE_DIR__, ".git/hooks")
__GITHOOKS_CONFIGFILE_PATH__ = os.path.join(__BASE_DIR__, ".githooks.ini")
__PATHS__ = namedtuple("Paths", ["base", "hooks", "config"])(
    base=__BASE_DIR__, hooks=__GITHOOKS_BASE_DIR__, config=__GITHOOKS_CONFIGFILE_PATH__
)


@pytest.fixture
def workspace_without_git():
    os.makedirs(__BASE_DIR__)
    yield __PATHS__
    shutil.rmtree(__BASE_DIR__)


@pytest.fixture
def workspace_with_git():
    os.makedirs(__GITHOOKS_BASE_DIR__)
    yield __PATHS__
    shutil.rmtree(__BASE_DIR__)


@pytest.fixture
def workspace_with_config(workspace_with_git):
    create_config_file(__GITHOOKS_CONFIGFILE_PATH__)
    yield __PATHS__
    os.remove(__GITHOOKS_CONFIGFILE_PATH__)
