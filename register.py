import aiohttp
import aiofiles
import asyncio
import solver
import tempmail_io
import json
import secrets
from typing import Optional, Any

class Client:
    def __init__(self) -> None:
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        with open("config.json") as f:
            config = json.load(f)
            self.file = str(config["file"])
            self.counts = int(config["counts"])
            self.aio_num = int(config["aio_num"])
            self.api_key = str(config["api_key"])
            self.bdayYear = str(config["bdayYear"])
            self.bdayMonth = str(config["bdayMonth"])
            self.bdayDay = str(config["bdayDay"])
            self.gender = str(config["gender"])
            self.password = str(config["password"])
            self.proxy = str(config["proxy"])
        with open("recaptcha_v2.json") as f:
            self.payload_v2 = {"clientKey":self.api_key,"task": json.load(f)}
        with open("recaptcha_v3.json") as f:
            self.payload_v3 = {"clientKey":self.api_key,"task": json.load(f)}

    async def __aenter__(self) -> Any:
        self.f = await aiofiles.open(self.file,"a")
        return self
    
    async def __aexit__(self,*args) -> None:
        await self.f.close()

    async def signup_start(self,
                           session: aiohttp.ClientSession) -> None:
        headers = {
            'Host': 'auth.user.ameba.jp',
            'User-Agent': self.userAgent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            # Requests doesn't support trailers
            # 'Te': 'trailers',
        }
        await session.get('https://auth.user.ameba.jp/signup/email', headers=headers, proxy=self.proxy)
        _csrf = session.cookie_jar.filter_cookies("https://auth.user.ameba.jp")["XSRF-TOKEN"].value
        return _csrf
    
    async def signup_v2(self,
                        session: aiohttp.ClientSession,
                        _csrf: str,
                        email: str,
                        reCaptchaToken: str) -> None:
        headers = {
            'Host': 'auth.user.ameba.jp',
            'User-Agent': self.userAgent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Content-Length': '2440',
            'Origin': 'https://auth.user.ameba.jp',
            'Referer': 'https://auth.user.ameba.jp/signup/email',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            # Requests doesn't support trailers
            # 'Te': 'trailers'
        }
        data = {
            '_csrf': _csrf,
            'emailAddress': email,
            'reCaptchaToken': reCaptchaToken,
            'g-recaptcha-response':reCaptchaToken
        }
        async with session.post('https://auth.user.ameba.jp/signup/email', headers=headers, data=data, proxy=self.proxy) as response:
            print(f"<{str(response.status)}-{len(response.history)} signup_v2>")
            if len(response.history) != 2:
                print("<v2_error>")
                raise

    async def signup_v3(self,
                        session: aiohttp.ClientSession,
                        _csrf: str,
                        email: str,
                        reCaptchaToken: str) -> Optional[bool]:
        headers = {
            'Host': 'auth.user.ameba.jp',
            'User-Agent': self.userAgent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Content-Length': '2440',
            'Origin': 'https://auth.user.ameba.jp',
            'Referer': 'https://auth.user.ameba.jp/signup/email',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            # Requests doesn't support trailers
        }
        data = {
            '_csrf': _csrf,
            'emailAddress': email,
            'reCaptchaToken': reCaptchaToken,
        }
        async with session.post('https://auth.user.ameba.jp/signup/email', headers=headers, data=data, proxy=self.proxy) as response:
            print(f"<{str(response.status)}-{len(response.history)} signup_v3>")
            if len(response.history) != 2:
                print("<v3_error>")
                return True
            else:
                return False
            
    async def verify_email(self,
                           session: aiohttp.ClientSession,
                           _csrf: str,
                           code: str) -> None:
        headers = {
            'Host': 'auth.user.ameba.jp',
            # 'Content-Length': '54',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://auth.user.ameba.jp',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.userAgent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://auth.user.ameba.jp/signup/email/verification',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
            'Priority': 'u=0, i'
        }
        data = {
            '_csrf': _csrf,
            'code': code,
        }
        async with session.post('https://auth.user.ameba.jp/signup/email/verification',headers=headers,data=data,proxy=self.proxy) as response:
            print(f"<{str(response.status)} verify_email>")

    async def get_ameba_id(self,
                           session: aiohttp.ClientSession) -> str:
        ameba_id = secrets.token_hex(5)
        headers = {
            'Host': 'auth.user.ameba.jp',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': self.userAgent,
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://auth.user.ameba.jp/signup/email/ameba-id',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
            'Priority': 'u=1, i'
        }
        async with session.get(f'https://auth.user.ameba.jp/api/available-ameba-id/{ameba_id}',headers=headers,proxy=self.proxy) as response:
            print(f"<{str(response.status)} get_ameba_id>")
        return ameba_id
    
    async def signup_finish(self,
                            session: aiohttp.ClientSession,
                            _csrf: str,
                            ameba_id: str) -> str:
        headers = {
            'Host': 'auth.user.ameba.jp',
            # 'Content-Length': '151',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://auth.user.ameba.jp',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.userAgent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://auth.user.ameba.jp/signup/email/profile',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
            'Priority': 'u=0, i',
            # 'Cookie': '_ga_FNC8BLTBPL=GS1.1.1721412006.1.0.1721412008.0.0.0; XSRF-TOKEN=9f75348b-df0b-4972-9fa7-82baad72942f; P=a15ac64a-320a-4567-ad77-3ec279728738; __utma=257183131.465698129.1721412007.1721412393.1721412393.1; __utmc=257183131; __utmz=257183131.1721412393.1.1.utmcsr=ameblo.jp|utmccn=(referral)|utmcmd=referral|utmcct=/; __gads=ID=5ec4ed5e9a56847e:T=1721412040:RT=1721490967:S=ALNI_MZ3l2bq8oPSkyeder0eBnFjoDYHkg; __gpi=UID=00000e9c1fa17de0:T=1721412040:RT=1721490967:S=ALNI_MbxQAuocv-PQhhsLrHub244PuWAlw; __eoi=ID=9fb64807825ceb41:T=1721412040:RT=1721490967:S=AA-AfjYHc9PXu3h5J411XxGEEsJQ; _ga_WVMM60SGEG=GS1.1.1721490964.2.1.1721490979.0.0.0; _clck=cpv33v%7C2%7Cfnm%7C0%7C1661; FCNEC=%5B%5B%22AKsRol-MX6W-J3JyiUPjMDHwk-vULUQM2xcsLnN-S8udvdJsZfDoSnTxMuyJomzV5gCGc9XBJIfhGbcScIZAu57l2Burq1rHjQ2pX75CA40HPu8sxkI_84r0HXI4F4mHezQvPKPbqisb0QkS8ixZYma2zH7XfdrWpA%3D%3D%22%5D%5D; _ga_7BCS07G3H9=GS1.1.1721494529.2.1.1721495993.0.0.0; _ga_3028DJK3ZG=GS1.1.1721494529.2.1.1721495993.0.0.0; _gid=GA1.2.902801996.1722028736; user_session1=YjhkNGQwY2ItOGM0Ni00YWFkLTkwZmQtYjdiNjI1MmY1Yzc4; _ga=GA1.1.465698129.1721412007; _ga_H1X8917JB8=GS1.1.1722028755.4.1.1722029904.0.0.0',
        }
        data = {
            '_csrf': _csrf,
            'amebaId': ameba_id,
            'showPassword': 'on',
            'password': self.password,
            'bdayYear': self.bdayYear,
            'bdayMonth': self.bdayMonth,
            'bdayDay': self.bdayDay,
            'gender': self.gender,
        }
        async with session.post('https://auth.user.ameba.jp/signup/email/form',headers=headers, data=data, proxy=self.proxy) as response:
            print(f"<{str(response.status)} signup_finish>")
        auth_token = session.cookie_jar.filter_cookies("https://auth.user.ameba.jp")["asauth"].value
        return auth_token
    
    async def get_ameblo_token(self,
                               session: aiohttp.ClientSession) -> str:
        headers = {
            'Host': 'blog-embed.ameba.jp',
            'User-Agent': self.userAgent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'X-From': 'https://blog-embed.ameba.jp/embed/api',
            'Origin': 'https://blog-embed.ameba.jp',
            'Referer': 'https://blog-embed.ameba.jp/embed/api',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            # 'Content-Length': '0',
            # Requests doesn't support trailers
            # 'Te': 'trailers',
        }
        async with session.post('https://blog-embed.ameba.jp/_api/ameblo/token/generate', headers=headers, proxy=self.proxy) as response:
            response_json = await response.json()
        ameblo_token = response_json["data"]["ameblo_token"]
        return ameblo_token
    
    async def check_ameblo_token(self,
                                 session: aiohttp.ClientSession,
                                 ameblo_token: str) -> None:
        session.cookie_jar.clear()
        headers = {
            'Host': 'blog-embed.ameba.jp',
            'User-Agent': self.userAgent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'X-From': 'https://blog-embed.ameba.jp/embed/api',
            # 'Content-Length': '118',
            'Origin': 'https://blog-embed.ameba.jp',
            'Referer': 'https://blog-embed.ameba.jp/embed/api',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            # Requests doesn't support trailers
            # 'Te': 'trailers',
        }
        json_data = {
            'amebloToken': ameblo_token,
        }
        async with session.post('https://blog-embed.ameba.jp/_api/ameblo/token/check', headers=headers, json=json_data, proxy=self.proxy) as response:
            response_json = await response.json()
        if str(response_json["data"]["member"]) != '1':
            print("<check_failed>")
            raise
    
    async def task(self) -> None:
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector,raise_for_status=True) as session:
                _csrf = await self.signup_start(session)
                email = await tempmail_io.get_mail_io(session,self.proxy)
                reCaptchaToken = await solver.solver(session,self.payload_v3,proxy=self.proxy)
                flag = await self.signup_v3(session,_csrf,email,reCaptchaToken)
                if flag:
                    reCaptchaToken = await solver.solver(session,self.payload_v2,proxy=self.proxy)
                    await self.signup_v2(session,_csrf,email,reCaptchaToken)
                code = await tempmail_io.get_code_io(session,email,self.proxy)
                await self.verify_email(session,_csrf,code)
                ameba_id = await self.get_ameba_id(session)
                auth_token = await self.signup_finish(session,_csrf,ameba_id)
                ameblo_token = await self.get_ameblo_token(session)
                await self.check_ameblo_token(session,ameblo_token)
                account = f"{email}:{self.password}:{ameba_id}:{auth_token}:{ameblo_token}\n"
                await self.f.write(account)
                print("<success>")
        except:
            return
    
    async def register(self) -> None:
        q = self.counts // self.aio_num
        r = self.counts % self.aio_num
        for _ in range(q):
            tasks = [self.task() for _ in range(self.aio_num)]
            await asyncio.gather(*tasks)
        if r != 0:
            tasks = [self.task() for _ in range(r)]
            await asyncio.gather(*tasks)

async def main():
    async with Client() as client:
        await client.register()

if __name__ == "__main__":
    asyncio.run(main())
