import file_service
import random
import pytest
import tempfile
import shutil
import os
from config import CONTENT_LENGTH


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(0)


@pytest.fixture()
def workdir():
    try:
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    except OSError:
        raise


def test_create(workdir):
    assert file_service.create(workdir) == workdir + '\\41pjso2k.txt'


def test_delete(workdir):
    filepath = file_service.create(workdir)
    assert file_service.delete(workdir, os.path.basename(filepath)) is True
    assert file_service.delete(workdir, os.path.basename(filepath)) is False


def test_read(workdir):
    filepath = file_service.create(workdir)

    assert len(file_service.read(workdir, filepath)) == CONTENT_LENGTH


def test_print_metadata(workdir):
    filepath = file_service.create(workdir)

    assert file_service.print_metadata(workdir, filepath)


def test_get_or_create_storage(workdir):
    assert os.path.exists(
        file_service.get_or_create_storage(
            os.path.join(
                workdir, "tmp")))
