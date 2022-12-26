import os
import pytest
import sys
sys.path.append('..')

from fakeshell.commands import buildin

def test_cmd_echo():
    assert buildin.cmd_echo(cmd_args="test", std_in="") == "test\n"
    assert buildin.cmd_echo(cmd_args="$VARNAME", std_in="") == "\n"
    assert buildin.cmd_echo(cmd_args="test1 test2", std_in="") == "test1 test2\n"

def test_cmd_cd():
    current_dir = os.getcwd()
    assert buildin.cmd_cd(cmd_args="/tmp", std_in="") == ""
    assert os.getcwd() == "/tmp" or os.getcwd() == "/private/tmp"
    buildin.cmd_cd(cmd_args=current_dir, std_in="")

def test_cmd_pwd():
    assert buildin.cmd_pwd(cmd_args="", std_in="") == os.getcwd() + "\n"

def test_cmd_export():
    assert "VARNAME" not in os.environ
    assert buildin.cmd_export(cmd_args="VARNAME=value", std_in="") == ""
    assert os.environ["VARNAME"] == "value"

def test_cmd_unset():
    os.environ["VARNAME"] = "value"
    assert "VARNAME" in os.environ
    assert buildin.cmd_unset(cmd_args="VARNAME", std_in="") == ""
    assert "VARNAME" not in os.environ

