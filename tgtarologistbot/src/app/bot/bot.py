import asyncio

from aiogram import Bot, Dispatcher

from .handlers.callback import callback_router
from .handlers.reply import router as reply_router

from .modules.middlewares import UserMiddleware

from tgtarologistbot.src.core import logger, Config, TaskManager
from ...servises.payment_service import PaymentService
from ...servises.user_service import UserService


async def start_pooling():
    task_manager = TaskManager()
    dp = Dispatcher()

    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())

    dp.include_routers(
        callback_router,
        reply_router
    )

    logger.info("Loading services...")
    unpaid_payments_coroutines = await PaymentService(dp).get_all_unpaid_payments_wait()
    for coro in unpaid_payments_coroutines:
        task_manager.add_task(coro)

    task_manager.add_task(UserService(dp).check_subscriptions())

    logger.info('Starting bot pooling...')
    task_manager.add_task(dp.start_polling(Bot(token=Config().bot_token)))

    await asyncio.gather(*task_manager.get_tasks())