import optparse
import shlex
import base64

def cmd_base64(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    parser.add_option("-d", "--decode", action="store_true", default=False)
    parser.add_option("-w", "--wrap", type="int", default=76)
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    if options.decode:
        try:
            std_out = base64.b64decode(std_in).decode("utf-8")
        except Exception as e:
            std_out = str(e)
    else:
        std_out = base64.b64encode(std_in.encode("utf-8")).decode("utf-8")
        if options.wrap > 0:
            std_out = "\n".join(std_out[i:i+options.wrap] for i in range(0, len(std_out), options.wrap))
    return std_out

