from datetime import date

import psycopg2
from psycopg2 import Error
# TODO обновить названия после ренейма


def tablesList(cursor: psycopg2._psycopg.cursor):
    try:
        cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'main'""")
        table_names = cursor.fetchall()
        # Print the table names
        result = ""
        for table_name in table_names:
            result += (str(table_name[0])+"\n")
        return result
    except (Exception, Error) as error:
        print(error)
        return str(error)
    finally:
        cursor.connection.rollback()


def cartridge_seek(cursor: psycopg2._psycopg.cursor, cab: str):
    try:
        sql = '''SELECT model FROM main."printer state"
        WHERE cabinet = %s'''
        cursor.execute(sql, (cab,))
        record = cursor.fetchone()
        sql = '''SELECT "Модель картриджа" FROM main."Модели картриджей"
        WHERE "Модель принтера" = %s'''
        cursor.execute(sql, (record,))
        carts = cursor.fetchall()
        # Print the table names
        result = ""
        for cart in carts:
            result += (str(cart) + "\n")
        return result
    except (Exception, Error) as error:
        print(error)
        return str(error)
    finally:
        cursor.connection.rollback()


def cartridge_replace(cursor: psycopg2._psycopg.cursor, cab: str):
    try:
        sql = '''UPDATE "main.printer state" SET "cartridge replasment date" = %s
        WHERE cabinet = %s'''
        cursor.execute(sql, (date.today(), cab,))
        cursor.connection.commit()
        result = "успешно" + str(cursor.rowcount)
        return result
    except (Exception, Error) as error:
        print(error)
        return str(error)
    finally:
        cursor.connection.rollback()
