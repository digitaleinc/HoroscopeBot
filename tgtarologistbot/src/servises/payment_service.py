import asyncio
import traceback
from datetime import timedelta, datetime, timezone
from typing import List, Coroutine, Optional

from aiogram import Dispatcher

from tgtarologistbot.src.app.database.models import Payment
from tgtarologistbot.src.core import logger
from tgtarologistbot.src.enums import PaymentStatuses


class PaymentService:
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher

        self.payment_life_time = timedelta(days=1)
        self.check_interval = timedelta(minutes=1)

    async def create_payment(self, payment: Payment) -> bool:
        return True

    async def is_payed(self, payment: Payment) -> bool:
        return True

    async def get_all_unpaid_payments_wait(self) -> List[Coroutine]:
        unpaid_payments = await Payment.filter(status=PaymentStatuses.open)
        unpaid_payments_wait: List[Optional[Coroutine]] = []

        for unpaid_payment in unpaid_payments:
            unpaid_payments_wait.append(self.wait_payment_payed(unpaid_payment))

        return unpaid_payments_wait

    async def wait_payment_payed(self, payment: Payment) -> bool:
        while True:
            current_time = datetime.now(timezone.utc)
            if current_time - payment.created_at < self.payment_life_time:
                try:
                    return await self._payment_failure(payment)
                except Exception as e:
                    logger.error(traceback.print_exception(e))

            if await self.is_payed(payment):
                try:
                    return await self._payment_success(payment)
                except Exception as e:
                    logger.error(traceback.print_exception(e))

            await asyncio.sleep(self.check_interval.seconds)

    async def _payment_success(self, payment: Payment) -> bool:
        return True  # TODO сделать

    async def _payment_failure(self, payment: Payment) -> bool:
        return True  # TODO сделать
