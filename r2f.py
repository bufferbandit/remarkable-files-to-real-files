#!/usr/bin/env python3
from RemarkableFlatFileSystem import RemarkableFlatFileSystem
from distutils.dir_util import mkpath
from shutil import copy

from os import path, symlink
from sys import argv

IN_PATH = argv[1] if len(argv) > 1  else "/home/root/.local/share/remarkable/xochitl/" 
OUT_PATH = argv[2] if len(argv) > 2  else "/home/root/rmfile/"
SUPPORT_HIDDEN_FILES = bool(int(argv[3])) if len(argv) > 3  else True

def create_dir_if_not_exists(directory):
    if not path.exists(directory):
        mkpath(directory)


def create_symlink_for_rm_file(rm_file):
    if not path.exists(rm_file.rm_file_path) \
            and bool(rm_file.real_file_path)\
            and (SUPPORT_HIDDEN_FILES and 
                    not any(item.startswith(".") for item in rm_file.rm_filepath_parent_files)):
        if 1:
        #try:
            # symlink(rm_file.real_file_path, rm_file.rm_file_path)
            # TODO: Find a more elegant way to switch the copying/symlinking implementation (eg. providing it as a callback)
            copy(
                            rm_file.real_file_path,
                            rm_file.rm_file_path
                                    .replace("|","")
                                    .replace("+","")
                                    .replace(",","") 
                                    .replace("&","") 
                                    .replace(":","") 
                                    .replace("藏","") 
                                    .replace("海","") 
                                    .replace("花","") 
                                    .replace("\n","") 
                                    .replace("?","") 
                                    .replace("https//","https")
                                    .replace("http//","http")
                                    .replace("\"","")
                                    .replace(">","")
                                    .replace("<","")
                                    .replace("=","")
                                    .replace("*","")
                            )        
            print(f"└─> Symlink success!\n")
        #except FileNotFoundError:
            #print(f"└─> Symlink failed\n")
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
