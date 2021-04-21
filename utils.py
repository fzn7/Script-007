import random
import string
import os

from config import FILENAME_LENGTH


def generate_filename(length=FILENAME_LENGTH):
    return "{}.txt".format(generate_string(length))


def generate_string(length):
    return ''.join(
        random.choice(
            string.ascii_lowercase +
            string.digits) for _ in range(length))


def get_filepath(path, filename):
    return os.path.join(path, filename)
