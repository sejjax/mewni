import asyncio

from aioschedule import run_pending
from time import sleep


async def start_scheduling():
    while True:
        await run_pending()
        sleep(0.1)
