import os
import sys
import pytest
import hashlib
sys.path.append('..')
from fakeshell.commands import md5sum

def test_cmd_md5sum():
    # ファイルが存在しない場合
    std_out = md5sum.cmd_md5sum("/tmp/not_exist.txt")
    assert std_out == "md5sum: /tmp/not_exist.txt: No such file or directory\n"

    # ファイルが存在する場合
    with open("/tmp/test.txt", "w") as f:
        f.write("test")
    std_out = md5sum.cmd_md5sum("/tmp/test.txt")
    expected_output = hashlib.md5(open("/tmp/test.txt", "rb").read()).hexdigest()
    assert std_out.split()[0] == expected_output

    # 複数のファイルを指定した場合
    std_out = md5sum.cmd_md5sum("/tmp/test.txt /tmp/not_exist.txt")
    expected_output = hashlib.md5(open("/tmp/test.txt", "rb").read()).hexdigest()
    assert std_out.split()[0] == expected_output
    assert std_out.split()[3] == "/tmp/not_exist.txt:"
    assert std_out.split()[4] == "No"

    os.remove("/tmp/test.txt")

