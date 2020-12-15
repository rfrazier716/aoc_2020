from pathlib import Path
import numpy as np
from collections import defaultdict

def customs_importer(i_stream):
    customs_string = ""
    line_counter = 0
    for line in i_stream:
        # if It's an empty line we've found a customs ID entry
        if line == "\n" or not line:
            yield line_counter, customs_string
            customs_string = "" # reset the string
            line_counter = 0
        #If it's not an empty line, append it to the current customs string
        else:
            customs_string += (line.rstrip('\n'))
            line_counter+=1
    # yield the last string
    yield line_counter, customs_string

def part_1_solution(customs_strings):
    """
    Turn every customs string into a set to eliminate duplicates 
    the answer to part 1 is the sum of the length of the sets
    """
    customs_sets = [set(x) for x in customs_strings]
    part_1_sum = np.sum([len(x) for x in customs_sets])
    print(f"Part 1 Solution: {part_1_sum}")

def part_2_solution(customs_strings, party_size):
    """
    for part 2 take the following steps
    - for each customs entry make a default dict that counts the occurances of every letter
    - when updating the dict entry, check if it equals the party size, if so increment all answered
    the solution is the resulting value of all_answered
    """

    all_answered = 0 # variable that tracks how many questions every group member answered
    for customs_string, size in zip(customs_strings, party_size):
        this_dict = defaultdict(int)
        for char in customs_string:
            this_dict[char]+=1 # add the total count
            # check if the value equals that party's size, this eliminates a second for loop
            all_answered += 1 if this_dict[char] == size else 0 

    print(f"Part 2 Solution {all_answered}")



if __name__ == '__main__':
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day6.txt"
    max_seat_id = 0
    with open(input_file) as fii:
        # make a multiline string generator
        ml_string_gen = customs_importer(fii)
        party_size=[]
        customs_strings=[]
        for n_people,customs_string in ml_string_gen:
            party_size.append(n_people)
            customs_strings.append(customs_string)

    part_1_solution(customs_strings)
    part_2_solution(customs_strings, party_size)
