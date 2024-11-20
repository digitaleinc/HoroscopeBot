import asyncio

from tortoise import Tortoise

from tgtarologistbot.src.app.bot.bot import start_pooling
from tgtarologistbot.src.core.config import TORTOISE_ORM
from tgtarologistbot.src.core import logger


async def main():
    logger.info("Loading...")
    await Tortoise.init(config=TORTOISE_ORM)

    await Tortoise.generate_schemas()
    logger.info("Database initialized successfully.")
    await start_pooling()


def start():
    asyncio.run(main())
