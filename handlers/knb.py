from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import GuessKnb
from games.knb_logic import knb

router = Router()

@router.message(F.text == "🤚 КНБ")
async def start_knb_game(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(GuessKnb.knbguessing)
    await state.update_data(wins=0, lose=0)
    await message.answer("Играем в ""камень, ножницы, бумага"" до трех раундов")

print(knb)

@router.message(GuessKnb.knbguessing)
async def handle_knb(message: Message, state: FSMContext):
    bot_choice = knb()
    guess = message.text.strip().capitalize()

        # Получаем текущий счёт
    data = await state.get_data()
    wins = data.get("wins", 0)
    lose = data.get("lose", 0)

    await state.update_data(wins=0, lose=0)
    if guess not in ["Камень", "Ножницы", "Бумага"]:
        await message.answer("Напишите Камень, Ножницы или Бумага")
        return
    
    # Игровая логика
    result = ""
    if guess == "Камень":
        if bot_choice == 1:
            result = "Камень\nНичья"
        elif bot_choice == 2:
            wins += 1
            result = "Ножницы\nТы победил"
        elif bot_choice == 3:
            lose += 1
            result = "Бумага\nТы проиграл"
    elif guess == "Ножницы":
        if bot_choice == 1:
            lose += 1
            result = "Камень\nТы проиграл"
        elif bot_choice == 2:
            result = "Ножницы\nНичья"
        elif bot_choice == 3:
            wins += 1
            result = "Бумага\nТы победил"
    elif guess == "Бумага":
        if bot_choice == 1:
            wins += 1
            result = "Камень\nТы победил"
        elif bot_choice == 2:
            lose += 1
            result = "Ножницы\nТы проиграл"
        elif bot_choice == 3:
            result = "Бумага\nНичья"

    # Обновляем счёт
    await state.update_data(wins=wins, lose=lose)

    # Проверка на окончание игры
    if wins >= 3:
        await message.answer(f"{result}\nТы выиграл игру! Финальный счёт: {wins} / {lose}")
        await state.clear()
    elif lose >= 3:
        await message.answer(f"{result}\nТы проиграл игру. Финальный счёт: {wins} / {lose}")
        await state.clear()
    else:
        await message.answer(f"{result}\nТекущий счёт: {wins} / {lose}")