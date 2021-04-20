import argparse
import file_service as fs
import utils as u
import os

commands = {"create": fs.create, "delete": fs.delete, "read": fs.read, "print_matadata": fs.print_matadata}

def main(storage_folder, command, args):
    if command not in commands:
        raise Exception("command {} not in set of commands".format(command))

    print("storage folder: {}".format(storage_folder))
    print("command: {}".format(command))
    print("command args: {}".format(args))

    path = u.get_or_create_storage(storage_folder)
    commands[command](path, *args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File System Prototype')
    parser.add_argument("--storage_folder", type=str, help="storage folder for files", default=os.getcwd())
    parser.add_argument("command", type=str, help="fs command: {}".format(commands.keys()))
    parser.add_argument("--args", nargs='+', help="command arg list")
    args = parser.parse_args()

    main(args.storage_folder, args.command, args.args)
