import utils
import os
import logging


def create(path, *args):
    print args
    with open(os.path.sep.join([path, utils.generate_filename()]), "w") as f:
        f.write(utils.generate_string())


def delete(path, *args):
    file_path = os.path.sep.join([path, args[0]])
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        logging.warn("{} not a file".format(file_path))


def read(path, *args):
    file_path = os.path.sep.join([path, args[0]])
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            print(f.read())


def print_matadata(path, *args):
    file_path = os.path.sep.join([path, args[0]])
    if os.path.isfile(file_path):
        print "{} metadata: {}".format(file_path, os.stat(file_path))