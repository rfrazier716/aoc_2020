from pathlib import Path
import re
import numpy as np

boarding_pass_format = r"^[FB]{7}[RL]{3}$"
bp_prog = re.compile(boarding_pass_format)


def validate_boarding_pass(boarding_pass_string):
    if not re.match(bp_prog, boarding_pass_string):
        raise ValueError(f"Boarding Pass {boarding_pass_string} does not match Expected Format.")

def bp_string_to_row_col(boarding_pass_string):
    
    n_row_letters = 7
    n_col_letters = len(boarding_pass_string) - n_row_letters
    row_string = boarding_pass_string[:n_row_letters]
    col_string = boarding_pass_string[n_row_letters:]

    row = 0
    for j,char in enumerate(row_string):
        row += 2**(n_row_letters-(j+1)) if char=="B" else 0
    
    col = 0
    for j,char in enumerate(col_string):
        col += 2**(n_col_letters-(j+1)) if char=="R" else 0

    return row,col

def rc_to_seat_id(r,c):
    return r*8+c


def part_2(seat_id_array):
    # for part 2 sort the list and take the diff, then find the spot where the dif == 2
    seat_ids = np.sort(np.array(seat_id_array))
    diff = np.diff(np.sort(seat_ids),prepend=seat_ids[0])
    missing_id = seat_ids[diff==2][0]-1
    print(f"Part 2 Solution: {missing_id}")

if __name__ == '__main__':
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day5.txt"
    max_seat_id = 0
    with open(input_file) as fii:
        # pull the input into seat_IDs
        seat_ids = [rc_to_seat_id(*bp_string_to_row_col(line.rstrip("\n"))) for line in fii]
    print(f"Part 1 Solution: {max(seat_ids)}")

    part_2(seat_ids)

