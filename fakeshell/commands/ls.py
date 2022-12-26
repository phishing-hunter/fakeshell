import os
import optparse
import shlex
import pwd
import stat
import time
import grp
from datetime import datetime

def cmd_ls(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    parser.add_option("-l", "--long", action="store_true", default=False)
    parser.add_option("-a", "--all", action="store_true", default=False)
    parser.add_option("-R", "--recursive", action="store_true", default=False)
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    path = "." if not args else args[0]

    if options.recursive:
        for root, dirs, files in os.walk(path):
            std_out += f"\n{root}:\n"
            if options.long:
                std_out += print_long_format(root, files)
            else:
                std_out += print_short_format(root, files, options.all)
    else:
        if not options.all:
            files = [f for f in os.listdir(path) if not f.startswith(".")]
        else:
            files = os.listdir(path)
        if options.long:
            std_out = print_long_format(path, files)
        else:
            std_out = print_short_format(path, files, options.all)
    return std_out

def print_short_format(path, files, show_all):
    std_out = ""
    for file in files:
        std_out += f"{file}  "
    std_out += "\n"
    return std_out

def print_long_format(path, files):
    std_out = ""
    for file in files:
        file_path = os.path.join(path, file)
        file_stats = os.lstat(file_path)
        file_permission = stat.filemode(file_stats.st_mode)
        file_link = file_stats.st_nlink
        try:
            file_owner = pwd.getpwuid(file_stats.st_uid).pw_name
        except KeyError:
            file_owner = file_stats.st_uid
        try:
            file_group = pwd.getpwuid(file_stats.st_gid).pw_name
        except KeyError:
            file_group = file_stats.st_gid

        file_size = file_stats.st_size
        file_modify_time = datetime.fromtimestamp(file_stats.st_mtime).strftime("%b %d %H:%M")
        is_link = False
        if os.path.islink(file_path):
            is_link = True
            file_size = os.readlink(file_path)
        std_out += f"{file_permission} {file_link} {file_owner}\t{file_group}\t{file_size:>{len(str(file_size))+5}}\t{file_modify_time} "
        if is_link:
            std_out += f"{file} -> {file_size}\n"
        else:
            std_out += f"{file}\n"
    return std_out
