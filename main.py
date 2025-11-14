
from collections import Counter
import db
import telegram
from config import Webhook
from datetime import date
import redis_worker
import requests
from loguru import logger

wh = Webhook()

def translate_status(status):
    """Переводит статус заказа на русский язык."""
    return {
        'WaitingCarSearch': 'Ожидается поиск машины',
        'SearchesForCar': 'Выполняется поиск машины',
        'CarFound': 'Машина найдена',
        'Running': 'Заказ выполняется',
        'Canceled': 'Заказ отменен',
        'Executed': 'Заказ успешно выполнен',
        'CostCalculation': 'Просчет'
    }.get(status)


def get_emoji(status):
    """Возвращает эмодзи для соответствующего статуса заказа."""
    return {
        'WaitingCarSearch': '⏰',
        'SearchesForCar': '♻️',
        'Running': '🟢',
        'CarFound': '🟢',
        'Canceled': '🔴',
        'Executed': '✅',
        'CostCalculation': '🔴'
    }.get(status)


def calc_total(stat):
    """Рассчитывает общие суммы выполненных и отмененных заказов."""
    total_complete = stat.get('CarFound', 0) + stat.get('Running', 0) + stat.get('Executed', 0)
    total_canceled = stat.get('Canceled', 0) + stat.get('CostCalculation', 0)
    total = sum(stat.values())

    stat['total_complete'] = total_complete
    stat['total_canceled'] = total_canceled
    stat['total'] = total


def calc_and_update_stat(stat):
    """Рассчитывает и обновляет статистику заказов, включая процент выполнения."""
    calc_total(stat)
    if stat['total'] > 0:
        stat['complete_perc'] = round(stat['total_complete'] / stat['total'] * 100)
    else:
        stat['complete_perc'] = 0


def make_stat_message(stat, emolist=None):
    """Формирует текстовое сообщение со статистикой заказов."""
    if emolist:
        message = f"{stat['complete_perc']}%\n{emolist}\nВывоз:{stat['complete_perc']}%\nВсего: {stat['total']}\nВыполнено: {stat['total_complete']}\nОтменено: {stat['total_canceled']}\nПредварительные заказы: {stat.get('WaitingCarSearch', 0)}"
    else:
        message = f"\nВывоз:{stat['complete_perc']}%\nВсего: {stat['total']}\nВыполнено: {stat['total_complete']}\nОтменено: {stat['total_canceled']}\nПредварительные заказы: {stat.get('WaitingCarSearch', 0)}"

    return message
def get_daily_stat():
    """Получает и рассчитывает статистику заказов за текущий день."""
    today_data = db.get_today_data()
    if today_data is None:
        return

    today_stat = dict(Counter(today_data))
    calc_and_update_stat(today_stat)
    message = make_stat_message(today_stat)
    return message


def make_emo_message_part(stat):
    """Создает строку эмодзи на основе списка статусов заказов."""
    message = ''
    for status in stat:
        message += get_emoji(status) or ''
    return message[::-1]


def get_current_stat():
    """Получает и рассчитывает текущую статистику заказов с визуализацией."""
    current_data = db.get_current_data()
    emolist = make_emo_message_part(current_data)

    if not current_data:
        return None, None

    current_stat = dict(Counter(current_data))
    calc_and_update_stat(current_stat)
    message = make_stat_message(current_stat, emolist)
    return message, current_stat


def send_miband_massage(current_value, old_value):
    """ Формирует и отправляет сообщение в Macrodroid для отображения уведомления в mi band """
    try:
        if int (current_value) > int(old_value):
            message = f"Вывоз растёт {current_value}"
        else:
            message = f"Вывоз падает {current_value}"
            requests.get(f'{wh.url}?message={message}')
    except Exception as ex:
        pass


def send_to_redis(current_value):
    """ Отправляет сообщения в Redis и обновляет там данные """
    redis_worker.send_message(f"{current_value}%")
    redis_worker.update_completion_percentage(current_value)


def send_completion_percentage(stat):
    """Отправляет процент выполнения в Mi Band и Redis при изменении."""
    old_value = redis_worker.get_completion_percentage()
    current_value = stat.get('complete_perc')

    try:
        if current_value and int(current_value) == int(old_value):
            return
    except Exception as ex:
        logger.exception(ex)
        return
    send_miband_massage(current_value, old_value)
    send_to_redis(current_value)


def main():
    """Основная функция, собирающая статистику и отправляющая уведомления."""
    day_message = get_daily_stat()
    current_message, current_stat = get_current_stat()
    if current_stat:
        send_completion_percentage(current_stat)
    day_header = f'Статистика за день ({date.today().strftime("%d.%m.%Y")}):\n'
    message = f"{current_message or ''}\n{'_'*10}\n{day_header}{day_message or ''}"

    last_message = db.get_last_message()
    if last_message:
        last_message_id, last_message_text = last_message
        if last_message_text != message:
            telegram.edit_message(last_message_id, message)
            db.save_message(last_message_id, message)
    else:
        response = telegram.send_message(message)
        if response:
            response = response.json()
            message_id = response["result"]["message_id"]
            telegram.pin_message(message_id)
            db.save_message(message_id, message)


if __name__ == "__main__":
    from time import sleep
    for i in range(5):
        main()
        sleep(10)
