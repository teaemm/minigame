from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import GuessNumberState
from games.guess_number_logic import get_random_number

router = Router()
secret_numbers = {}  # {user_id: number}

@router.message(F.text == "🎯 Угадай число")
async def start_guess_game(message: Message, state: FSMContext):
    number = get_random_number()
    secret_numbers[message.from_user.id] = number
    await state.set_state(GuessNumberState.guessing)
    await message.answer("Я загадал число от 1 до 100. Попробуй угадать!")

@router.message(GuessNumberState.guessing)
async def handle_guess(message: Message, state: FSMContext):
    await state.clear()
    try:
        guess = int(message.text)
    except ValueError:
        await message.answer("Введите целое число!")
        return

    secret = secret_numbers.get(message.from_user.id)
    if not secret:
        await message.answer("Что-то пошло не так. Попробуй снова /start")
        return

    if guess > 100:
        await message.answer("Я загадал число до 100! ")
    elif guess < 1:
        await message.answer("Я загадал число от 1! ")
    elif guess < secret:
        await message.answer("Моё число больше 🔼")
    elif guess > secret:
        await message.answer("Моё число меньше 🔽")
    else:
        await message.answer("🎉 Правильно! Ты угадал!")
        await state.clear()
