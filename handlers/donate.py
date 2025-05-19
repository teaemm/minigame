from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

router = Router()

# Токен вашего платежного провайдера (замените на ваш токен)
PROVIDER_TOKEN = "1744374395:TEST:29aa7cf2ee47b5c011a7"

# Настройка товара
PRICES = [LabeledPrice(label="Поддержка бота", amount=10000)]  # 100 рублей (в копейках)

@router.message(F.text.in_({"/donate", "💰 Донат"}))  # Обрабатываем и команду, и текст кнопки
async def donate_handler(message: Message):
    """Обработчик команды /donate и кнопки "💰 Донат". Отправляет счет пользователю."""
    try:
        await message.answer_invoice(
            title="Поддержка бота",
            description="Спасибо за поддержку нашего бота! ❤️",
            payload="donation_payload",  # Полезная нагрузка для проверки платежа
            provider_token=PROVIDER_TOKEN,
            currency="RUB",  # Валюта (например, RUB для рублей)
            prices=PRICES,
            start_parameter="donation"
        )
    except Exception as e:
        await message.answer("Произошла ошибка при создании счета. Попробуйте позже.")
        print(f"Ошибка: {e}")

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    """Обработчик предоплаты. Подтверждает платеж."""
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    """Обработчик успешного платежа."""
    await message.answer("Спасибо за ваш донат! Вы помогаете развитию бота! ❤️")