import pymysql



def conection():
    return pymysql.connect (
            host='localhost',
            user='root',
            password='Pg260410',
            database='mania doce',
            cursorclass=pymysql.cursors.Cursor
        )