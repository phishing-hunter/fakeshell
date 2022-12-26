import optparse
import shlex

def cmd_df(cmd_args="", std_in=""):
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args(shlex.split(cmd_args))

    if "--help" in cmd_args:
        return """
df - report file system disk space usage

Synopsis:
  df [OPTION]... [FILE]...

Description:
  Show information about the file system on which each FILE resides, or all file systems by default.

Options:
  -h, --human-readable  print sizes in human readable format (e.g., 1K 234M 2G)
  --help                display this help and exit
"""

    std_out = """
Filesystem                        1K-blocks     Used Available Use% Mounted on
tmpfs                               1638556     1336   1637220   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv 101590008 24889260  71494120  26% /
tmpfs                               8192764        0   8192764   0% /dev/shm
tmpfs                                  5120        0      5120   0% /run/lock
/dev/sda2                           1992552   252624   1618688  14% /boot
/dev/sdb1                         514936064 67506840 421198492  14% /var/lib/docker
tmpfs                               1638552        4   1638548   1% /run/user/1000
"""

    return std_out
