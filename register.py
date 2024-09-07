import aiofiles
import asyncio
import solver
import tempmail_io
import json
from client import BaseClient

class Client:
    def __init__(self) -> None:
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
            self.task_v2 = json.load(f)
        with open("recaptcha_v3.json") as f:
            self.task_v3 = json.load(f)

    async def __aenter__(self):
        self.f = await aiofiles.open(self.file,"a")
        return self
    
    async def __aexit__(self,*args) -> None:
        await self.f.close()
    
    async def task(self) -> None:
        try:
            async with BaseClient(proxy=self.proxy) as client:
                _csrf = await client.signup_start()
                email = await tempmail_io.get_mail_io(client.session,self.proxy)
                reCaptchaToken = await solver.solver(client.session,self.api_key,self.task_v3,proxy=self.proxy)
                flag = await client.signup_v3(_csrf,email,reCaptchaToken)
                if flag:
                    reCaptchaToken = await solver.solver(client.session,self.api_key,self.task_v2,proxy=self.proxy)
                    await client.signup_v2(_csrf,email,reCaptchaToken)
                code = await tempmail_io.get_code_io(client.session,email,self.proxy)
                await client.verify_email(_csrf,code)
                ameba_id = await client.get_ameba_id()
                auth_token = await client.signup_finish(_csrf,ameba_id,self.password,self.bdayYear,self.bdayMonth,self.bdayDay,self.gender)
                ameblo_token = await client.get_ameblo_token()
                await client.check_ameblo_token(ameblo_token)
                account = f"{email}:{self.password}:{ameba_id}:{auth_token}:{ameblo_token}\n"
                await self.f.write(account)
                print("<success>")
        except:
            return
    
    async def register(self) -> None:
        r = self.counts % self.aio_num
        for _ in range(self.counts // self.aio_num):
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
