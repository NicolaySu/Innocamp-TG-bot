import asyncio
import logging
from sys import stdout

import handlers  # noqa: F401
from config import dp, bot, rt


async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s: %(message)s",
                        datefmt="%H:%M:%S",
                        stream=stdout)
    dp.include_router(rt)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
