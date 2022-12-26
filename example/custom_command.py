from fakeshell.shell import FakeShell
from fakeshell.interpreter import register_command

# コマンドを定義する
def hello(args="", stdin=""):
    stdout = f"Hello, {args}"
    return stdout

# コマンドを登録する
register_command("hello", hello)

# コマンドを実行する
fake_sh = FakeShell()
for result in fake_sh.run_command("hello John"):
    print(result)
fake_sh.stop()
