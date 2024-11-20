from tortoise import Model, fields

from tgtarologistbot.src.enums import PaymentStatuses
from tgtarologistbot.src.enums.payment_buy_option import PaymentBuyOption


class Payment(Model):
    id = fields.IntField(primary_key=True)

    amount = fields.FloatField()
    buy_option = fields.IntEnumField(enum_type=PaymentBuyOption)

    user = fields.ForeignKeyField('models.User', related_name='payments')
    status = fields.IntEnumField(enum_type=PaymentStatuses, default=PaymentStatuses.open)

    created_at = fields.DatetimeField(auto_now_add=True)
