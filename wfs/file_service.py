import wfs.utils as utils
import os
import logging
from wfs.config import CONTENT_LENGTH


def create(path):
    """
    Create file

    :param path: path to file folder (string)
    :return: created file path (string)
    """
    try:
        file_path = os.path.join(path, utils.generate_filename())
        with open(file_path, "w") as f:
            f.write(utils.generate_string(CONTENT_LENGTH))

        logging.info("Created file: {}".format(file_path))

        return file_path
    except Exception as e:
        logging.error(e)


def delete(path, filename):
    """
    Delete file

    :param path: path to file folder (string)
    :param filename: file name (string)
    :return: True / False on success / failure
    """
    file_path = utils.get_filepath(path, filename)

    try:
        os.remove(file_path)

        return True
    except Exception as e:
        logging.error(e)

    return False


def read(path, filename):
    """
    Read and return file content
    :param path: path to file folder (string)
    :param filename: file name (string)
    :return: file content (string)
    """
    file_path = utils.get_filepath(path, filename)

    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        logging.error(e)


def print_metadata(path, filename):
    """
    get file metadata
    :param path: path to file folder (string)
    :param filename: file name (string)
    :return: formatted file metadata (string)
    """
    file_path = utils.get_filepath(path, filename)

    try:
        return "{} metadata: {}".format(file_path, os.stat(file_path))
    except Exception as e:
        logging.error(e)


def get_or_create_storage(storage_folder):
    """
    Get storage folder path, create if not exist
    :param storage_folder: folder path (string)
    :return: folder path (string)
    """
    path = storage_folder

    try:
        os.makedirs(path)
    except Exception as e:
        logging.debug(e)

    return path
