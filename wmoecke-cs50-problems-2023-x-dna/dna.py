import csv
import sys
import re


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("python dna.py data.csv sequence.txt")

    ext1 = re.search('\.[a-zA-Z]{3}', sys.argv[1])
    ext2 = re.search('\.[a-zA-Z]{3}', sys.argv[2])
    if ext1.group().lower() != '.csv' or ext2.group().lower() != '.txt':
        sys.exit("python dna.py data.csv sequence.txt")

    # Read database file into a variable
    database = []
    with open(sys.argv[1], 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as file:
        sequence = file.read()

    # Find longest match of each STR in DNA sequence
    AGATC = longest_match(sequence, 'AGATC')
    TTTTTTCT = longest_match(sequence, 'TTTTTTCT')
    AATG = longest_match(sequence, 'AATG')
    TCTAG = longest_match(sequence, 'TCTAG')
    GATA = longest_match(sequence, 'GATA')
    TATC = longest_match(sequence, 'TATC')
    GAAA = longest_match(sequence, 'GAAA')
    TCTG = longest_match(sequence, 'TCTG')

    # Check database for matching profiles
    match = ''
    for i in range(len(database)):
        try:
            if (AGATC == int(database[i]['AGATC'])
                and TTTTTTCT == int(database[i]['TTTTTTCT'])
                and AATG == int(database[i]['AATG'])
                and TCTAG == int(database[i]['TCTAG'])
                and GATA == int(database[i]['GATA'])
                and TATC == int(database[i]['TATC'])
                and GAAA == int(database[i]['GAAA'])
                    and TCTG == int(database[i]['TCTG'])):
                match = database[i]['name']
                break
        except KeyError:
            if (AGATC == int(database[i]['AGATC'])
                and AATG == int(database[i]['AATG'])
                    and TATC == int(database[i]['TATC'])):
                match = database[i]['name']
                break

    print(match if len(match) > 0 else 'No match')

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
