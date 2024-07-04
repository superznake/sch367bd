import psycopg2


def tablesList(cursor: psycopg2._psycopg.cursor):
    cursor.execute("""SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'main'""")
    table_names = cursor.fetchall()
    # Print the table names
    for table_name in table_names:
        print(table_name[0])
