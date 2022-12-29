import os
import time
import shlex
import random
import paramiko
import threading
import traceback
from socketserver import ThreadingTCPServer, BaseRequestHandler
from fakeshell.shell import FakeShell
from fakeshell.interpreter import register_command

def cmd_nmap(cmd_args="", std_in=""):
    cmd_args = shlex.split(cmd_args)
    if "--help" in cmd_args or "-h" in cmd_args:
        return """
nmap - Network exploration tool and security/port scanner
Synopsis:
  nmap [OPTION]... [TARGET]...
Description:
  Scan the TARGET hosts to determine the service and version information.
Options:
  -sV              probe open ports to determine service/version info
  -p [portlist]    specify port range to scan
  --top-ports num  scan the top num most common ports
  -oA [file]       output scan results in the specified file in three formats
  --help           display this help and exit
"""
    std_out = "ダミーの結果出力"
    return std_out


def cmd_exploit(cmd_args="", std_in=""):
    cmd_args = shlex.split(cmd_args)
    if "--help" in cmd_args or "-h" in cmd_args:
        return """
exploit - execute an exploit
Synopsis:
  exploit [OPTION]... [EXPLOIT_NAME]
Description:
  Execute the specified exploit.
Options:
  --help                display this help and exit
"""

    if len(cmd_args) < 1:
        return "Error: specify exploit name"

    exploit_name = cmd_args[0]

    # ダミーのログ追記
    with open("/var/log/syslog", "a") as f:
        f.write("Executed exploit: {}\n".format(exploit_name))

    # 攻撃が成功する確率は50%
    if random.randint(0, 1) == 0:
        # バックドアを設置する
        with open("/tmp/backdoor.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'I am a backdoor'\n")
        return "Exploit success"
    return "Exploit failed"

register_command("nmap", cmd_nmap)
register_command("exploit", cmd_exploit)

class Server(paramiko.server.ServerInterface):
    def __init__(self):
        super().__init__()
        self.event = threading.Event()
        self.username = ""

    def check_auth_password(self, username, password):
        if username == "root" and password == "password":
            self.username = username
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        # コマンド実行用のスレッドを作成する
        stdout = channel.makefile("w")
        stdin = channel.makefile("r")
        t = threading.Thread(target=self._execute_command, args=(stdin, stdout, self.event), daemon=True).start()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return False

    def _get_ps1(self):
        cwd = os.getcwd()
        cwd = "~" if cwd == os.environ["HOME"] else cwd
        ps1 = f"[{self.username}@localhost {cwd}]# "
        return ps1

    def _execute_command(self, stdin, stdout, event):
        sh = FakeShell("/", exclude_dir=["/scripts", "/dev"])
        ps1 = self._get_ps1()
        banner = f"Hello FakeShell\n\n{ps1}"
        stdout.write(banner)
        for command in stdin:
            if command == "\n":
                stdout.write(self._get_ps1())
                continue
            if command in ["quit\n", "exit\n"]:
                stdout.write("")
                break
            for cmd_out in sh.run_command(command):
                stdout.write(cmd_out)
            stdout.write(self._get_ps1())
        event.set()
        sh.stop()

class SshHandler(BaseRequestHandler):
    def handle(self):
        connection = self.request
        try:
            t = paramiko.Transport(connection)
            t.load_server_moduli()
            t.add_server_key(paramiko.RSAKey.from_private_key_file("/tmp/server.key"))
            server = Server()
            t.start_server(server=server)
            t.join()

        except Exception as err:
            print(traceback.format_exc())

        try:
            t.close()
        except:
            pass
        connection.close()


ThreadingTCPServer.allow_reuse_address = True
with ThreadingTCPServer(("", 2222), SshHandler) as server:
    server.serve_forever()
