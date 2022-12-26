import os
import sys
import stat
import shutil
from stat import S_IMODE
sys.path.append('..')
from fakeshell.commands import chmod

def test_chmod():
    # テスト用ファイルを作成する
    with open('/tmp/test.txt', 'w') as f:
        f.write('test')
    # パーミッションを変更する
    chmod.cmd_chmod('777 /tmp/test.txt')
    # パーミッションが正しく設定されたかを確認する
    assert oct(os.stat('/tmp/test.txt').st_mode)[-3:] == '777'
    # テスト用ファイルを削除する
    os.remove('/tmp/test.txt')

def test_cmd_chmod_R():
    # テスト用のディレクトリを作成
    os.makedirs('/tmp/chmod_test', exist_ok=True)
    open('/tmp/chmod_test/file1.txt', 'w').close()
    open('/tmp/chmod_test/file2.txt', 'w').close()
    os.mkdir('/tmp/chmod_test/subdir')
    open('/tmp/chmod_test/subdir/file3.txt', 'w').close()
    # 権限を設定
    assert chmod.cmd_chmod(cmd_args='777 -R /tmp/chmod_test') == ''
    # 権限を確認
    for path in ['/tmp/chmod_test/file1.txt', '/tmp/chmod_test/file2.txt', '/tmp/chmod_test/subdir', '/tmp/chmod_test/subdir/file3.txt']:
        assert oct(stat.S_IMODE(os.lstat(path).st_mode)) == '0o777'
    # テスト用のディレクトリを削除
    shutil.rmtree('/tmp/chmod_test')

