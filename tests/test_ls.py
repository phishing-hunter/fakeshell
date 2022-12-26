import os
import pytest
import sys
sys.path.append('..')
from fakeshell.commands import cmd_ls

def test_cmd_ls(tmpdir):
    # テストで使用するファイルを作成する
    test_dir = tmpdir.mkdir("test_dir")
    test_file1 = test_dir.join("file1.txt")
    test_file1.write("test")
    test_file2 = test_dir.join("file2.txt")
    test_file2.write("test")

    # テスト対象関数を実行し、出力を取得する
    output = cmd_ls(std_in="", cmd_args=f"{test_dir}")

    # 出力を検証する
    assert output == "file1.txt  file2.txt  \n"
