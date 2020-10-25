import datetime
import sqlite3

# CONSTANTS
OK = '\033[92m'
WARNING = '\033[93m'
NORMAL = '\033[0m'
CYAN = '\u001b[36m'
VERBOSE = True
DATABASE_NAME = "courseManager.db"
COURSE_NAME = "CSCI3771"


class Student:
    """
    Student Class: Student Class holds Data for Student data structure
    fullname:  Student's Full Name
    fname: Student's First Name
    lname: Student's Last Name
    student_number: Student's ID Number starting with @ symbol
    total_points: current total accumulated points from graded assignments

    __gt__ provides for comparison between students by alphabetical sorting of last name
    __lt__ provides for comparison between students by alphabetical sorting of last name
    __eq__ comparison of students by ID number to determine if they are identical

    """

    def __init__(self, name, sn):
        self.fullname = name
        self.fname, self.lname = self.fullname.split()
        self.student_number = sn
        self.total_points = 0

    def __gt__(self, other):
        return self.lname.lower() > other.lname.lower()

    def __lt__(self, other):
        return self.lname.lower() < other.lname.lower()

    def __eq__(self, other):
        return self.student_number == other.student_number


class Assignment:
    """
    Assignment Class: Assignment Class holds Data for Assignment data structure
    name: name of assignment
    due_date: date that assignment is due
    point_value: total amount of points that are possible for finishing the assignment

    __eq__: provides for comparison by name to determine if they are identical
    """

    def __init__(self, name, due_date, pv):
        self.name = name
        self.due_date = due_date
        self.point_value = pv

    def __eq__(self, other):
        return self.name == other.name


class Course:
    """
    Course class: Course class holds data for the Course data structure
    name: course name
    assignments: list of assignments in course.  list contains Assignment Data Structures
    students: list of students in course.  list contains Student Data Structures

    AddStudent: Adds a student to the course
    AddAssignment: Adds an assignment to the course
    """

    def __init__(self, name):
        self.name = name
        self.assignments = []
        self.students = []

    def AddStudent(self, name, sn):
        """
        AddStudent Method: Adds a student to the course.  Name is checked to make sure there is a first and last name
        new student is compared to list of current students so that duplicate students are not added
        student is then added to the student list and written into the database

        :parameter
        name: name of student to be added
        sn: student number of student to be added
        :return:  Boolean False if First or Last were omitted, False if Duplicate entry else result of WriteNewStudent
        """
        if VERBOSE: print("Length: " + str(len(name.split())), sn)
        if len(name.split()) != 2:
            print(WARNING + "First and Last name Required" + NORMAL)
            return False
        new_student = Student(name, sn)
        if new_student in self.students:
            print(WARNING + "Duplicate Entry: Student Already Exists" + NORMAL)
            return False
        else:
            self.students.append(new_student)
            self.students.sort()
            success = WriteNewStudent(new_student)
        return success

    def AddAssignment(self, name, ddate, pv):
        """
        AddAssignment Method: Adds an assignment to the course.  new assignment is compared to the list of current
        assignments so that duplicate assignments are not added. Assignment is then added to the list of assignments and
        written into the database

        :parameter
        name: name of assignment
        ddate: due date of assignment
        pv: point value of assignment
        """

        new_assignment = Assignment(name, ddate, pv)
        if new_assignment in self.assignments:
            print(WARNING + "Duplicate Entry: Assignment Already Exists" + NORMAL)
            return False
        else:
            self.assignments.append(new_assignment)
            success = WriteNewAssignment(new_assignment)
        return success


def WriteNewStudent(ns: Student) -> bool:
    """
    WriteNewStudent Function:  generates SQL for execution to Add new Student into the database

    :rtype: bool
    :param
    ns: Student Data Structure for student to be added
    :return:  result of sqlExecute Function
    """
    sql = "INSERT INTO STUDENTS (ID, FirstName, LastName, Course, TotalPoints) " \
          "VALUES ('{}', '{}', '{}', '{}', '{}')".format(
               str(ns.student_number), str(ns.fname), str(ns.lname), str(course.name), str(ns.total_points))
    return sqlExecute(sql)


