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
        sql = '''SELECT model FROM main."Printer state"
        WHERE cab = %s'''
        cursor.execute(sql, (cab,))
        record = cursor.fetchone()
        sql = '''SELECT "cartridge model" FROM main."Printer-Cartidge"
        WHERE "printer model" = %s'''
        cursor.execute(sql, (record,))
        carts = cursor.fetchall()
        # Print the table names
        result = ""
        for cart in carts:
            result += (str(cart) + "\n")
        if result!="":
            return result
        else:
            return "err"
    except (Exception, Error) as error:
        print(error)
        return str(error)
    finally:
        cursor.connection.rollback()


def cartridge_replace(cursor: psycopg2._psycopg.cursor, cab: str):
    try:
        sql = '''UPDATE main."Printer state" SET "cartridge replacement date" = %s
        WHERE cab = %s'''
        cursor.execute(sql, (date.today(), cab,))
        cursor.connection.commit()
        result = "успешно" + str(cursor.rowcount)
        return result
    except (Exception, Error) as error:
        print(error)
        return str(error)
    finally:
        cursor.connection.rollback()


def cab_list(cursor: psycopg2._psycopg.cursor):
    try:
        sql = '''SELECT cab FROM main."Cabs"'''
        cursor.execute(sql)
        cabs = cursor.fetchall()
        # Print the table names
        result = ""
        for cab in cabs:
            result += (str(cab) + "\n")
        return result
    except (Exception, Error) as error:
        print(error)
        return str(error)
    finally:
        cursor.connection.rollback()
