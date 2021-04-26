import random
import shutil
import tempfile

import pytest

import os

import wfs.utils as utils

from wfs import sfs
from wfs.config import CONTENT_LENGTH

from ..exception import SignatureException


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(0)


@pytest.fixture()
def name():
    return utils.generate_filename()


@pytest.fixture()
def sig_name(name):
    return utils.get_sig_name(name)


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


def test_create(workdir, name, content, sig_name):
    assert sfs.create(workdir, name, content) == workdir + '\\y0cq65zt.txt'

    assert os.path.exists(os.path.join(workdir, sig_name))


def test_delete(workdir, name, sig_name, content):
    filepath = sfs.create(workdir, name, content)

    assert os.path.exists(os.path.join(workdir, sig_name))
    assert sfs.delete(workdir, os.path.basename(filepath)) is True
    assert not os.path.exists(os.path.join(workdir, sig_name))
    assert sfs.delete(workdir, os.path.basename(filepath)) is False


def test_read(workdir, name, content, sig_name):
    filepath = sfs.create(workdir, name, content)

    assert len(sfs.read(workdir, filepath)) == CONTENT_LENGTH
    assert len(sfs.read(workdir, sig_name)) == 128

    with open(os.path.join(workdir, name), "a") as cf:
        cf.write("badword")

    with pytest.raises(SignatureException):
        sfs.read(workdir, filepath)


def test_print_metadata(workdir, name, content):
    filepath = sfs.create(workdir, name, content)

    assert sfs.print_metadata(workdir, filepath, )


def test_get_or_create_storage(workdir):
    assert os.path.exists(
        sfs.get_or_create_storage(
            os.path.join(
                workdir, "tmp")))
