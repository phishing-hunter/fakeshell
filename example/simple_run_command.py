from fakeshell.shell import FakeShell
with FakeShell("/tmp") as sh:
    commands = ["ls -l /", "cd /opt", "pwd", "ls -l"]
    for command in commands:
        for stdout in sh.run_command(command):
            print(stdout)
