from pathlib import Path
import numpy as np


def tree_in_path(map_line,map_x_coord):
    """
    Checks if a tree is in the x-cord of the map line, looping if x is > len(map_line)

    returns: True if a tree is in the path, False otherwise
    rtype: Bool
    """
    offset = map_x_coord % len(map_line) # module operater for rollover
    return map_line[offset]=='#'


def traverse_map(map, x_step, y_step):
    """
    iterates over a "map" (array of strings) starting at the top left until reaching the
    bottom of the map. every iteration advances position by <x_step,y_step> and checks if
    a tree is hit

    returns: the total number of Trees hit
    rtype: int
    """
    trees_hit = 0
    map_depth = len(map)
    y_steps = range(0,map_depth,y_step)
    for j,step in enumerate(y_steps):
        trees_hit += 1 if tree_in_path(map[step],j*x_step) else 0
    return trees_hit



if __name__ == "__main__":
    # Load the puzzle import to a map
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day3.txt"
    with open(input_file) as fii:
        map = [line.rstrip('\n') for line in fii] # Strip newline characters

    # Part one of the puzzle, traverse the map with a 3-1 slope and count trees
    # encountered
    print(f"Part One Solution: {traverse_map(map,3,1)}")

    # part two of the puzzle - try the 5 given slopes and spit out the total product
    slopes_to_test = [[1,1],[3,1],[5,1],[7,1],[1,2]]
    trees_hit_per_slope = [traverse_map(map,*slope) for slope in slopes_to_test]
    product_of_trees = np.prod(trees_hit_per_slope)

    # print the results for part 2
    print() # print a newline
    for slope,hit_count in zip(slopes_to_test,trees_hit_per_slope):
        print(f"Slope of {slope} results in {hit_count} trees hit")
    print(f"Part Two Solution: {product_of_trees}")
