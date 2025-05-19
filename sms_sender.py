import requests

API_KEY = "FC27DA09-2834-2502-C3CA-F449DCB99633"  # Замените на ваш API-ключ от sms.ru

def send_sms(phone: str, message: str) -> bool:
    """
    Отправляет SMS через API sms.ru.
    
    :param phone: Номер телефона в формате 7XXXXXXXXXX
    :param message: Текст сообщения
    :return: True, если сообщение успешно отправлено, иначе False
    """
    url = "https://sms.ru/sms/send"
    payload = {
        "api_id": API_KEY,
        "to": phone,
        "msg": message,
        "json": 1  # Ответ в формате JSON
    }
    try:
        response = requests.get(url, params=payload)
        data = response.json()
        if data.get("status") == "OK" and data["sms"][phone]["status"] == "OK":
            return True
        else:
            print(f"Ошибка отправки SMS: {data}")
            return False
    except Exception as e:
        print(f"Ошибка при отправке запроса: {e}")
        return False