import asyncio

from aioschedule import run_pending
from asyncio import sleep


async def start_scheduling():
    while True:
        await run_pending()
        await sleep(1)
