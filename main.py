import datetime
import sqlite3

OK = '\033[92m'
WARNING = '\033[93m'
NORMAL = '\033[0m'


class Student:
    def __init__(self, name, student_number):
        self.fullname = name
        self.fname, self.lname = self.fullname.split()
        self.student_number = student_number
        self.total_points = 0
        self.homeworks = []
        self.exams = []

    def __gt__(self, other):
        return self.lname.lower() > other.lname.lower()

    def __lt__(self, other):
        return self.lname.lower() < other.lname.lower()

    def __eq__(self, other):
        return self.student_number == other.student_number


class Assignment:
    def __init__(self, name, due_date, point_value):
        self.name = name
        self.due_date = due_date
        self.point_value = point_value

    def __eq__(self, other):
        return self.name == other.name


def WriteNewStudent(ns: Student):
    db = sqlite3.connect("coursemanager.db")
    cursor = db.cursor()
    sql = "INSERT INTO STUDENTS (ID, FirstName, LastName, Course) VALUES ('{}', '{}', '{}', '{}')".format(
        str(ns.student_number), str(ns.fname), str(ns.lname), str(course.name))
    print(sql)
    cursor.execute(sql)
    db.commit()


def WriteNewAssignment(na:Assignment):
    db = sqlite3.connect("coursemanager.db")
    cursor = db.cursor()
    sql = "INSERT INTO Assignments (Name, DueDate, PointValue) VALUES ('{}', '{}', '{}')".format(
        str(na.name), str(na.due_date), str(na.point_value))
    print(sql)
    cursor.execute(sql)
    db.commit()


class Course:
    def __init__(self, name):
        self.name = name
        self.assignments = []
        self.students = []

    def AddStudent(self, name, student_number):
        new_student = Student(name, student_number)
        if new_student in self.students:
            print(WARNING + "Duplicate Entry: Student Already Exists" + NORMAL)
            return False
        else:
            self.students.append(new_student)
            self.students.sort()
            WriteNewStudent(new_student)
        return True

    def AddAssignment(self, name, ddate, pv):
        new_assignment = Assignment(name, ddate, pv)
        if new_assignment in self.assignments:
            print(WARNING + "Duplicate Entry: Assignment Already Exists" + NORMAL)
            return False
        else:
            self.assignments.append(new_assignment)
            WriteNewAssignment(new_assignment)
        return True


def getStudents():
    db = sqlite3.connect("coursemanager.db")
    cursor = db.cursor()
    sql = "SELECT * FROM STUDENTS WHERE Course is 'CSCI3771'"
    records = cursor.execute(sql)
    return records


def printMenu():
    menuOptions = [1, 2, 3, 4, 5, 6, 0]
    print("* MAIN MENU *")
    print("=============")
    print("1: View Roster")
    print("2: View Assignments")
    print("-------------------")
    print("3: Add New Assignment")
    print("4: Add New Student")
    print("5: Input Student Grade")
    print("6: Print Student Grades")
    print("0: Quit")
    return menuOptions


def getAssignments():
    db = sqlite3.connect("coursemanager.db")
    cursor = db.cursor()
    sql = "SELECT * FROM Assignments"
    records = cursor.execute(sql)
    return records


def preprocessing():
    records = getStudents()
    for record in records:
        new_student = Student(record[1] + " " + record[2], record[0])
        new_student.total_points = record[4]
        course.students.append(new_student)
    records = getAssignments()
    for record in records:
        new_assignment = Assignment(record[0], record[1], record[2])
        course.assignments.append(new_assignment)


def printAssignmentMenu():
    amOptions = [j for j in range(len(course.assignments))]
    print("{:2s}: {:20s} \t {} \t {}".format("#", "Name", "Due Date", "Point Value"))
    for i in range(len(course.assignments)):
        print("{:2s}: {:20s} \t {} \t {}".format(str(i), course.assignments[i].name,
                                                 course.assignments[i].due_date, course.assignments[i].point_value))
    return amOptions


def printStudentMenu():
    smOptions = [j for j in range(len(course.students))]
    print("{:2s}: {:20s}\t{}".format("#", "Name", "Student Number"))
    for i in range(len(course.students)):
        lNameFirst = course.students[i].lname + ", " + course.students[i].fname
        print("{:2s}: {:20s}\t{}".format(str(i), lNameFirst, course.students[i].student_number))
    return smOptions

def GradingSystem():
    smOptions = printStudentMenu()
    studentSelection = input("Enter line number: ")
    if studentSelection.isnumeric() and int(studentSelection) in smOptions:
        studentSelection = int(studentSelection)
    else:
        print(WARNING + "Invalid Input" + NORMAL)
        return
    student = course.students[studentSelection]
    print("Grading Assignments for {}".format(student.fullname))
    amOptions = printAssignmentMenu()
    assignmentSelection = input("Enter line number: ")
    if assignmentSelection.isnumeric() and int(assignmentSelection) in amOptions:
        assignmentSelection = int(assignmentSelection)
    else:
        print(WARNING + "Invalid Input" + NORMAL)
    assignment = course.assignments[assignmentSelection]
    print("Student: {}".format(student.fullname))
    print("Assignment: {}".format(assignment.name))
    print("Points Possible: {}".format(assignment.point_value))
    print("Due Date: ".format(assignment.due_date))
    pointsAwarded = input("Enter points awarded: ")
    while not (pointsAwarded.isnumeric() and 0 < int(pointsAwarded) < assignment.point_value):
        pass
        #TODO Write Loop to ensure standard input

    dateTurnedIn = input("Enter Date Turned in (YYYY-MM-DD): ")
        #TODO Write date checker for input, and then write logic to adjust pointsAwarded based on date turned in





if __name__ == '__main__':
    # Main Loop
    course = Course("CSCI3771")
    preprocessing()

    while True:
        print()
        options = printMenu()
        selection = input()
        if selection.isnumeric() and int(selection) in options:
            selection = int(selection)
        else:
            print(WARNING + "Invalid Input" + NORMAL)
            continue
        print("selection: " + str(selection))
        # VIEW ROSTER
        if selection == 1:
            printStudentMenu()
        # VIEW ASSIGNMENTS
        if selection == 2:
            printAssignmentMenu()
        # ADD NEW ASSIGNMENT
        if selection == 3:
            assignment_name = input("Assignment Name: ")
            date_entry = input('Enter a date in YYYY-MM-DD format: ')
            year, month, day = map(int, date_entry.split('-'))
            date1 = datetime.date(year, month, day)
            print(date1)
            point_value = int(input("Point Value: "))
            addbool = course.AddAssignment(assignment_name, date1, point_value)

        # ADD NEW STUDENT
        if selection == 4:
            student_name = input("Student Name (First Last): ")
            student_number = input("Student Number (@01234567): ")
            addbool = course.AddStudent(student_name, student_number)

        # INPUT STUDENT GRADE:
        if selection == 5:
            GradingSystem()
