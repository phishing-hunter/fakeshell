import optparse
import shlex

def cmd_md5sum(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    if not args:
        std_out += std_in
        return std_out
    import hashlib
    for file in args:
        try:
            with open(file, "rb") as f:
                data = f.read()
                std_out += f"{hashlib.md5(data).hexdigest()}  {file}\n"
        except FileNotFoundError:
            std_out += f"md5sum: {file}: No such file or directory\n"
    return std_out

