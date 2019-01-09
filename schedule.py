import sqlite3
import os


def main():
    database_name = "schedule.db"
    is_database_exists = os.path.isfile(database_name)
    if is_database_exists:  # if file does not exist, we just exit
        connection_to_database = sqlite3.connect(database_name)

        with connection_to_database:
            cursor = connection_to_database.cursor()
            all_courses_are_done = cursor.execute("SELECT * FROM courses").fetchall() is None
            iteration_counter = 0

            while not all_courses_are_done or not is_database_exists:

                """check if a classroom is available

                assign all the courses you can to available classrooms
                    deduce the amount of students from the total amount of students
                    print: ([iteration No.]) [classroom's location]: [course name] is schedules to start
                    update the values of - current course id, current course time left.

                when a classroom has an on-going lecture inside:
                    print: ([iteration No.]) [classroom location]: occupied by [course name]
                    decrease by 1 the current course time left field.

                when a course just finished: (current course time left == 0)
                    print: ([iteration No.]) [classroom location]: [course name] is done
                    remove course from database
                    in the same iteration, assign a new course to the classroom, if exists. """

                cursor.execute("SELECT * FROM classrooms")
                classrooms = cursor.fetchall()
                for classroom in classrooms:
                    if classroom[3] == 0:
                        deal_with_ending_course(cursor, classroom, iteration_counter, connection_to_database)
                        deal_with_starting_course(cursor, classroom, iteration_counter, connection_to_database)
                    else:
                        deal_with_occupied_classroom(cursor, classroom, iteration_counter, connection_to_database)

                # updating truth values
                all_courses_are_done = cursor.execute("SELECT * FROM courses").fetchall() is None
                is_database_exists = os.path.isfile(database_name)


if __name__ == '__main__':
    main()


def deal_with_ending_course(cursor, classroom, iteration_counter, connection):
    # fetch finished course:
    cursor.execute("SELECT * FROM courses WHERE id = (?)", classroom[2])
    course = cursor.fetchone()
    # delete course from courses
    cursor.execute("DELETE FROM courses WHERE id = (?)", classroom[2])
    connection.commit()
    # print
    print('(', iteration_counter, ') ', classroom[1], ': ', course[1], ' is done')


def deal_with_starting_course(cursor, classroom, iteration_counter, connection):
    next_class_id = find_next_class(cursor, classroom[0])  # send id of classroom that's available
    if not next_class_id == -1: # there's a class to put in classroom
        cursor.execute("SELECT * FROM courses WHERE id=(?)", next_class_id)
        course = cursor.fetchone()
        # update classroom
        cursor.execute("UPDATE classrooms SET current_course_time_left = (?) WHERE id = (?)", (course[5], classroom[0]))
        connection.commit()
        cursor.execute("UPDATE classrooms SET current_course_id = (?) WHERE id =(?)", (course[0], classroom[0]))
        connection.commit()
        # update total num of students
        cursor.execute("SELECT count FROM students WHERE grade = (?)", (course[2]))
        student_count = cursor.fetchone()
        cursor.execute("UPDATE students SET count = (?) WHERE grade = (?)", (student_count-course[3], course[2]))
        connection.commit()
        # print
        print('(', iteration_counter, ') ', classroom[1], ': ', course[1], ' is scheduled to start')


def deal_with_occupied_classroom(cursor, classroom, iteration_counter, connection_to_database):
    # decrease by 1 current_course_time_left in classroom
    cursor.execute("UPDATE classrooms SET current_course_time_left = (?) WHERE id =(?)", (classroom[3]-1, classroom[0]))
    connection_to_database.commit()
    # get course name
    cursor.execute("SELECT name FROM courses WHERE id = (?)", classroom[2])
    course_name = cursor.fetchone()
    # print
    print('(', iteration_counter, ') ', classroom[1], ': occupied by ', course_name)


def find_next_class(cursor, classroom_id):
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    for course in courses:
        if course[4] == classroom_id:
            return course[0]
    return -1



