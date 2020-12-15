from collections import namedtuple
from pathlib import Path
import re

Password = namedtuple('Password',['password','key','min_occurances','max_occurances'])
password_regex_s = r"^([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)" # the string to match the password form
password_prog = re.compile(password_regex_s)


def validate_password(password, key_letter, min_occurances, max_occurances):
    occurance_in_string = password.count(key_letter)
    return (occurance_in_string >= min_occurances) and (occurance_in_string <= max_occurances)

# Password policy of the official toboggan corp
def validate_password_TCP(password, key_letter, min_occurances, max_occurances):
    # check if the key exists in the index, noting that it's base 1 index
    key_in_index = [password[index-1]==key_letter for index in [min_occurances,max_occurances]]
    return (key_in_index[0] and not key_in_index[1]) or (key_in_index[1] and not key_in_index[0]) # return the XOR of the search

def parse_password_string(password_string):
    match = password_prog.match(password_string)
    if match:
        return Password(match.group(4), match.group(3), int(match.group(1)), int(match.group(2)))
    else:
        raise ValueError(f"{password_string} does not match regex")

if __name__ == "__main__":
    # getting the puzzle input
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day2.txt"
    password_count_srp = 0 # sled rental place
    password_count_otc = 0 # official toboggan corp

    # Iterate over inputs and check which password policy they match
    with open(input_file) as fii:
        #iterate over all inputs and increment the counter if it's a valid password
        for line in fii.readlines():
            password = parse_password_string(line)
            password_count_srp += 1 if validate_password(*password) else 0
            password_count_otc += 1 if validate_password_TCP(*password) else 0
    print(f"Puzzle Part 1 Result: {password_count_srp}")
    print(f"Puzzle Part 2 Result: {password_count_otc}")
        
