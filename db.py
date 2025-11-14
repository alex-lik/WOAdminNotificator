import pymysql
from config import DB
from loguru import logger
db = DB()

def get_connection():
    try:
        if not all([db.host, db.port, db.user, db.password, db.name]): 
            print("Database connection information is incomplete.")
            return None
        return pymysql.connect(host=db.host, port=int(db.port), user=db.user, password=db.password, db=db.name)
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return None

def execute(query, args=None):
    try:
        connect = get_connection()
        if not connect: return None
        with connect:
            with connect.cursor() as cursor:
                cursor.execute(query, args)
                connect.commit()
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return None

def get_today_data():
    """ Получить сегодняшние статусы."""
    sql = "SELECT ExecutionStatus FROM StatOrder WHERE OrderDate >= CURDATE()"
    return [row[0] for row in execute(sql) if row[0]]

def get_current_data(limit=15):
    """ Получить текущее состояние статистики. Последние n записей. """
    sql = "SELECT ExecutionStatus FROM StatOrder WHERE OrderDate >= CURDATE() ORDER BY OrderDate DESC LIMIT %s" % (limit)
    return [row[0] for row in execute(sql) if row[0]]

def save_message(message_id, message_text):
    sql = "REPLACE INTO TgStatusMessage (msg_id, text, date) VALUES (%s, %s, CURDATE())"
    # print(sql, (message_id, message_text))
    execute(sql, (message_id, message_text))

def get_last_message():
    sql = "SELECT msg_id, text FROM TgStatusMessage WHERE date = CURDATE()"
    result = execute(sql)
    if result:
        return result[0]
    return None
