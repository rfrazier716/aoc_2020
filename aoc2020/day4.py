from pathlib import Path
import re
from collections import namedtuple,defaultdict

Passport = namedtuple('Passport',['byr','iyr','eyr','hgt','hcl','ecl','pid','cid'],defaults=[None])


#make a generator that parses multiline string and yields separated passports
def batch_passport_splitter(i_stream):
    passport_string = ""
    for line in i_stream:
        # if It's an empty line we've found a complete passport entry
        if line == "\n" or not line:
            # Try to generate a passport, but if more fields than CID are missing
            # an error will be raised
            try:
                yield passport_from_string(passport_string)

            except TypeError:
                pass
            passport_string=""
        #If it's not an empty line, append it to the current passport string
        else:
            passport_string += (line.rstrip("\n")+" ")
    try:
        yield passport_from_string(passport_string)  
    #Process the final passport string
    except TypeError:
        pass

def passport_from_string(passport_string):
    #get the passport string and split it by spaces
    passport_dict = {}
    substrings = passport_string.split()
    # return the passport named tutple 
    return Passport(**{substring[:3] : substring[4:] for substring in substrings})

def year_field_valid(year_string,year_min,year_max):
    # birth year needs 4 characters and >1920 and <=2002
    correct_characters = (len(year_string) == 4)
    year_int = int(year_string)
    correct_range = ((year_int >= year_min) and (year_int <= year_max))
    # return if both are accurate
    return correct_characters and correct_range

def hair_color_valid(hair_string):
    # a hex code that's 6 digits long
    regex_string = r"^#[a-f0-9]{6}$"
    return bool(re.match(regex_string,hair_string))

def height_valid(height_string):
    # can be either cm or inches
    if 'cm' in height_string:
        height_int = int(height_string.strip('cm'))
        return ((height_int >= 150) and (height_int <= 193))

    elif 'in' in height_string:
        height_int = int(height_string.strip('in'))
        return ((height_int >= 59) and (height_int <= 76))

    else:
        return False

def eye_color_valid(eye_string):
    # any member of this set
    eye_colors = ['amb','blu','brn','gry','grn','hzl','oth']
    return any([eye_string == eye_color for eye_color in eye_colors])

def passport_id_valid(country_id_string):
    # must be 9 numbers including leading zeroes
    regex_string = r"^[0-9]{9}$"
    return bool(re.match(regex_string,country_id_string))

def validate_passport(passport):
    # check that every passport field is valid
    return all([year_field_valid(passport.byr,1920,2002),
        year_field_valid(passport.iyr,2010,2020),
        year_field_valid(passport.eyr,2020,2030),
        height_valid(passport.hgt),
        hair_color_valid(passport.hcl),
        eye_color_valid(passport.ecl),
        passport_id_valid(passport.pid)
    ])


if __name__ == '__main__':
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day4.txt"
    with open(input_file) as fii:
        splitter = batch_passport_splitter(fii)
        all_passports = list(splitter)
    print(f"Puzzle 1 answer: {len(all_passports)}")

    #iterate and validate passports
    valid_passports = 0
    for passport in all_passports:
        valid_passports += 1 if validate_passport(passport) else 0
    print(f"Puzzle 2 answer: {valid_passports}")
