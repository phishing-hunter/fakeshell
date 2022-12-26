import os
import optparse
import shlex

def cmd_chmod(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    parser.add_option("-R", "--recursive", action="store_true", default=False)
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    if len(args) < 2:
        std_out = "chmod: missing operand\n"
    else:
        try:
            # パーミッションを8進数形式で指定する場合はint関数で整数に変換する
            if options.recursive:
                for root, dirs, files in os.walk(args[-1]):
                    for file in files:
                        os.chmod(os.path.join(root, file), int(args[0], 8))
                    for d in dirs:
                        os.chmod(os.path.join(root, d), int(args[0], 8))
            else:
                os.chmod(args[-1], int(args[0], 8))
        except Exception as e:
            std_out = str(e)
    return std_out


