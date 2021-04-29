import random
import string
import os

from wfs.config import FILENAME_LENGTH


def generate_filename(length=FILENAME_LENGTH, ext: str = 'txt'):
    """
    Generate filename
    :param ext: file extension
    :param length: filename length (int)
    :return: generated filename (string)
    """
    return "{}.txt".format(generate_string(length))


def generate_string(length):
    """
    Generate string of specific length from dictionary (ascii + digits)
    :param length: string length (int)
    :return: generated string (string)
    """
    return ''.join(
        random.choice(
            string.ascii_lowercase +
            string.digits) for _ in range(length))


def get_filepath(path, filename):
    """
    Generate absolute filepath for filename
    :param path: base path (string)
    :param filename: filename (string)
    :return: absolute filepath (string)
    """

    return os.path.join(path, filename)


def get_basename(filename: str):
    return os.path.splitext(filename)[0]


def get_sig_name(filename: str):
    return f"{get_basename(filename)}.sig"
