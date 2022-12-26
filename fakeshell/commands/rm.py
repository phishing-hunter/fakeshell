import os
import optparse
import shlex
import shutil

def cmd_rm(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    parser.add_option("-f", action="store_true", dest="force", default=False)
    parser.add_option("-r", action="store_true", dest="recursive", default=False)
    options, args = parser.parse_args(cmd_args.split())

    # Remove specified files
    for path in args:
        if not os.path.exists(path):
            std_out = f"rm: {path}: No such file or directory\n"
            return std_out
        else:
            try:
                if options.recursive:
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except OSError as e:
                if options.force:
                    pass
                else:
                    std_out = e
    return std_out
