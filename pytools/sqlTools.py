import pymysql
from flask import flash


def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="college_db",
        cursorclass=pymysql.cursors.DictCursor,
    )


def sql_commit(execution, values=()):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(execution, values)
        connection.commit()
        return True
    except pymysql.MySQLError:
        flash("A database error occurred. Please try again.", "error")
        return False
    finally:
        # in locals just incase it isn't active, as it would make the program attempt to close a never opened connection.
        if "connection" in locals():
            connection.close()


def sql_fetch(execution, values=(), fetch_type="all"):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(execution, values)

            if fetch_type == "all":
                return cursor.fetchall()
            if fetch_type == "one":
                return cursor.fetchone()
            flash("A database error occurred. Please try again.", "error")
            return None
    except pymysql.MySQLError:
        flash("A database error occurred. Please try again.", "error")
        return None
    finally:
        # in locals just incase it isn't active, as it would make the program attempt to close a never opened connection.
        if "connection" in locals():
            connection.close()