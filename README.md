# Fakeshell

Fakeshellは仮想的なシェル環境を提供するパッケージです。  
標準で提供されているLinuxコマンドの代わりに、Pythonで実装されたコマンドを実行できます。  
fakeshellを使用することで、Linuxシステムのようなサンドボックス環境を再現することができます。  
[![asciicast](https://asciinema.org/a/549416.svg)](https://asciinema.org/a/549416)

## インストール方法
pipを使ってfakeshellをインストールできます。

```bash
$ pip install fakeshell
```

## 使い方
fakeshellを使うには、PythonからFakeShellクラスをインポートしてインスタンスを作成する必要があります。  
FakeShellクラスは、次のように作成できます。  

```python
from fakeshell.shell import FakeShell
fake_sh = FakeShell(cwd="/tmp")
```

FakeShellクラスは、次のようなメソッドを提供しています。

run_command(command: str) -> Generator[str]:
FakeShellクラスのrun_commandメソッドを使用すると、指定したコマンドを実行することができます。
コマンドを実行すると、実行結果のジェネレータが返されます。

```python
for result in fake_sh.run_command("ls -l > hoge.txt"):
    print(result)
```

stopメソッドを呼び出すとファイルシステムへの書き込み内容を元の状態に戻します。
```python
fake_sh.stop()
```

以下のように記述することでstopメソッドを省略することもできます。
```python
with FakeShell(cwd="/tmp") as fake_sh:
    for result in fake_sh.run_command("ls -l > hoge.txt"):
        print(result)
```

run_commandメソッドによって実行される関数には、以下のような仮想のファイルシステムが提供されます。  
仮想ファイルシステム上ではホストマシンのファイルシステムと同じ内容が参照されますが、  
ファイルシステムへの読み書きはホストマシンへは影響しません。

* ファイルの読み書き
* ディレクトリの作成、削除
* ファイル、ディレクトリのパーミッション変更
* シンボリックリンクの作成、削除
* ファイルシステムの使用率の確認

## 独自コマンドを実装する
独自コマンドを実装するには、register_commandを使って関数を登録します。

```python
from fakeshell.interpreter import register_command

def hello(args="", stdin=""):
    stdout = f"Hello, {args}"
    return stdout

register_command("hello", hello)
```

登録したコマンドは、以下のようにして実行できます。

```python
for result in fake_sh.run_command("hello John"):
    print(result)
```

## FakeSSHサーバを構築する
```
$ docker pull ghcr.io/phishing-hunter/fakeshell:main
$ docker run --rm -it -d -p 2222:2222 ghcr.io/phishing-hunter/fakeshell:main
$ ssh root@localhost -p 2222 # root/password
```
