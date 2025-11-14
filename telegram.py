import requests
from config import TG


tg = TG()


def send_message(message):
    """Отправляет сообщение в Telegram чат."""
    try:
        url = f"https://api.telegram.org/bot{tg.token}/sendMessage"
        params = {"chat_id": tg.chat_id, "text": message}
        resp = requests.get(url, params=params)
        return resp
    except Exception:
        pass


def pin_message(msg_id):
    """Закрепляет сообщение в Telegram чате."""
    url = f"https://api.telegram.org/bot{tg.token}/pinChatMessage"
    params = {"chat_id": tg.chat_id, "message_id": msg_id}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp


def unpin_message(msg_id):
    """Открепляет сообщение в Telegram чате."""
    try:
        url = f"https://api.telegram.org/bot{tg.token}/unpinChatMessage"
        params = {"chat_id": tg.chat_id, "message_id": msg_id}
        resp = requests.get(url, params=params)
        return resp
    except Exception:
        pass


def edit_message(msg_id, message):
    """Редактирует существующее сообщение в Telegram чате."""
    try:
        url = f"https://api.telegram.org/bot{tg.token}/editMessageText"
        params = {"chat_id": tg.chat_id, "message_id": msg_id, "text": message}
        resp = requests.get(url, params=params)
        return resp
    except Exception:
        pass