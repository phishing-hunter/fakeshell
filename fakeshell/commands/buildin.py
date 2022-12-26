import optparse
import shlex
import os

def cmd_cd(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    if not args:
        os.chdir(os.environ.get("HOME", "/"))
        return std_out
    try:
        os.chdir(args[0])
    except FileNotFoundError:
        std_out += f"cd: {args[0]}: No such file or directory\n"
    return std_out


def cmd_pwd(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    std_out += os.getcwd() + "\n"
    return std_out


def cmd_export(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    if not args:
        std_out += "export: no arguments\n"
        return std_out
    for arg in args:
        if "=" not in arg:
            std_out += f"export: {arg}: not a valid identifier\n"
            continue
        key, value = arg.split("=", 1)
        os.environ[key] = value
    return std_out

def cmd_unset(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    if not args:
        std_out += "unset: no arguments\n"
        return std_out
    for arg in args:
        if arg in os.environ:
            del os.environ[arg]
    return std_out

def cmd_echo(cmd_args="", std_in=""):
    std_out = ""
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    for arg in args:
        if arg.startswith("$"):
            var_name = arg[1:]
            if var_name in os.environ and os.environ[var_name]:
                std_out += os.environ[var_name] + " "
            else:
                std_out += " "
        else:
            std_out += arg + " "
    std_out = std_out.rstrip() + "\n"
    return std_out

def cmd_env(cmd_args="", std_in=""):
    # 環境変数を表示する
    env_str = ""
    for key, value in os.environ.items():
        env_str += f"{key}={value}\n"
    return env_str
