import asyncio
import aiohttp

from bot import constance as co


class DataTaker:

    @staticmethod
    async def get_data(url:str, urn:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url}{urn}') as response:
                return await response.json()


    @staticmethod
    async def main(future_func, args):
        loop = asyncio.get_running_loop()
        task = loop.create_task(future_func(*args))
        data = await asyncio.gather(task)
        return data[0]


    @classmethod
    async def main_currency_list(cls):
        data = await cls.main(cls.get_data, (co.URL, co.CURRENCY_LIST))
        return data
    

    @classmethod
    async def main_active_pair(cls):
        data = await cls.main(cls.get_data, (co.URL, co. ACTIVE_PAIR))
        return data


    @classmethod
    async def main_exchange_rate(cls):
        data = await cls.main(cls.get_data, (co.URL, co.EXCHANGE_RATE))
        return data