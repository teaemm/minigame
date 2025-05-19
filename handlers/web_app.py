from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.web_app_data)
async def web_app_handler(message: Message):
    """
    Обрабатывает данные, отправленные из мини-приложения.
    """
    data = message.web_app_data.data  # Получаем данные, отправленные из мини-приложения

    if data == "guess_number":
        await message.answer("Вы выбрали игру 'Угадай число'. Напишите /start, чтобы начать!")
    elif data == "knb":
        await message.answer("Вы выбрали игру 'Камень, ножницы, бумага'. Напишите /start, чтобы начать!")
    else:
        await message.answer("Неизвестная команда из мини-приложения.")