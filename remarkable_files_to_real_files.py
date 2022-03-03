#!/usr/bin/env python3
from RemarkableFlatFileSystem import RemarkableFlatFileSystem
from distutils.dir_util import mkpath
from os import path, symlink
from sys import argv

IN_PATH = argv[1] if len(argv) >= 1  else "/home/root/.local/share/remarkable/xochitl/" 
OUT_PATH = argv[2] if len(argv) >= 2  else "/home/root/rmfile/"


def create_dir_if_not_exists(directory):
    if not path.exists(directory):
        mkpath(directory)


def create_symlink_for_rm_file(rm_file):
    if not path.exists(rm_file.rm_file_path) \
            and bool(rm_file.real_file_path)\
            and not "." in rm_file.rm_file_path:
        try:
            symlink(rm_file.real_file_path, rm_file.rm_file_path)
            print(f"└─> Symlink success!\n")
        except FileNotFoundError:
            print(f"└─> Symlink failed\n")
    else:
        print(f"└─> File already exists\n")


if __name__ == "__main__":
    rm_files = RemarkableFlatFileSystem(IN_PATH, OUT_PATH)
    for file in rm_files:
        print("┌─ Trying to create symlink")
        print(f"├─> FROM: {file.real_file_path}")
        print(f"├─> TO: {file.rm_file_path}")
        create_dir_if_not_exists(file.rm_parent_path)
        create_symlink_for_rm_file(file)
