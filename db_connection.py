import psycopg2
from psycopg2 import OperationalError


def get_connection():
    db_connection = None
    try:
        db_connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="use_your_postgresql_password", #put your password here
            database="student"
        )
        if db_connection:
            print("Connection success!")
        else:
            print("Unable to get the connection!")
    except OperationalError as err:
        if "password authentication failed" in str(err):
            print("Something is wrong with your user name or password")
        elif "does not exist" in str(err):
            print("Database does not exist")
        else:
            print(err)

    return db_connection
