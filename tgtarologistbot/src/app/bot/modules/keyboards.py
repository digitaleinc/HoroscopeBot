from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgtarologistbot.src.core import JsonAnswer

async def get_button_text(key: str) -> str:
    return await JsonAnswer.get(key) or key

async def get_main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=await get_button_text("start_button_1"), callback_data="subscribe"),
            InlineKeyboardButton(text=await get_button_text("start_button_2"), callback_data="tarot_horoscope")
        ],
        [
            InlineKeyboardButton(text=await get_button_text("start_button_3"), callback_data="profile")
        ]
    ])
    return keyboard

async def get_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=await get_button_text("subscription_week"), callback_data="week")
        ],
        [
            InlineKeyboardButton(text=await get_button_text("subscription_month"), callback_data="month")
        ],
        [
            InlineKeyboardButton(text=await get_button_text("subscription_single_use"), callback_data="single_use")
        ],
        [
            InlineKeyboardButton(text=await get_button_text("subscription_two_uses"), callback_data="two_uses")
        ],
        [
            InlineKeyboardButton(text=await get_button_text("subscription_five_uses"), callback_data="five_uses")
        ]
    ])
    return keyboard

async def get_tarot_horoscope_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=await get_button_text("tarot_button"), callback_data="tarot"),
            InlineKeyboardButton(text=await get_button_text("horoscope_button"), callback_data="horoscope")
        ]
    ])
    return keyboard

async def get_profile_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=await get_button_text("edit_profile"), callback_data="edit_profile"),
            InlineKeyboardButton(text=await get_button_text("back_button"), callback_data="back")
        ]
    ])
    return keyboard
