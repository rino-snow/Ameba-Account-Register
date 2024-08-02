# Ameba-Account-Register
非同期処理でamebaアカウントを自動生成するスクリプトをPythonで設計しました。reCAPTCHA Enterprise V2,V3の解決にも対応しています。config.jsonにて設定情報を入力したのちにregister.pyをダブルクリックするだけで実行します。

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
