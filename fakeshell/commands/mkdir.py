import os
import optparse
import shlex

def cmd_mkdir(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    parser.add_option("-p", "--parents", action="store_true", default=False)
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    if len(args) < 1:
        std_out = "mkdir: missing operand\n"
    else:
        try:
            if options.parents:
                os.makedirs(args[0])
            else:
                os.mkdir(args[0])
        except FileExistsError:
            std_out = f"{args[0]}: File exists\n"
        except Exception as e:
            std_out = str(e)
    return std_out

