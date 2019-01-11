import sqlite3
import os


def main():
    database_name = "schedule.db"
    database_exists = os.path.isfile(database_name)
    if database_exists:
        connection_to_database = sqlite3.connect(database_name)

        with connection_to_database:
            cursor = connection_to_database.cursor()
            all_courses_are_done = cursor.execute("SELECT * FROM courses").fetchone() is None
            iteration = 0

            while (not all_courses_are_done) and database_exists:
                classrooms = cursor.execute("SELECT * FROM classrooms").fetchall()
                for classroom in classrooms:
                    current_course_time_left = update_classroom(classroom, cursor, connection_to_database, iteration)
                    # decrease by 1 the current_course_time_left and returns it.
                    # also: prints to screen the classroom is occupied by class
                    # if there is no lecture in classroom, returns 0.
                    if current_course_time_left == 0:
                        release_classroom(classroom, cursor, connection_to_database, iteration)
                        # print that the course is finished.
                        # also: delete course from database
                        # returns current_course_time_left and _current_course_id to 0.
                        # if there is no class to release, function just returns.
                        assign_course(classroom, cursor, connection_to_database, iteration)

                all_courses_are_done = cursor.execute("SELECT * FROM courses").fetchone() is None
                database_exists = os.path.isfile(database_name)
                iteration = iteration + 1
                print_database(cursor)


def assign_course(classroom, cursor, connection_to_database, iteration):
    """assigns new course to classroom, updates current_course_id, current_course_time_left, and
                            print to the screen that this new course is about to start.
                            also, updates the number of students."""
    classroom_id = classroom[0]
    courses = cursor.execute("SELECT * FROM courses").fetchall()

    chosen_course = 0
    for course in courses:
        if course[4] == classroom_id and chosen_course == 0:
            chosen_course = course

    if chosen_course != 0:
        cursor.execute("UPDATE classrooms SET current_course_id = (?) WHERE id = (?)", (chosen_course[0], classroom_id))
        connection_to_database.commit()
        cursor.execute("UPDATE classrooms SET current_course_time_left=(?) WHERE id=(?)", (chosen_course[5], classroom_id))
        connection_to_database.commit()

        updated_count = cursor.execute("SELECT count FROM students WHERE grade = (?)", (chosen_course[2],)).fetchone()[0] - chosen_course[3]
        cursor.execute("UPDATE students SET count = (?) WHERE grade = (?)", (updated_count, chosen_course[2]))
        connection_to_database.commit()

        print('(', iteration, ') ', classroom[1], ': ', chosen_course[1], ' is schedule to start', sep='')


def update_classroom(classroom, cursor, connection_to_database, iteration):
    """decrease by 1 the current_course_time_left and returns it.
                    also: prints to screen the classroom is occupied by class.
                    if there is no lecture in classroom, returns 0."""
    new_cctl = 0
    if classroom[2] != 0 and iteration != 0:
        new_cctl = classroom[3]-1
        cursor.execute("UPDATE classrooms SET current_course_time_left = (?) WHERE id = (?)", (new_cctl, classroom[0]))
        connection_to_database.commit()

        course_name = cursor.execute("SELECT course_name FROM courses WHERE id =(?)", (classroom[2],)).fetchone()
        # print('course name: ', course_name[0])

        if new_cctl != 0:
            print('(', iteration, ') ', classroom[1], ': occupied by ', course_name[0], sep='')

    return new_cctl


def release_classroom(classroom, cursor, connection_to_database, iteration):
    """print that the course is finished.
                            also: delete course from database and returns current_course_time_left
                            and current_course_id to 0.
                            if there is no class to release, function just returns."""
    if classroom[2] != 0:
        classroom_id = classroom[0]
        course_name = cursor.execute("SELECT course_name FROM courses WHERE id =(?)", (classroom[2],)).fetchone()

        print('(', iteration, ') ', classroom[1], ': ', course_name[0], ' is done', sep='')

        cursor.execute("DELETE FROM courses WHERE id =(?)", (classroom[2],))
        connection_to_database.commit()
        cursor.execute("UPDATE classrooms SET current_course_id =(?) WHERE id = (?)", (0, classroom_id))
        connection_to_database.commit()
        cursor.execute("UPDATE classrooms SET current_course_time_left = (?) WHERE id = (?)", (0, classroom_id))
        connection_to_database.commit()


def print_database(cursor):
    print('courses')
    no_courses_left = cursor.execute("SELECT * FROM courses").fetchone() is None
    if not no_courses_left:
        courses = cursor.execute("SELECT * FROM courses").fetchall()
        for course in courses:
            print(course)
    print('classrooms')
    classrooms = cursor.execute("SELECT * FROM classrooms").fetchall()
    for classroom in classrooms:
        print(classroom)
    print('students')
    students = cursor.execute("SELECT * FROM students").fetchall()
    for student in students:
        print(student)


if __name__ == '__main__':
    main()




