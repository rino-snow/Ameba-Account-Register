import asyncio
import aiohttp

async def solver(session: aiohttp.ClientSession,
                 payload: dict,
                 proxy: str = '') -> str: 
    api_key = payload["clientKey"]
    async with session.post("https://api.capsolver.com/createTask", json=payload, proxy=proxy) as res:
        resp = await res.json()
    task_id = resp.get("taskId")
    if not task_id:
        print("<Failed to create task>")
        raise
    while True:
        await asyncio.sleep(3)
        payload = {"clientKey": api_key, "taskId": task_id}
        async with session.post("https://api.capsolver.com/getTaskResult", json=payload, proxy=proxy) as res:
            resp = await res.json()
        status = resp.get("status")
        if status == "ready":
            reCaptchaToken = resp.get("solution", {}).get('gRecaptchaResponse')
            print(f"<Captcha Success>")
            return reCaptchaToken
        if status == "failed" or resp.get("errorId"):
            print("<Solve failed>")
            raise