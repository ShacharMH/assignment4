import sqlite3
import os
import sys


def main():
    database_name = "schedule.db"
    is_database_exists = os.path.isfile(database_name)

    if not is_database_exists:  # if database does not exists - we're going to create it.
        connection_to_database = sqlite3.connect(database_name)
        with connection_to_database:  # this promises to close the connection when we're done with it
            cursor = connection_to_database.cursor()  # this enables us to go through the database
            cursor.execute("""CREATE TABLE courses
                             (id INTEGER PRIMARY KEY,
                             course_name TEXT NOT NULL,
                             student TEXT NOT NULL,
                             number_of_students INTEGER NOT NULL,
                             class_id INTEGER REFERENCES classrooms(id),
                             course_length INTEGER NOT NULL)""")
            cursor.execute("""CREATE TABLE students
                             (grade TEXT PRIMARY KEY,
                             count INTEGER NOT NULL)""")
            cursor.execute("""CREATE TABLE classrooms
                             (id INTEGER PRIMARY KEY,
                             location TEXT NOT NULL,
                             current_course_id INTEGER NOT NULL,
                             current_course_time_left INTEGER NOT NULL)""")

    with open(sys.argv[1]) as f:
        file = f.read()
        input = file.split('\n')

    for line in input:
        list = line.split(', ')
        if list[0] == "C":  # course
            cursor.execute("""INSERT INTO courses
                            (id, course_name, student, number_of_students, class_id, course_length)
                            VALUES(?,?,?,?,?,?)""", (list[1], list[2], list[3], list[4], list[5], list[6]))
        elif list[0] == "S":
            cursor.execute("""INSERT INTO students 
                              (grade, count)
                              VALUES(?,?)""", (list[1], list[2]))
        else:  # list[0] == "R" classroom
            cursor.execute("""INSERT INTO classrooms
                               (id, location, current_course_id, current_course_time_left)
                               VALUES(?,?,?,?)""", (list[1], list[2], 0, 0))

    # we will now print the database:
    print("courses")
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    for course in courses:
        print(str(course))

    print("classrooms")
    cursor.execute("SELECT * FROM classrooms")
    classrooms = cursor.fetchall()
    for classroom in classrooms:
        print(str(classroom))

    print("students")
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    for student in students:
        print(str(student))

    connection_to_database.commit()


if __name__ == '__main__':
    main()





