import os
import sys
import pytest
sys.path.append('..')
from fakeshell import commands

def test_cmd_chown():
    # テスト用のダミーファイルを作成する
    dummy = "dummy.txt"
    with open(dummy, "w") as f:
        f.write("dummy")
    # ファイルの所有者を変更する
    uid = os.stat(dummy).st_uid
    commands.cmd_chown(str(uid), "dummy.txt")
    # 所有者がrootであることを確認する
    assert os.stat("dummy.txt").st_uid == uid
    # ファイルを削除する
    os.remove("dummy.txt")

