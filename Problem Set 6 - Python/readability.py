# Importing
from cs50 import get_string
import math

# Declaring
letters, words, sentences = 0, 1, 0

text = get_string("Text: ")

for char in text:

    if char.isspace():
        words += 1

    elif char in ['?', '!', '.']:
        sentences += 1

    elif char.isalpha():
        letters += 1

L = letters / words * 100
S = sentences / words * 100
grade = round(0.0588 * L - 0.296 * S - 15.8)

if grade >= 16:
    print("Grade 16+")

elif grade < 1:
    print("Before Grade 1")

else:
    print(f"Grade {round(grade)}")