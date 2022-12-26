import sys
import pytest
import base64

sys.path.append('..')
from fakeshell.commands import b64

def test_cmd_b64_encode():
    assert b64.cmd_base64(cmd_args="", std_in="test") == base64.b64encode("test".encode()).decode()

def test_cmd_b64_decode():
    assert b64.cmd_base64(cmd_args="-d", std_in=base64.b64encode("test".encode()).decode()) == "test"

def test_cmd_b64_invalid_option():
    with pytest.raises(SystemExit):
        b64.cmd_base64(cmd_args="--invalid-option", std_in="")
