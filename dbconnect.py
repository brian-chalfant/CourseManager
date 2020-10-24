import sqlite3

db = sqlite3.connect("courseManager.db")
cursor = db.cursor()
with open("assignments.txt", 'r') as newfile:
    lines = newfile.readlines()
    for line in lines:
        line = line.split()
        rows = cursor.execute("INSERT INTO ASSIGNMENTS (Name, DueDate, PointValue, Type ) VALUES ('{}', '{}', '{}', "
                              "'{}')".format(line[0], line[1], line[2], line[3]))
db.commit()
