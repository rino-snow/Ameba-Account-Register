import aiohttp
import secrets
from typing import Optional

class BaseClient:
    def __init__(self,
                 userAgent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                 proxy: str = "") -> None:
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False),raise_for_status=True)
        self.userAgent = userAgent
        self.proxy = proxy

    async def __aenter__(self):
        return self
    
    async def __aexit__(self,*args) -> None:
        await self.session.close()

    async def signup_start(self) -> None:
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
        await self.session.get('https://auth.user.ameba.jp/signup/email', headers=headers, proxy=self.proxy)
        _csrf = self.session.cookie_jar.filter_cookies("https://auth.user.ameba.jp")["XSRF-TOKEN"].value
        return _csrf
    
    async def signup_v2(self,
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
        async with self.session.post('https://auth.user.ameba.jp/signup/email', headers=headers, data=data, proxy=self.proxy) as response:
            print(f"<{str(response.status)}-{len(response.history)} signup_v2>")
            if len(response.history) != 2:
                print("<v2_error>")
                raise

    async def signup_v3(self,
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
        async with self.session.post('https://auth.user.ameba.jp/signup/email', headers=headers, data=data, proxy=self.proxy) as response:
            print(f"<{str(response.status)}-{len(response.history)} signup_v3>")
            if len(response.history) != 2:
                print("<v3_error>")
                return True
            else:
                return False
            
    async def verify_email(self,
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
        async with self.session.post('https://auth.user.ameba.jp/signup/email/verification',headers=headers,data=data,proxy=self.proxy) as response:
            print(f"<{str(response.status)} verify_email>")

    async def get_ameba_id(self) -> str:
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
        async with self.session.get(f'https://auth.user.ameba.jp/api/available-ameba-id/{ameba_id}',headers=headers,proxy=self.proxy) as response:
            print(f"<{str(response.status)} get_ameba_id>")
        return ameba_id
    
    async def signup_finish(self,
                            _csrf: str,
                            ameba_id: str,
                            password: str,
                            bdayYear: str,
                            bdayMonth: str,
                            bdayDay: str,
                            gender: str) -> str:
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
            'Priority': 'u=0, i'
        }
        data = {
            '_csrf': _csrf,
            'amebaId': ameba_id,
            'showPassword': 'on',
            'password': password,
            'bdayYear': bdayYear,
            'bdayMonth': bdayMonth,
            'bdayDay': bdayDay,
            'gender': gender,
        }
        async with self.session.post('https://auth.user.ameba.jp/signup/email/form',headers=headers, data=data, proxy=self.proxy) as response:
            print(f"<{str(response.status)} signup_finish>")
        auth_token = self.session.cookie_jar.filter_cookies("https://auth.user.ameba.jp")["asauth"].value
        return auth_token
    
    async def get_ameblo_token(self) -> str:
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
        async with self.session.post('https://blog-embed.ameba.jp/_api/ameblo/token/generate', headers=headers, proxy=self.proxy) as response:
            response_json = await response.json()
        ameblo_token = response_json["data"]["ameblo_token"]
        return ameblo_token
    
    async def check_ameblo_token(self,
                                 ameblo_token: str) -> None:
        self.session.cookie_jar.clear()
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
        async with self.session.post('https://blog-embed.ameba.jp/_api/ameblo/token/check', headers=headers, json=json_data, proxy=self.proxy) as response:
            response_json = await response.json()
        if str(response_json["data"]["member"]) != '1':
            print("<check_failed>")
            raise
