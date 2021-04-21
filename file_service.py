import utils
import os
import logging
from config import CONTENT_LENGTH


def create(path):
    try:
        file_path = os.path.join(path, utils.generate_filename())
        with open(file_path, "w") as f:
            f.write(utils.generate_string(CONTENT_LENGTH))

        logging.info("Created file: {}".format(file_path))
    except Exception as e:
        logging.error(e)


def delete(path, filename):
    file_path = utils.get_filepath(path, filename)

    try:
        os.remove(file_path)
    except Exception as e:
        logging.error(e)


def read(path, filename):
    file_path = utils.get_filepath(path, filename)

    try:
        with open(file_path, "r") as f:
            print(f.read())
    except Exception as e:
        logging.error(e)


def print_matadata(path, filename):
    file_path = utils.get_filepath(path, filename)

    try:
        print "{} metadata: {}".format(file_path, os.stat(file_path))
    except Exception as e:
        logging.error(e)


def get_or_create_storage(storage_folder):
    path = os.getcwd()
    path = os.path.join(path, storage_folder)

    try:
        os.makedirs(path)
    except Exception as e:
        logging.info(e)

    return path
