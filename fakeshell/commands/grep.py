import optparse
import shlex

def parse_grep_args(cmd_args):
    """
    grepコマンドの引数をパースする関数。
    :param cmd_args: str, grepコマンドの引数
    :return: tuple(options, pattern, files)
    """
    parser = optparse.OptionParser()
    parser.add_option("-i", action="store_true", dest="ignore_case", default=False, help="Ignore case distinctions in PATTERN")
    parser.add_option("-n", action="store_true", dest="line_number", default=False, help="Prefix each line of output with the 1-based line number within its input file")
    parser.add_option("-v", action="store_true", dest="invert_match", default=False, help="Invert the sense of matching, to select non-matching lines")
    options, args = parser.parse_args(cmd_args.split())
    if len(args) == 0:
        return (options, "", [])
    elif len(args) == 1:
        return (options, args[0], [])
    else:
        return (options, args[0], args[1:])

def read_file(file_name):
    """
    ファイルを読み込んで、その中身を返す関数。
    :param file_name: str, ファイル名
    :return: list[str], ファイルの中身を行ごとに要素としたリスト
    """
    with open(file_name, "r") as f:
        return f.readlines()

def cmd_grep(cmd_args="", std_in=""):
    """
    grepコマンドを実行する関数。
    :param cmd_args: str, grepコマンドの引数
    :param std_in: str, 標準入力
    :return: str, grepコマンドの実行結果
    """
    options, pattern, files = parse_grep_args(cmd_args)
    if not files:
        files = ["-"]
    result = []
    for file in files:
        if file == "-":
            lines = std_in.split("\n")
        else:
            lines = read_file(file)
        for line in lines:
            if options.ignore_case:
                line = line.lower()
                pattern = pattern.lower()
            if pattern in line:
                if not options.invert_match:
                    result.append(line)
            else:
                if options.invert_match:
                    result.append(line)
    return "\n".join(result)
