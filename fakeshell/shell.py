import os
from .interpreter import run_command
from pyfakefs import fake_filesystem_unittest

def replace_env_variables(command: str) -> str:
    # 引数の文字列を改行で分割して、各行に対して処理を行う
    lines = command.split("\n")
    processed_lines = []
    for line in lines:
        # 各行内の文字列を空白文字で分割する
        words = line.split()
        processed_words = []
        for word in words:
            if word.startswith("$"):
                # 環境変数名を取り出す
                env_name = word[1:]
                # 環境変数を取得する
                env_value = os.environ.get(env_name, "")
                processed_words.append(env_value)
            else:
                processed_words.append(word)
        # 各行を再び結合する
        processed_lines.append(" ".join(processed_words))
    # 各行を改行で結合する
    return "\n".join(processed_lines)


class FakeShell:
    def __init__(self, cwd="/tmp", home="/", exclude_dir=["/proc", "/dev"], fakefs=True):
        self._exclude_dir = exclude_dir
        self._fakefs = fakefs
        if self._fakefs:
            self.start()
        # ワーキングディレクトリをセットする
        os.environ["HOME"] = home
        os.chdir(cwd)

    def start(self):
        rootfs = os.listdir("/")
        # 仮想ファイルシステムを作成する
        self.patcher = fake_filesystem_unittest.Patcher()
        self.patcher.setUp()
        self.fs = self.patcher.fs
        # ホスト側のファイルシステムをコピーする
        for _dir in rootfs:
            try:
                _dir = os.path.join("/", _dir)
                if not _dir in self._exclude_dir:
                    self.fs.add_real_directory(_dir)
            except: pass

    def run_command(self, command):
        for cmd in command.split(";"):
            cmd = replace_env_variables(cmd)
            yield run_command(cmd)

    def stop(self):
        if self._fakefs:
            # 仮想環境の終了
            self.patcher.tearDown()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
