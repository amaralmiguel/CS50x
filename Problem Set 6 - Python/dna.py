import sys
import csv

# Cheking for invalid inputs
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

# Reading the .txt File
txt_file = open(sys.argv[2], "r")
for char in txt_file:
    string = char

# Finding the Longest Sequence of a DNA


def longest_sequence(string, dna):
    count = 0
    pattern = dna

    while pattern in string:
        count += 1
        pattern += dna

    return count


# Gets the occurrences of every sequence in the .txt File...
DNA = {
    "AGATC": str(longest_sequence(string, "AGATC")),
    "TTTTTTCT": str(longest_sequence(string, "TTTTTTCT")),
    "AATG": str(longest_sequence(string, "AATG")),
    "TCTAG": str(longest_sequence(string, "TCTAG")),
    "GATA": str(longest_sequence(string, "GATA")),
    "TATC": str(longest_sequence(string, "TATC")),
    "GAAA": str(longest_sequence(string, "GAAA")),
    "TCTG": str(longest_sequence(string, "TCTG"))
}

# Reading the .csv File
with open(str(sys.argv[1])) as csv_file:
    read_csv = csv.DictReader(csv_file, delimiter=',')
    for row in read_csv:
        # If we searching in the small database
        if 'small' in sys.argv[1]:
            # Checking
            AGATC = row['AGATC'] == DNA['AGATC']
            AATG = row['AATG'] == DNA['AATG']
            TATC = row['TATC'] == DNA['TATC']

            if AGATC and AATG and TATC:
                print(row['name'])
                exit(0)
        # If we searching in the large database
        elif 'large' in sys.argv[1]:
            # Checking
            AGATC = row['AGATC'] == DNA['AGATC']
            TTTTTTCT = row['TTTTTTCT'] == DNA['TTTTTTCT']
            AATG = row['AATG'] == DNA['AATG']
            TCTAG = row['TCTAG'] == DNA['TCTAG']
            GATA = row['GATA'] == DNA['GATA']
            TATC = row['TATC'] == DNA['TATC']
            GAAA = row['GAAA'] == DNA['GAAA']
            TCTG = row['TCTG'] == DNA['TCTG']

            if AGATC and TTTTTTCT and AATG and TCTAG and GATA and TATC and GAAA and TCTG:
                print(row['name'])
                exit(0)
        # If none of two cases before
        else:
            exit(2)
    # In case no match
    print("No Match")