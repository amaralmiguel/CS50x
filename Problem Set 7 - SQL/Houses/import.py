import csv
import sys
import re
from cs50 import SQL

# Cheking for invalid inputs
if len(sys.argv) != 2:
    print("Usage: python import.py file.csv")
    exit(1)

# Accessing the database
db = SQL("sqlite:///students.db")

# Opening the .csv File
with open(sys.argv[1], "r") as students:

    # Create DictReader
    students = csv.DictReader(students, delimiter=",")

    # Iterate over .csv File
    for row in students:

        # Getting the First, Middle and Last names
        splited_names = re.split(' ', row['name'])

        if len(splited_names) == 2:
            first_name = splited_names[0]
            last_name = splited_names[1]

            # Inserting the values into the database
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, NULL, ?, ?, ?)",
                       first_name, last_name, row['house'], row['birth'])

        else:
            first_name = splited_names[0]
            middle_name = splited_names[1]
            last_name = splited_names[2]

            # Inserting the values into the database
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       first_name, middle_name, last_name, row['house'], row['birth'])