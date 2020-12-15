import numpy as np
from pathlib import Path

def part2_depth_first_helper(input_array,search_index):
    """
    Look at the next three values in the array, for each one that is <3 from the current array
    re-enter the search with that value (since it's an appropriate jump)
    """
    sub_count = 0 # this is the count for all the calls below this function call
    potential_jumps = [x for x in range(search_index+1,min(search_index+4,input_array.shape[0])) if (input_array[x]-input_array[search_index])<=3]

    # for every potential jump, re-enter the helper function with the updated index
    if potential_jumps:
        for jump in potential_jumps:
            sub_count+=part2_depth_first_helper(input_array,jump) # add all the complete branches to this count
        return sub_count

    # if there were no potential jumps, we're at the max, so add 1 to denote an exit
    else:
        return sub_count+1 

def part2(input_array):
    """
    find out how many combination of the input array will product the right joltage output.

    the puzzle input can be sorted and then split into sub-arrays at any point where the gap is >=3
    since that step always needs to be taken.

    for every sub-array do a depth-first search to find how many independent combinations of the subarray
    make a chain with gap <3 that still reaches the max value of the subarray
    """

    sorted_input = np.sort(input_array) # sort the list
    sorted_input = np.insert(sorted_input,0,0) # prepend the input with zero (the wall charger input)
    sorted_diff = np.diff(sorted_input,prepend=0) # take a diff of the list which we'll use to split it into subarrays
    
    # split the sorted input into subarrays where the gap is 3 or more, these arrays can be analyzed separately
    split_indices = np.arange(sorted_input.shape[0])[sorted_diff>=3]

    branch_products=1 # variable to keep track of the total number of potential combinations
    # make the sublist and iterate over it
    for head, tail in zip(np.insert(split_indices,0,0),np.insert(split_indices,split_indices.shape[0],sorted_input.shape[0])):
        sub_array=sorted_input[head:tail]
        counts_in_subarray = part2_depth_first_helper(sub_array,0)
        branch_products*=counts_in_subarray
    return branch_products

def part1(input_array):
    """
    Get the chain of joltage converters and count the 3 steps multiplied by the 1 steps
    """
    # sort the list and take the difference of the sort
    sorted_diff = np.diff(np.sort(input_array),prepend=0)
    n_one_steps = np.count_nonzero(sorted_diff == 1)
    n_three_steps = np.count_nonzero(sorted_diff == 3)+1 # add one to account for the final interface
    return n_one_steps*n_three_steps

if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day10.txt"
    input_list = np.loadtxt(input_file)
    part1_answer = part1(input_list)
    print(f"Part 1 Solution: {part1_answer}")
    part2_answer = part2(input_list)
    print(f"Part 2 Solution: {part2_answer}")