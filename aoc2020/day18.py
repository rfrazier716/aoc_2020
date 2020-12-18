import re
import operator
from pathlib import Path
import numpy as np

# regex used to parse line
math_regex = re.compile(r"\([0-9*+ ]+\)")
addition_regex = re.compile(r"([0-9]+) \+ ([0-9]+)")
operator_regex = re.compile("[+*]")
num_regex = re.compile("[0-9]+")

def math_char_to_operator(math_char):
    """
    takes a math character and returns a function to act on two inputs based on that math char
    """
    if math_char == "*":
        return operator.mul
    elif math_char == "+":
        return operator.add
    else:
        raise ValueError(f"{math_char} does not match a known operator")

def new_math(math_string):
    """
    assumes a flattened math string
    """
    operators = operator_regex.findall(math_string)
    numbers = num_regex.findall(math_string)
    current_sum = int(numbers[0])
    for num,this_operation in zip(numbers[1:], operators):
    # apply the appropriate operation to based on the found values
        current_sum = math_char_to_operator(this_operation)(current_sum, int(num))
    
    return current_sum

def new_math_with_priority(math_string):
    # do all addition first
    n_subs = 1 # have to do this to enter the loop the first tiem
    while n_subs:
        math_string, n_subs = addition_regex.subn(lambda x: str(int(x.group(1)) + int(x.group(2))), math_string)
    # now extract all the numbers from the math string and take the product
    numbers = [int(x) for x in num_regex.findall(math_string)]
    return np.prod(numbers)
    



def parse_math_string(math_string, math_operation):
    n_subs = 1 # have to do this to enter the loop the first tiem
    while n_subs:
        math_string, n_subs = math_regex.subn(lambda x: str(math_operation(x.group(0))), math_string)
    return math_operation(math_string)
    
def total_sum(input_file, math_function):
    total_sum = 0
    with open(input_file) as fii:
        for line in fii:
            total_sum += parse_math_string(line, math_function)
    return total_sum


# Find All Paranthesis gaps
if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[1] / "inputs" / "day18.txt"
    part1_soln = total_sum(input_file, new_math)
    print(f"Part 1 Solution: {part1_soln}")
    part2_soln = total_sum(input_file, new_math_with_priority)
    print(f"Part 2 Solution: {part2_soln}")
   

