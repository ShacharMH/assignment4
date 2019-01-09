import sqlite3
import os


def main():
    database_name = "schedule.db"
    is_database_exists = os.path.isfile(database_name)
    connection_to_database = sqlite3.connect(database_name)

    with connection_to_database:

        cursor = connection_to_database.cursor()

        if is_database_exists:
            should_finish = cursor.execute("SELECT * FROM courses").fetchall() is None
            counter = 0

            while not should_finish:


