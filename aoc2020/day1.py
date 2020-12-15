import itertools
from pathlib import Path,PurePosixPath
import numpy as np




def find_2020(inputs,num_combinations = 2):
    """
    accepts an interable as input and returns the product of the first two numbers in the
    iterable that sum to 2020
    """
    for vals in itertools.permutations(inputs,num_combinations):
        if sum(vals) == 2020:
            yield np.prod(vals)



if __name__ =='__main__':
    # getting the puzzle input
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day1.txt"
    puzzle_input = np.loadtxt(input_file,dtype=int)

    # Part one solution
    my_gen = find_2020(puzzle_input)
    print(next(my_gen))

    # Part two solution
    my_gen = find_2020(puzzle_input,3)
    print(next(my_gen))