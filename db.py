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

        cursor.execute(command)
        connection.commit()
        record = cursor.fetchall()
        print("")
        print("Результат")
        print(record)

        cursor.close()
        connection.close()
        print("")
        print("Соединение с PostgreSQL закрыто")

        return record

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
