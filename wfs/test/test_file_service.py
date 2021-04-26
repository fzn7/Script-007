import random
import pytest
import tempfile
import shutil
import os

import wfs.utils as utils

from wfs import fs
from wfs.config import CONTENT_LENGTH


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(0)


@pytest.fixture()
def name():
    return utils.generate_filename()


@pytest.fixture()
def content():
    return utils.generate_string(CONTENT_LENGTH)


@pytest.fixture()
def workdir():
    try:
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    except OSError:
        raise


def test_create(workdir, name, content):
    assert fs.create(workdir, name, content) == workdir + '\\y0cq65zt.txt'


def test_delete(workdir, name, content):
    filepath = fs.create(workdir, name, content)
    assert fs.delete(workdir, os.path.basename(filepath)) is True
    assert fs.delete(workdir, os.path.basename(filepath)) is False


def test_read(workdir, name, content):
    filepath = fs.create(workdir, name, content)

    assert len(fs.read(workdir, filepath)) == CONTENT_LENGTH


def test_print_metadata(workdir, name, content):
    filepath = fs.create(workdir, name, content)

    assert fs.print_metadata(workdir, filepath, lambda x: "metadata")


def test_get_or_create_storage(workdir):
    assert os.path.exists(
        fs.get_or_create_storage(
            os.path.join(
                workdir, "tmp")))
