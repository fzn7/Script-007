import random
import string
import os


def generate_filename(length=8):
    return "{}.txt".format(generate_string(length))


def generate_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_or_create_storage(storage_folder):
    path = os.getcwd()
    path = os.path.join(path, storage_folder)

    if not os.path.exists(path):
        os.makedirs(path)

    return path
