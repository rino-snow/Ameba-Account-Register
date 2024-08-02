# Ameba-Account-Register
非同期処理でamebaアカウントを自動生成するスクリプトをPythonで設計しました。reCAPTCHA Enterprise V2,V3の解決にも対応しています。config.jsonにて設定情報を入力したのちにregister.pyをダブルクリックするだけで実行します。

# Example
```Python:qiita.py
import asyncio
from register import Client

async def main():
  async with Client() as client:
    client.register()
if __name__ == "__main__":
  asyncio.run(main())
```
