import sys
import json
import requests
sys.path.append('..')
from fakeshell.commands import curl

def test_cmd_curl():
    # テスト用のURL
    url = "https://httpbin.org/get"
    # 期待される出力
    expected_output = json.loads(requests.get(url).text)
    # curlコマンドを実行
    output = json.loads(curl.cmd_curl(url))
    # レスポンスのボディが期待される出力と一致するか確認
    assert output["origin"] == expected_output['origin']
