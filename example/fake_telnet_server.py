import os
from fakeshell.shell import FakeShell
from socketserver import TCPServer, StreamRequestHandler

def _get_ps1():
    cwd = os.getcwd()
    cwd = "~" if cwd == os.environ["HOME"] else cwd
    ps1 = f"[root@localhost {cwd}]# "
    return ps1

class Handler(StreamRequestHandler):
    def handle(self):
        stdin = self.request.makefile('r', encoding='utf-8')
        stdout = self.request.makefile('w', encoding='utf-8')

        command = ""
        with FakeShell(cwd="/", exclude_dir=["/scripts", "/dev"]) as sh:
            ps1 = _get_ps1()
            banner = f"Hello FakeShell\n\n{ps1}"
            stdout.write(banner)
            stdout.flush()
            for command in stdin:
                if command == "\n":
                    stdout.write(_get_ps1())
                    stdout.flush()
                    continue
                if command in ["quit\n", "exit\n"]:
                    stdout.write("")
                    stdout.flush()
                    break
                for cmd_out in sh.run_command(command):
                    stdout.write(cmd_out)
                    stdout.flush()
                stdout.write(_get_ps1())
                stdout.flush()

        stdin.close()
        stdout.close()
 
TCPServer(('', 2323), Handler).serve_forever()
