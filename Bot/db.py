import config
import psycopg2
from psycopg2 import Error


def db_request(command):
    try:
        connection = psycopg2.connect(user=config.USER,
                                      password=config.PASSWORD,
                                      host=config.HOST,
                                      port=config.PORT,
                                      database=config.DATABASE)

        cursor = connection.cursor()
        print("Соединение с PostgreSQL открыто")
        cursor.execute(command)
        connection.commit()
        record = cursor.fetchall()
        print("Запрос: " + command)
        print(record)
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")

        return record

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
