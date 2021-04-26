from typing import Callable

import wfs.utils as utils
import os
import logging


class FileService(object):
    def create(self, path: str, name: str, content: str) -> str:
        """
        Create file

        :param name:
        :param content:
        :param path: path to file folder (string)
        :return: created file path (string)
        """
        try:
            file_path = os.path.join(path, name)
            with open(file_path, "w") as f:
                f.write(content)

            logging.info("Created file: {}".format(file_path))

            return file_path
        except Exception as e:
            logging.error(e)

    def delete(self, path: str, filename: str) -> bool:
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

    def read(self, path, filename) -> str:
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

    def print_metadata(self, path, filename, stat: Callable = os.stat) -> str:
        """
        get file metadata
        :param path: path to file folder (string)
        :param filename: file name (string)
        :param stat:
        :return: formatted file metadata (string)
        """
        file_path = utils.get_filepath(path, filename)

        try:
            return "{} metadata: {}".format(file_path, stat(file_path))
        except Exception as e:
            logging.error(e)

    def get_or_create_storage(self, storage_folder: str) -> str:
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
