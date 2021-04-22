import utils
import random
import pytest


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(0)


def test_generate_filename():
    assert utils.generate_filename(10) == '41pjso2krv.txt'


def test_generate_string():
    assert utils.generate_string(20) == '41pjso2krv6sk1wj6936'


def test_get_filepath():
    assert utils.get_filepath("a", "b") == "a\\b"