def WriteNewAssignment(na: Assignment):
    """
    WriteNewAssignment Function:  generates SQL for execution to Add new Assignment into the database

    :param
    na: Assignment Data Structure for assignment to be added
    :return:  result of sqlExecute Function
    """
    sql = "INSERT INTO Assignments (Name, DueDate, PointValue, Course) " \
          "VALUES ('{}', '{}', '{}', '{}')".format(
               str(na.name), str(na.due_date), str(na.point_value), COURSE_NAME)
    return sqlExecute(sql)


def WriteGradedAssignment(sn, name, pv, pointsAwarded):
    """
    WriteGradedAssignment Function: generates SQL for execution to Add a graded assignment into the database

    :param
    sn: student number of student that completed the assignment
    name: name of assignment completed
    pv: points possible for assignment
    pointsAwarded: points awarded to the student for completing
    :return:  result of sqlExecute Function
    """
    sql = "INSERT INTO GradedAssignments (StudentNumber, AssignmentName, PointsPossible, PointsEarned, Course) " \
          "VALUES ('{}', '{}', '{}', '{}', '{}')".format(str(sn), str(name), str(pv),
                                                         str(pointsAwarded), COURSE_NAME)
    return sqlExecute(sql)


def getStudents():
    """
    getStudents Function: retrieves students from database for the course.
    """
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()
    sql = "SELECT * FROM STUDENTS WHERE Course is '{}'".format(COURSE_NAME)
    if VERBOSE: print(CYAN + sql + NORMAL)
    records = cursor.execute(sql)
    return records


def getStudentGrades(student):
    """
    getStudentGrades retrieves graded assignments, puts them in a list and returns them
    :param student:
    :return: list of grades
    """
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()
    sql = "SELECT * FROM GradedAssignments WHERE StudentNumber is '{}' " \
          "AND Course is '{}'".format(student.student_number, COURSE_NAME)
    if VERBOSE: print(CYAN + sql + NORMAL)
    records = cursor.execute(sql)
    return records


def printMenu():
    """
    printMenu Function:  Prints the main menu, If adding options, be sure to add option to the MenuOptions list.
    """
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
    """
    getAssignments Function: retrieves assignments from database for the course
    """
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()
    sql = "SELECT * FROM Assignments WHERE Course is '{}'".format(COURSE_NAME)
    if VERBOSE: print(CYAN + sql + NORMAL)
    records = cursor.execute(sql)
    return records


def preprocessing():
    """
    preprocessing Function:  sorts retrieved records and puts them into Course Data Structure before main menu is shown
    this occurs only once during runtime and ensures that data is up to date when the program initiates
    """
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
    """
    printAssignmentMenu Function:  prints the menu for Assignment selection.  amOptions dynamically creates a list of
    menu options
    """
    amOptions = [j for j in range(len(course.assignments))]
    print("{:2s}: {:20s} \t {} \t {}".format("#", "Name", "Due Date", "Point Value"))
    for i in range(len(course.assignments)):
        print("{:2s}: {:20s} \t {} \t {}".format(str(i), course.assignments[i].name,
                                                 course.assignments[i].due_date, course.assignments[i].point_value))
    return amOptions


def printStudentMenu():
    """
    printStudentMenu Function:  prints the menu for Student selection.  smOptions dynamically creates a list of
    menu options
    """
    smOptions = [j for j in range(len(course.students))]
    print("{:2s}: {:20s}\t{}".format("#", "Name", "Student Number"))
    for i in range(len(course.students)):
        lNameFirst = course.students[i].lname + ", " + course.students[i].fname
        print("{:2s}: {:20s}\t{}".format(str(i), lNameFirst, course.students[i].student_number))
    return smOptions


def compareDates(due_date, dateTurnedIn):
    """
    compareDates Function:  a utility function that compares due date and date turned in to determine how many days late
    the assignment is. function returns an integer of days late. if integer is negative, assignment is not late at all.
    """
    due_date = list(map(int, due_date.split("-")))
    dateTurnedIn = list(map(int, dateTurnedIn.split("-")))
    d1 = datetime.date(due_date[0], due_date[1], due_date[2])
    d2 = datetime.date(dateTurnedIn[0], dateTurnedIn[1], dateTurnedIn[2])
    delta = d2 - d1
    return delta.days


