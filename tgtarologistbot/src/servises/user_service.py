import asyncio
import traceback
from datetime import datetime, timezone, timedelta

from aiogram import Dispatcher

from tgtarologistbot.src.app.database.models import User
from tgtarologistbot.src.core import logger
from tgtarologistbot.src.enums import UserStatuses, SubscriptionType


class UserService:
    def __init__(self, dispatcher: Dispatcher):
        self.check_interval = 600
        self.dispatcher = dispatcher

    async def check_subscriptions(self):
        """
        Бесконечный цикл проверки подписок у пользователей
        :return: None
        """
        while True:
            current_time = datetime.now(timezone.utc)
            expired_users = await User.filter(subscription_end__lte=current_time, status=UserStatuses.subscriber,
                                              subscription_type=SubscriptionType.time_based).all()

            for user in expired_users:
                try:
                    await self.handle_expired_subscription(user)
                except Exception as e:
                    logger.error(f"Произошла ошибка, при вызове функции handle_expired_subscription, "
                                 f"у пользователя {user.tg_id}\n{traceback.print_exception(e)}")

            await asyncio.sleep(self.check_interval)

    async def handle_expired_subscription(self, user: User):
        """
        Логика для обработки истекших подписок.
        :param user: Пользователь, подписка которого истекла
        :return: None
        """
        logger.debug(f"Подписка пользователя {user.tg_id} истекла")

        user.status = UserStatuses.guest.value()
        user.subscription_end = None
        await user.save()

        # TODO доделать

    async def subscribe_user(self, user: User, subscription_type: SubscriptionType,
                             duration: timedelta = None, usage_limit: int = None) -> bool:
        """
        Продлевает подписку пользователя на указанное время.

        :param subscription_type: Тип подписки
        :param user: Пользователь, время подписки которого нужно продлить
        :param duration: Время подписки в виде timedelta
        :param usage_limit: Добавочное количество применений подписки

        :return: bool
        """
        match subscription_type:
            case SubscriptionType.time_based:
                user.subscription_type = SubscriptionType.time_based
                current_time = datetime.now(timezone.utc)

                if user.subscription_end and user.subscription_end > current_time:
                    user.subscription_end += duration
                else:
                    user.subscription_end = current_time + duration

                logger.debug(f"Подписка пользователя {user.tg_id} продлена до {user.subscription_end}")

                return True
            case SubscriptionType.usage_based:
                user.subscription_type = SubscriptionType.usage_based
                user.usage_limit += usage_limit
                logger.debug(f"Количество применений подписки у {user.tg_id} изменена на {usage_limit}")

        await user.save()

    async def decrement_usage(self, user: User) -> bool:
        """
        Уменьшает количество оставшихся применений для "поразовой" подписки.
        :param user: Пользователь, количество применений подписок которого уменьшается

        :return: bool
        """
        if user.subscription_type == SubscriptionType.usage_based and user.usage_limit > 0:
            user.usage_limit -= 1
            await user.save()

            logger.debug(f"Количество применений подписки пользователя {user.tg_id} изменено на {user.usage_limit}")

            return True
        else:
            raise Exception(f"Пользователь {user.tg_id} не может использовать поразовую подписку")
