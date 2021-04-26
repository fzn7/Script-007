import argparse
import os

import wfs.file_service as fs
import wfs.exception as exception

import logging

commands = {
    "create": fs.create,
    "delete": fs.delete,
    "read": fs.read,
    "print_matadata": fs.print_metadata,
}


def main(storage_folder, command, args):
    """
    Execute user defined command
    :param storage_folder: working folder (string)
    :param command: command (string)
    :param args: command args (list)
    :return: None
    """
    if command not in commands:
        raise exception.ArgumentException(
            "command {} not in set of commands".format(command))

    logging.info("storage folder: {}".format(storage_folder))
    logging.info("command: {}".format(command))
    logging.info("command args: {}".format(args))

    path = fs.get_or_create_storage(storage_folder)
    commands[command](path, *args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File System Prototype')
    parser.add_argument(
        "--storage_folder",
        type=str,
        help="storage folder for files",
        default=os.getcwd())
    parser.add_argument(
        "command",
        type=str,
        help="fs command: {}".format(
            commands.keys()))
    parser.add_argument(
        "--args",
        nargs='+',
        help="command arg list",
        default=[])
    args = parser.parse_args()

    main(args.storage_folder, args.command, args.args)
