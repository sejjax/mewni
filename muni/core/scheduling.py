from aioschedule import run_pending
from asyncio import sleep
from typing import NoReturn


async def start_scheduling() -> NoReturn:
    """
    Start async scheduler forever
    """
    while True:
        await run_pending()
        await sleep(1)