def sqlExecute(sql):
    """
    sqlExecute sets up a connection to the database and executes an sql statement excepts sqlite3.OperationalError
    :param sql: valid SQL statement for current database
    :return: boolean, True if SQL statement was committed, False if error occurred
    """
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()
    if VERBOSE: print(CYAN + sql + NORMAL)
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except sqlite3.OperationalError as err:
        print(WARNING + str(err) + NORMAL)
        print(WARNING + "Check Your Formatting, do not use special characters in your input")
        return False


def UpdateStudent(student):
    """
    UpdateStudent: generates SQL statement to update a student's total points after an assignment is graded
    :param student: valid Student Data Type of student who's assignment was graded
    :return:  result of sqlExecute Function
    """
    sql = "UPDATE Students SET TotalPoints = '{}' WHERE ID is '{}'".format(str(student.total_points),
                                                                           str(student.student_number))
    return sqlExecute(sql)


def CheckIfExists(student, assignment):
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()
    sql = "SELECT * FROM GradedAssignments WHERE StudentNumber is '{}' and AssignmentName is '{}'".format(
           student.student_number, assignment.name)
    records = cursor.execute(sql)
    exists = [record for record in records]
    return (True, exists[0]) if len(exists) > 0 else (False, None)


def UpdateGradedAssignment(student_number, name, pointsAwarded):
    sql = "UPDATE GradedAssignments SET PointsEarned = '{}' WHERE StudentNumber = '{}' and AssignmentName = '{}'".format(
        str(pointsAwarded), str(student_number), str(name), str(pointsAwarded), COURSE_NAME)
    return sqlExecute(sql)


def GradingSystem():
    """
    GradingSystem:  Allows the user to choose a student and then an assignment to enter a grade for.  If the assignment
    is late, it prompts the user if they would like to impose a penalty.  The points awarded is then calculated if they
    choose yes, otherwise the original points awarded is used.  The student's data structure is then updated and changes
    are written to the database
    :return: occurs if the user selects invalid input and is then returned to the main menu
    """
    smOptions = printStudentMenu()
    studentSelection = input("Enter line number: ")
    # is the selection valid?
    if studentSelection.isnumeric() and int(studentSelection) in smOptions:
        studentSelection = int(studentSelection)
    else:
        # Selection was not valid
        print(WARNING + "Invalid Input" + NORMAL)
        return
    student = course.students[studentSelection]
    print("Grading Assignments for {}{}{}".format(OK, student.fullname, NORMAL))
    amOptions = printAssignmentMenu()
    assignmentSelection = input("Enter line number: ")
    # is the selection valid
    if assignmentSelection.isnumeric() and int(assignmentSelection) in amOptions:
        assignmentSelection = int(assignmentSelection)
    else:
        #selection was not valid
        print(WARNING + "Invalid Input" + NORMAL)
        return
    assignment = course.assignments[assignmentSelection]
    print("Student: {}".format(student.fullname))
    print("Assignment: {}".format(assignment.name))
    print("Points Possible: {}".format(assignment.point_value))
    print("Due Date: {} ".format(assignment.due_date))
    pointsAwarded = input("Enter points awarded: ")
    # is the selection valid?
    while not (pointsAwarded.isnumeric() and 0 < int(pointsAwarded) <= assignment.point_value):
        # selection not valid, loop until valid
        print(WARNING + "Invalid Input" + NORMAL)
        pointsAwarded = input("Enter points awarded: ")
    pointsAwarded = float(pointsAwarded)
    dateTurnedIn = input("Enter Date Turned in (YYYY-MM-DD): ")
    # is the date valid?
    dateCheck = dateTurnedIn.split("-")
    while not ((len(dateCheck) == 3) and dateCheck[0].isnumeric() and dateCheck[1].isnumeric() and
               dateCheck[2].isnumeric()):
        print(WARNING + "Invalid Input" + NORMAL)
        dateTurnedIn = input("Enter Date Turned in (YYYY-MM-DD): ")
    days_late = compareDates(assignment.due_date, dateTurnedIn)
    if days_late > 0:
        imposePenalty = input(OK + ("Assignment is {} days late, impose {}% penalty? (y/n):".format(
            days_late, (days_late * 10))) + NORMAL)
        if imposePenalty.lower() == "y":
            if days_late >= 10:
                pointsAwarded = 0
            else:
                print("pointsAwarded:" + str(pointsAwarded), "days_late * .1: " + str(days_late * .1))
                pointsAwarded -= pointsAwarded * (days_late * .1)
    # Check if this assignment has been previously graded and is already in the database
    exists = CheckIfExists(student, assignment)
    if exists[0]:
        replace = input("This Assignment has been previously graded: \nPoints Awarded: {} \n"
                        "Would you like to update? (y/n): ".format(exists[1][3]))
        if replace.lower() == 'y':
            # Update the database with the new grade
            UpdateGradedAssignment(student.student_number, assignment.name, pointsAwarded)
            # remove the points that were awarded previously from the student record
            student.total_points -= int(exists[1][3])
        else:
            return
    else:
        # Write the graded assignment to the database
        WriteGradedAssignment(student.student_number, assignment.name, assignment.point_value, pointsAwarded)
    # add the new points to the student record
    student.total_points += pointsAwarded
    # update the student record to the database
    UpdateStudent(student)


