import redis
import json
from config import RedisConf as RedisConf

conf = RedisConf()

def get_redis():
    """ Подключаемся к серверу Redis """
    try:
        return redis.Redis(host=conf.host, port=conf.port, db=conf.db)
    except:pass


def send_message(data, channel=conf.channel):
    """
    Отправляем сообщение в канал.

    :param data: Данные, которые необходимо отправить в канал
    :param channel: Имя канала, в который будут отправлены данные
    """
    try:
       redis = get_redis()
       redis.publish(channel, data)
    except Exception as e:
       print(f'Ошибка при отправке сообщения в канал {channel}: {e}')
       
def get_data(key):

    r = get_redis()
    key_type = r.type(key)

    # Обработка в зависимости от типа данных
    if key_type == b'string':
        value = r.get(key).decode('utf-8')
    elif key_type == b'list':
        value = r.lrange(key, 0, -1)  # Получение всех элементов списка
    elif key_type == b'hash':
        value = r.hgetall(key)  # Получение всех полей и значений хэша
    elif key_type == b'set':
        value = r.smembers(key)  # Получение всех элементов множества
    elif key_type == b'zset':
        value = r.zrange(key, 0, -1)  # Получение всех элементов отсортированного множества
    else:
        value = "Unknown type"
    return value


def update_completion_percentage(percentage):
    r = get_redis()
    r.set('percentage', percentage)

def get_completion_percentage():
    return get_data('percentage')