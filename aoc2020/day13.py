import numpy as np
from pathlib import Path
from math import gcd
from collections import namedtuple

# a timetable object 
Timetable = namedtuple("Timetable",['start','period'])

def lcm(x, y):
    """
    Least Common Multiple
    """
    return x * y // gcd(x, y)

def timetable_intersection(table1,table2,gap,max_iterations = 1000):
    """
    returns a timetable that is the point where the two timetables are offset by gap
    """
    timestamp = table1.start # the initial timestamp to search
    for j in range(max_iterations):
        # if the timestamp + gap is a multiple of the period we found the new intersection
        if ((timestamp + gap) % table2.period) == 0:
            # make a new timetable object where the period is the lcm of the two periods
            new_period = lcm(table1.period,table2.period)
            return Timetable(timestamp,new_period)
        # otherwise update the timestamp and repeat
        timestamp += table1.period
    raise valueError(f"Intersection not found after {max_iterations} iterations")

def parse_puzzle_input(input_file):
    """
    parses input and returns a departure time and timetable
    """
    with open(input_file) as fii:
        departure_time = int(fii.readline())
        gap_count = 1
        bus_periods = []
        gaps = []
        for char in fii.readline().split(','):
            # if it's an x add to the gap counter
            if char=='x':
                gap_count+=1
            # if it's a character set the gap count to the number of x's in between buses
            else:
                bus_periods.append(int(char))
                gaps.append(gap_count)
                gap_count = 1
    return departure_time, np.array(bus_periods), np.array(gaps[1:])

def part1(departure_time, timetables):
    """
    find the earliest bus leaving by your departure time
    """
    departure_products = np.ceil(departure_time/timetables)
    time_til_departure = np.mod(departure_products*timetables, departure_time)
    min_departure_time = np.min(time_til_departure)
    return int(timetables[time_til_departure == min_departure_time][0]*min_departure_time)

def part2(timetables, gaps):
    """
    For part 2 you make run an intersection of the two timetables to get a new timetable object
    who's start is the point where they intersect and whose period is the LCM of the two periods

    This is done successively for each Timetable object until only one timetable remains
    """
    total_timetable = timetables[0]
    for table,gap in zip(timetables[1:],np.cumsum(gaps)):
        total_timetable = timetable_intersection(total_timetable,table,gap)
    return total_timetable.start
    

if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day13.txt"
    departure, timetable, gaps = parse_puzzle_input(input_file)
    part1_solution = part1(departure, timetable)
    print(f"Part 1 Answer: {part1_solution}")

    # for part 2 make a list of timetable objects from the timetable array
    timetables = [Timetable(0,x) for x in timetable]
    part2_solution = part2(timetables,gaps)
    print(f"Part 2 Solution: {part2_solution}")

