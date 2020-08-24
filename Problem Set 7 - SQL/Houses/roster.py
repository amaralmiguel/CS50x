import sys
from cs50 import SQL

# Cheking for invalid inputs
if len(sys.argv) != 2:
    print("Usage: python roster.py House")
    exit(1)

# Getting the house name
house = sys.argv[1]

# Accessing the database
db = SQL("sqlite:///students.db")

# Getting the name and the birth from students from certain house
student = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

index = 0

# Iterate over the result of the SELECT query above
for row in student:
    first_name = student[index]['first']
    middle_name = student[index]['middle']
    last_name = student[index]['last']

    if middle_name == None:
        print(first_name, ' ', last_name, ', born ', student[index]['birth'], sep='')

    else:
        print(first_name, ' ', middle_name, ' ', last_name, ', born ', student[index]['birth'], sep='')

    index += 1