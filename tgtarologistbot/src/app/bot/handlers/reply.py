from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, CommandStart, Command

from tgtarologistbot.src.app.database.models import User
from tgtarologistbot.src.core.json_answer import JsonAnswer
from tgtarologistbot.src.app.bot.modules.keyboards import *

router = Router()


@router.message(CommandStart())
async def start_reply(message: Message):
    start_text = await JsonAnswer.get("start")
    await message.answer(text=start_text, reply_markup=await get_main_menu_keyboard())

# Обработчик кнопки "Подписка"
@router.callback_query(lambda c: c.data == "subscribe")
async def handle_subscribe(callback_query: CallbackQuery):
    subscription_text = await JsonAnswer.get("subscription_text")
    await callback_query.message.edit_text(text=subscription_text, reply_markup=await get_subscription_keyboard())

# Обработчик кнопки "Таро / Гороскоп"
@router.callback_query(lambda c: c.data == "tarot_horoscope")
async def handle_tarot_horoscope(callback_query: CallbackQuery):
    tarot_horoscope_text = await JsonAnswer.get("tarot_questions", "intro")
    await callback_query.message.edit_text(text=tarot_horoscope_text, reply_markup=await get_tarot_horoscope_keyboard())

# Обработчик кнопки "Профиль"
@router.callback_query(lambda c: c.data == "profile")
async def handle_profile(callback_query: CallbackQuery):
    profile_text = await JsonAnswer.get("profile_info", "header")
    await callback_query.message.edit_text(text=profile_text, reply_markup=await get_profile_keyboard())

# Обработчик выбора подписки
@router.callback_query(lambda c: c.data in ["week", "month", "single_use", "two_uses", "five_uses"])
async def handle_subscription_choice(callback_query: CallbackQuery):
    subscription_choice = await JsonAnswer.get("subscription_options", callback_query.data)
    await callback_query.answer(text=f"Вы выбрали: {subscription_choice}")

# Обработчик кнопки "Назад"
@router.callback_query(lambda c: c.data == "back")
async def handle_back(callback_query: CallbackQuery):
    back_text = await JsonAnswer.get("back_to_menu")
    await callback_query.message.edit_text(text=back_text, reply_markup=await get_main_menu_keyboard())

# Обработчики для вопросов таро
@router.callback_query(lambda c: c.data == "tarot_question_1")
async def handle_tarot_question_1(callback_query: CallbackQuery):
    question_1 = await JsonAnswer.get("tarot_questions", "question_1")
    await callback_query.message.edit_text(text=question_1)

@router.callback_query(lambda c: c.data == "tarot_question_2")
async def handle_tarot_question_2(callback_query: CallbackQuery):
    question_2 = await JsonAnswer.get("tarot_questions", "question_2")
    await callback_query.message.edit_text(text=question_2)

@router.callback_query(lambda c: c.data == "tarot_question_3")
async def handle_tarot_question_3(callback_query: CallbackQuery):
    question_3 = await JsonAnswer.get("tarot_questions", "question_3")
    await callback_query.message.edit_text(text=question_3)

@router.callback_query(lambda c: c.data == "tarot_question_4")
async def handle_tarot_question_4(callback_query: CallbackQuery):
    question_4 = await JsonAnswer.get("tarot_questions", "question_4")
    await callback_query.message.edit_text(text=question_4)

@router.callback_query(lambda c: c.data == "tarot_question_5")
async def handle_tarot_question_5(callback_query: CallbackQuery):
    question_5 = await JsonAnswer.get("tarot_questions", "question_5")
    await callback_query.message.edit_text(text=question_5)

# Обработчик для ввода даты рождения для гороскопа
@router.callback_query(lambda c: c.data == "horoscope")
async def handle_horoscope(callback_query: CallbackQuery):
    horoscope_prompt = await JsonAnswer.get("horoscope_prompt")
    await callback_query.message.edit_text(text=horoscope_prompt)

# Обработчик для обработки даты рождения и вывода гороскопа
@router.message(lambda m: m.text)
async def handle_horoscope_date(message: Message):
    try:
        # Логика обработки даты рождения и гороскопа
        horoscope_result = "Гороскоп для вашего знака: Овен"
        zodiac_sign = "Овен"  # Это будет вычисляться на основе даты
        await message.answer(text=await JsonAnswer.get("horoscope_processing"))
        await message.answer(text=(await JsonAnswer.get("horoscope_result")).format(zodiac_sign=zodiac_sign, result=horoscope_result))
    except Exception as e:
        await message.answer(text=await JsonAnswer.get("horoscope_invalid_date"))

# Обработчик для продления подписки
@router.callback_query(lambda c: c.data == "extend_subscription")
async def handle_extend_subscription(callback_query: CallbackQuery):
    subscription_extended_text = await JsonAnswer.get("messages", "subscription_extend_not_possible")
    await callback_query.message.edit_text(text=subscription_extended_text)

# Обработчик для ошибок
@router.callback_query(lambda c: c.data == "error")
async def handle_error(callback_query: CallbackQuery):
    error_message = await JsonAnswer.get("messages", "error_occurred")
    await callback_query.answer(text=error_message)