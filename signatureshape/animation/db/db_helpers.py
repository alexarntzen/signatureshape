from .db_config import FULL_PATH_DB


def set_up():
    import sqlite3

    connection = sqlite3.connect(FULL_PATH_DB)
    cursor = connection.cursor()
    return connection, cursor
