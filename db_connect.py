import pymysql


def connection_db():
    host = 'localhost'
    user = 'root'
    password = '12345678'
    database = 'password'

    connection = pymysql.connect(
        host=host, user=user, password=password, database=database)

    return connection
