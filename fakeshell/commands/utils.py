import optparse
import shlex
import random
from datetime import datetime, timedelta

def cmd_last(cmd_args="", std_in=""):
    # 現在時刻を取得
    now = datetime.now()

    # 現在から過去30日分のログを生成する
    logs = []
    for i in range(30):
        # ランダムなログイン時刻とログアウト時刻を生成
        login_time = now - timedelta(days=i, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        logout_time = login_time + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))

        # ログイン時刻が現在より未来の場合はログアウト時刻も未来にする
        if login_time > now:
            logout_time = now + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))

        # ログイン時刻とログアウト時刻を整形
        login_time_str = login_time.strftime("%a %b %d %H:%M")
        logout_time_str = logout_time.strftime("%H:%M")

        # ログイン時刻が現在より未来の場合はstill logged inとする
        if login_time > now:
            logout_time_str = "still logged in"

        # ログを追加
        logs.append("tatsui   pts/0        192.168.1.65    {} - {}  ({})"
                    .format(login_time_str, logout_time_str, (logout_time - login_time)))

    # 生成したログを文字列として連結して出力
    return "\n".join(logs) + "\n"


# ダミーのコマンド名を格納する配列
commands = ["systemd", "kthreadd", "rcu_gp", "rcu_par_gp", "netns", "kworker/0:0H-kblockd", "mm_percpu_wq"]

def cmd_ps(cmd_args="", std_in=""):
    cmd_args = shlex.split(cmd_args)
    if "--help" in cmd_args or "-h" in cmd_args:
        return """
ps - report a snapshot of the current processes
Synopsis:
  ps [OPTION]...
Description:
  Report a snapshot of the current processes.
Options:
  -e, --all           select all processes
  -a, --all-with-term include processes without a controlling terminal
  -h, --no-header     omit header
  --help              display this help and exit
"""

    # ヘッダ行を出力する
    std_out = "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\n"

    # 現在時刻を取得する
    now = datetime.now()

    # コマンド名を出力する
    for i, command in enumerate(commands):
        # PIDをインクリメントする
        pid = i + 1

        # STARTを現在時刻から1時間前にする
        start = now - timedelta(hours=1)

        # TIMEを1~10分の範囲でランダムに生成する
        time = timedelta(minutes=random.randint(1, 10))

        std_out += f"root       {pid:<8}  0.0  0.0      0     0 ?        I<   {start:%b%d}   {time} {command}\n"

    return std_out

