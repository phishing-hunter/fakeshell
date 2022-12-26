import os
import sys
import pytest
import tempfile
sys.path.append('..')
from fakeshell.commands import cmd_mkdir

def test_cmd_mkdir():
    # 通常のmkdir
    std_out = cmd_mkdir("/tmp/test_dir")
    assert std_out == ""
    assert os.path.exists("/tmp/test_dir")

    # ディレクトリがすでに存在する場合
    std_out = cmd_mkdir("/tmp/test_dir")
    assert std_out == "/tmp/test_dir: File exists\n"

    # パーミッションを指定した場合
    std_out = cmd_mkdir("-p /tmp/test_dir/test_dir2")
    assert std_out == ""
    assert os.path.exists("/tmp/test_dir/test_dir2")

    # パーミッションを指定して親ディレクトリが存在しない場合
    std_out = cmd_mkdir("-p /tmp/test_dir/test_dir3/test_dir4")
    assert std_out == ""
    assert os.path.exists("/tmp/test_dir/test_dir3/test_dir4")

    # 存在するファイル名を指定した場合
    fd, path = tempfile.mkstemp()
    os.close(fd)
    std_out = cmd_mkdir(path)
    assert std_out == f"{path}: File exists\n"

def teardown_module():
    os.rmdir("/tmp/test_dir/test_dir2")
    os.rmdir("/tmp/test_dir/test_dir3/test_dir4")
    os.rmdir("/tmp/test_dir/test_dir3")
    os.rmdir("/tmp/test_dir")

