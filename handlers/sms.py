from aiogram import Router, F
from aiogram.types import Message
from sms_sender import send_sms

router = Router()

@router.message(F.text.startswith("/sms"))
async def sms_handler(message: Message):
    """
    Обработчик команды /sms.
    Формат команды: /sms <номер_телефона> <текст_сообщения>
    """
    try:
        # Разделяем команду на части
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            await message.answer("Используйте формат: /sms <номер_телефона> <текст_сообщения>")
            return

        phone = parts[1]
        sms_text = parts[2]

        # Отправляем SMS
        if send_sms(phone, sms_text):
            await message.answer(f"SMS успешно отправлено на номер {phone}.")
        else:
            await message.answer(f"Не удалось отправить SMS на номер {phone}.")
    except Exception as e:
        await message.answer("Произошла ошибка при отправке SMS.")
        print(f"Ошибка: {e}")