import sys
import datetime
from main import Student, Course, Assignment


def writefile(course):
    with open("newfile.txt", 'w') as newfile:
        for student in course.students:
            newfile.write(str(student.student_number) + " " +
                student.fname + " " + student.lname + " " + "CSCI3771 " +
                str(student.total_points) + "\n")
        for assignment in course.assignments:
            newfile.write("A " + assignment.name + " " + str(assignment.due_date) + " " + str(assignment.point_value))


def readfile(course):
    with open("assignments.txt", 'r') as coursefile:
        lines = coursefile.readlines()
        for i in lines:
            line_args = i.split()
            if line_args[0] == "S":
                new_student = Student(line_args[1] + " " + line_args[2], line_args[3])
                course.students.append(new_student)
            if line_args[0] == "A":
                date = line_args[2].split('-')
                new_assignment = Assignment(line_args[1], datetime.datetime(int(date[0]), int(date[1]), int(date[2])), int(line_args[3]))
                course.assignments.append((new_assignment))


if __name__ == '__main__':
    testcourse = Course("Testing")
    readfile(testcourse)
    for student in testcourse.students:
        student.total_points = 1500
    for assignment in testcourse.assignments:
        print(assignment.name, assignment.due_date, assignment.point_value)
    writefile(testcourse)
