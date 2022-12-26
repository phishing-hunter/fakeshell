import optparse
import shlex
import os
import time
import pwd
import psutil
import humanfriendly

def print_df_line(device, mount_point, file_system_type, total, used, free, percent, options):
    std_out = ""
    if options.human_readable:
        # Print sizes in human-readable format (e.g., 1K 234M 2G)
        total_str = f"{humanfriendly.format_size(total)}"
        used_str = f"{humanfriendly.format_size(used)}"
        free_str = f"{humanfriendly.format_size(free)}"
    else:
        # Print sizes in bytes
        total_str = f"{total}"
        used_str = f"{used}"
        free_str = f"{free}"
    # Align the columns by padding with spaces
    device_str = f"{device:<40}"
    total_str = f"{total_str:>10}"
    used_str = f"{used_str:>10}"
    free_str = f"{free_str:>10}"
    percent_str = f"{percent:>3}"
    std_out += f"{device_str}\t{total_str}\t{used_str}\t{free_str}\t{percent_str}%\t{mount_point}\n"
    return std_out


def cmd_df(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    # Add options to the parser
    parser.add_option("-a", "--all", action="store_true", dest="all", default=False, help="show all file systems")
    parser.add_option("-H", "--human-readable", action="store_true", dest="human_readable", default=False, help="print sizes in human-readable format")
    # Parse the command line arguments
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    # Get the list of file systems and their usage
    file_systems = psutil.disk_partitions(options.all)
    # Print the header
    if options.human_readable:
        std_out += "Filesystem\tSize\t\tUsed\t\tAvail\t\tUse%\tMounted on\n"
    else:
        std_out += "Filesystem\t1K-blocks\t\tUsed\t\tAvailable\t\tUse%\tMounted on\n"
    # Print the file system details
    for file_system in file_systems:
        device = file_system.device
        mount_point = file_system.mountpoint
        file_system_type = file_system.fstype
        try:
            usage = psutil.disk_usage(mount_point)
        except OSError:
            # Skip file systems that cannot be accessed
            continue
        total = usage.total
        used = usage.used
        free = usage.free
        percent = usage.percent
        if options.human_readable:
            total_size = humanfriendly.format_size(total, binary=True)
            used_size = humanfriendly.format_size(used, binary=True)
            free_size = humanfriendly.format_size(free, binary=True)
            std_out += f"{device}\t{total_size}\t{used_size}\t{free_size}\t{percent}%\t{mount_point}\n"
        else:
            std_out += f"{device}\t{total}\t{used}\t{free}\t{percent}%\t{mount_point}\n"
    return std_out