def printStudentGrade(student: Student):
    total_points_possible = 0
    grades = getStudentGrades(student)
    print("- - - - - - - - - - - - ")
    print(" {} Grades for {}{}{}({})".format(COURSE_NAME, OK, student.fullname, NORMAL, student.student_number))
    print("{:20}\t{:10}\t{:10}".format("Assignment", "Points Possible", "Points Awarded"))

    for grade in grades:
        total_points_possible += int(grade[2])
        print("{:20}\t{:10}\t{:10}".format(grade[1], grade[2], grade[3]))
    if total_points_possible > 0:
        print("{} has a total of {} points out of {} possible: {}% ".format(
            student.fname, student.total_points, total_points_possible,
            (student.total_points / total_points_possible) * 100))
    else:
        print("{} has not completed any assignments".format(student.fname))
    print("- - - - - - - - - - - - ")


def printGradeMenu():
    stOptions = printStudentMenu()
    gdSelection = input("Enter line number or enter 'A' for all: ")
    if gdSelection.isnumeric() and int(gdSelection) in stOptions:
        # only printing one student
        student = course.students[int(gdSelection)]
        printStudentGrade(student)
    elif gdSelection == 'A':
        # printing all of the students
        for student in course.students:
            printStudentGrade(student)
        pass
    else:
        # invalid
        return


if __name__ == '__main__':
    # Main Loop
    course = Course(COURSE_NAME)
    preprocessing()

    while True:
        print()
        options = printMenu()
        selection = input(">:")
        print()
        if selection.isnumeric() and int(selection) in options:
            selection = int(selection)
        else:
            print(WARNING + "Invalid Input" + NORMAL)
            continue
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
            formatCheck = date_entry.split("-")
            while not ((len(formatCheck) == 3) and formatCheck[0].isnumeric() and formatCheck[1].isnumeric() and
                       formatCheck[2].isnumeric()):
                print(WARNING + "Invalid Input" + NORMAL)
                date_entry = input("Enter a date in YYYY-MM-DD format: ")
            year, month, day = map(int, date_entry.split('-'))
            date1 = datetime.date(year, month, day)
            point_value = input("Point Value: ")
            while not (point_value.isnumeric() and int(point_value) > 0):
                point_value = input("Point Value: ")
            point_value = int(point_value)
            added = course.AddAssignment(assignment_name, date1, point_value)
            if added:
                print(OK + "Assignment Added Successfully" + NORMAL)
            else:
                print(WARNING + "Assignment Not Added!" + NORMAL)

        # ADD NEW STUDENT
        if selection == 4:
            student_name = input("Student Name (First Last): ")
            student_number = input("Student Number (@01234567): ")
            added = course.AddStudent(student_name, student_number)
            if added:
                print(OK + "Student Added Successfully" + NORMAL)
            else:
                print(WARNING + "Student Not Added!" + NORMAL)

        # INPUT STUDENT GRADE:
        if selection == 5:
            GradingSystem()

        # PRINT GRADE
        if selection == 6:
            printGradeMenu()

# TODO Delete Student
# TODO Delete Assignment
# TODO Update Assignment
