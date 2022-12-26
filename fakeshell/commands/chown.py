import os
import grp
import pwd
import optparse
import shlex

def cmd_chown(cmd_args="", std_in=""):
    # パーサーを初期化する
    parser = optparse.OptionParser()
    # オプションを追加する
    parser.add_option("-R", action="store_true", dest="recursive", default=False)
    # 引数を解析する
    (options, args) = parser.parse_args(shlex.split(cmd_args))
    # 引数が2つあるか確認する
    if len(args) != 2:
        return "chown: Invalid arguments"
    # ユーザー名とグループ名を取得する
    user_group = args[0].split(":")
    if len(user_group) == 2:
        user, group = user_group
    else:
        user = user_group[0]
        group = user_group[0]
    # パスを取得する
    path = args[1]
    # パスが存在するか確認する
    if not os.path.exists(path):
        return "chown: Invalid path"
    # パスがディレクトリの場合、再帰的に処理する
    if os.path.isdir(path):
        # 再帰的に処理するか確認する
        if options.recursive:
            # ディレクトリ内のすべてのファイルを処理する
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.chown(file_path, pwd.getpwnam(user).pw_uid, grp.getgrnam(group).gr_gid)
        else:
            return "chown: Invalid argument"
    # パスがファイルの場合、処理する
    else:
        os.chown(path, pwd.getpwnam(user).pw_uid, grp.getgrnam(group).gr_gid)
    # 空の文字列を返す
    return ""
