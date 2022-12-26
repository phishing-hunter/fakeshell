import shlex
import logging
import optparse
from . import commands

def register_command(name, func):
    """
    独自コマンドをfake_sh.run_commandで実行できるように登録します。

    Parameters
    ----------
    name : str
        コマンド名
    func : Callable
        コマンドを実行する関数
    """
    setattr(commands, f"cmd_{name}", func)

def read_file(filename):
    content = ""
    with open(filename, "r") as f:
        content = f.read()
    return content

def create_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)

def run_command(command, std_in=""):
    # | で区切って、各コマンドを分割する
    cmds = command.split("|")
    # 結果を格納する変数を初期化する
    result = std_in
    for cmd in cmds:
        # コマンドの文字列をスペースで分割する
        cmd_parts = cmd.split()
        # コマンド名を取得する
        cmd_name = cmd_parts[0]
        # コマンドの引数を取得する
        cmd_args = cmd_parts[1:]
        # < を含む場合は、それより左側のコマンドを実行する
        run_func = True
        func_args = ""
        if "<" in cmd_args:
            # < の位置を取得する
            input_redirection_index = cmd_args.index("<")
            func_args = " ".join(cmd_parts[:input_redirection_index+1])
            for input_redirection_index, item in enumerate(cmd_args):
                # < の右側のファイル名を取得する
                if item == '<':
                    input_filename = cmd_args[input_redirection_index + 1]
                    # ファイルから入力を読み込む
                    result += read_file(input_filename)
            # < の左側のコマンドを実行する
            result = run_command(func_args, result)
            run_func = False
        # > を含む場合は、それより右側のコマンドを実行する
        if ">" in cmd_args:
            # > の位置を取得する
            output_redirection_index = cmd_args.index(">")
            func_args = " ".join(cmd_parts[:output_redirection_index+1])
            # > の左側のコマンドを実行する
            result = run_command(func_args, result)
            for output_redirection_index, item in enumerate(cmd_args):
                # > の右側のファイル名を取得する
                if item == '>':
                    # ファイルに出力を書き込む
                    output_filename = cmd_args[output_redirection_index + 1]
                    create_file(output_filename, result)
                    result = ""
            run_func = False
        # それ以外の場合は、コマンドを実行する
        if run_func:
            # 定義済みの関数を呼び出す
            function_name = "cmd_" + cmd_name
            try:
                cmd_function = getattr(globals()["commands"], function_name)
                result = cmd_function(" ".join(cmd_args), result)
            except:
                result = f"command not found: {cmd_name}\n"
                logging.exception(result)
    return result
