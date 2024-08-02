# Ameba-Account-Register
非同期処理でamebaアカウントを自動生成するスクリプトをPythonで設計しました。reCAPTCHA Enterprise V2,V3の解決にも対応しています。config.jsonにて設定情報を入力したのちにregister.pyをダブルクリックするだけで実行します。httpリクエストにはaiohttp、ファイル出力にはaiofilesを使用しております。

# Example
```Python:qiita.py
import asyncio
from register import Client

async def main():
    async with Client() as client:
        await client.register()

if __name__ == "__main__":
    asyncio.run(main())
```

# config.json
```Python:qiita.json
{
    "file": "accounts.txt",
    "counts": 50,
    "aio_num": 30,
    "bdayYear": 2000,
    "bdayMonth": 4,
    "bdayDay": 1,
    "gender": "male",
    "password": "@password321",
    "api_key": "CAP-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "proxy": "http://USERNAME:PASSWORD@XXXXXXproxy.com:30000"
}
```
countsには合計の試行回数を、aio_numには非同期処理でgatherする最大の並列数を数値で入力してください。\n
fileで指定したパスにアカウントが出力されます。
