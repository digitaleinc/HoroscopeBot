from tortoise import Model, fields

from tgtarologistbot.src.enums import UserStatuses, SubscriptionType


class User(Model):
    tg_id = fields.IntField()

    balance = fields.FloatField(default=0.0)
    status = fields.IntEnumField(UserStatuses, default=UserStatuses.guest)

    subscription_end = fields.DatetimeField(default=None, null=True)

    subscription_type = fields.IntEnumField(SubscriptionType, default=SubscriptionType.time_based)
    usage_limit = fields.IntField(default=0)

    referral = fields.ForeignKeyField(model_name="models.User", related_name="user_referral", null=True)
