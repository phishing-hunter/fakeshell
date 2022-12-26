import sys
sys.path.append('..')

import pytest
import os

from fakeshell.commands import cat

def test_cmd_cat():
    # Test reading file
    with open("/tmp/test.txt", "w") as f:
        f.write("test\n")
    assert cat.cmd_cat(cmd_args="/tmp/test.txt", std_in="") == "test\n"
    os.remove("/tmp/test.txt")

    # Test reading from stdin
    assert cat.cmd_cat(cmd_args="", std_in="test") == "test"

    # Test file not found error
    not_exist_file_path = '/tmp/not_exist.txt'
    expected_output = f"cat: {not_exist_file_path}: No such file or directory\n"
    assert cat.cmd_cat(cmd_args=not_exist_file_path, std_in="") == expected_output
