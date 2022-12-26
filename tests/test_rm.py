import os
import sys
import shlex
import pytest
import optparse
sys.path.append('..')
from fakeshell import commands

def test_cmd_rm():
    # テスト用のファイルを作成する
    with open("/tmp/test_file", "w") as f:
        f.write("test content")
    assert os.path.exists("/tmp/test_file")

    # ファイルを削除する
    assert commands.cmd_rm("/tmp/test_file") == ""
    assert not os.path.exists("/tmp/test_file")

    # 存在しないファイルを削除しようとする
    assert commands.cmd_rm("not_exist_file") == "rm: not_exist_file: No such file or directory\n"

    # ディレクトリを削除する
    #os.makedirs("/tmp/test_dir", exist_ok=True)
    #assert os.path.exists("test_dir")
    #assert commands.cmd_rm("test_dir") == ""
    #assert not os.path.exists("test_dir")

