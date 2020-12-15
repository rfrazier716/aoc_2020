from collections import defaultdict

def memory_generator(starting_numbers):
    # make a dictionary that keeps track of number that were called and when they were called
    memory_dict = defaultdict(int, zip(starting_numbers,range(1,len(starting_numbers)+1)))
    next_num = 0
    turn = len(memory_dict) + 1
    # now constantly loop over the last value, check if it's been called before, and if so
    # this turns value is the difference from when it was last called
    while True:
        yield next_num # return the next number
        # now update the dictionary so you can generate the number after
        last_called_turn = memory_dict[next_num]
        # if it's never been called added it to the dict and set the next num to zero
        if not last_called_turn:
            memory_dict[next_num]=turn
            next_num = 0 # next number is always zero since it's never been called
        else:
            temp = turn - memory_dict[next_num] # temporarily store what the next number will be
            memory_dict[next_num]= turn # update the memory dict with the turn
            next_num = temp # update the next num to be the difference from when the number was last called
        turn+=1 # incrememnt the turn

def find_nth_memory_result(input_array, search_number):
    gen = memory_generator(input_array)
    for _ in range(search_number-1-len(input_array)):
        next(gen)
    return next(gen)

if __name__ == "__main__":
    input_array = [1,2,16,19,18,0]
    part1_answer = find_nth_memory_result(input_array, 2020)
    print(f"Part1 Solution: {part1_answer}")
    part2_answer = find_nth_memory_result(input_array, 30000000)
    print(f"Part1 Solution: {part2_answer}")