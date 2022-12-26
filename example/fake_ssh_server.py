import os
import time
import paramiko
import threading
import traceback
from socketserver import ThreadingTCPServer, BaseRequestHandler
from fakeshell.shell import FakeShell


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
        sh = FakeShell("/")
        ps1 = self._get_ps1()
        banner = f"Hello FakeShell\n\n{ps1}"
        stdout.write(banner)
        for command in stdin:
            if command == "\n":
                stdout.write(ps1)
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
            t.add_server_key(paramiko.RSAKey.from_private_key_file("server.key"))
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
