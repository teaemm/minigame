from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router = Router()

@router.message(lambda msg: msg.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🎯 Угадай число")],
        [KeyboardButton(text="🤚 КНБ")],
        [KeyboardButton(text="❌ Крестики-нолики")],
        [KeyboardButton(text="💰 Донат")],
        [KeyboardButton(text="🌐 Мини-приложение", web_app=WebAppInfo(url="https://teaemm.github.io/"))]  # Кнопка для мини-приложения
    ], resize_keyboard=True)

    await message.answer("Привет! Выбери игру или поддержи бота:", reply_markup=kb)