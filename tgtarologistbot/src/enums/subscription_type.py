from enum import IntEnum


class SubscriptionType(IntEnum):
    time_based = 0  # Подписка по времени
    usage_based = 1  # Подписка по количеству применений