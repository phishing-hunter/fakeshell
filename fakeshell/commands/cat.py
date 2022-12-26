import optparse
import shlex

def cmd_cat(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    if not args:
        std_out += std_in
        return std_out
    for file in args:
        try:
            with open(file, "r") as f:
                std_out += f.read()
        except FileNotFoundError:
            std_out += f"cat: {file}: No such file or directory\n"
    return std_out

