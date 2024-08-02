import re
import asyncio
import aiohttp

async def get_mail_io(client: aiohttp.ClientSession,
                      proxy: str = "") -> str:
    json = {
        'min_name_length': 10,
        'max_name_length': 10,
    }
    try:
        async with client.post("https://api.internal.temp-mail.io/api/v3/email/new",json=json,proxy=proxy) as response:
            res = await response.json()
            email = str(res["email"])
            print(email)
    except:
        print("<get_mail_error>")
        raise
    return email

async def get_code_io(client: aiohttp.ClientSession,
                      email: str,
                      proxy: str = "") -> str:
    for _ in range(5):
        try:
            await asyncio.sleep(3)
            async with client.get(f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages',proxy=proxy) as response:
                res = await response.json()
                text = res[0]["subject"]
                code = re.compile(r"\d+").findall(text)[0]
                print(code)
            return code
        except:
            continue
    print("<get_code_error>")
    raise