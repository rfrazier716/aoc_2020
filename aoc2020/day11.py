import numpy as np 
from pathlib import Path
from scipy.signal import convolve2d
import itertools


class FerryNode(object):
    """
    Ferry Node object keeps track of all the spaces on the ferry, 
    whether they have neightbors and if it's a seat or not

    neighbors is an array that keeps track of neighbors relative to the seat
    ordered like below

    0 1 2
    3 X 4
    5 6 7
    """
    def __init__(self, coord, is_seat):
        self.coord = coord
        self.seat = is_seat
        self._occupied = False
        # by default there's no neighbors
        self.clear_neighbors()

    def clear_neighbors(self):
        self.neighbors = [False for _ in range(8)]
        self.modified = False # flags whether a cell was modified

    @property
    def n_neighbors(self):
        return np.sum(list(map(int,self.neighbors)))

    @property
    def occupied(self):
        return self._occupied
    
    def occupy(self):
        self._occupied = True
    
    def clear(self):
        self._occupied = False


def np_array_from_puzzle_input(input_file):
    """
    Returns an array where a 1 indicates a seat and a 0 is empty space
    """
    with open(input_file) as fii:
        ml_string = [line.replace("L",'1').replace('.',"0") for line in fii.readlines()]    
    return np.genfromtxt(ml_string,int, delimiter=1)

def gen_ferry_node_array(input_file):
    """
    makes an array of Ferry node objects and returns it
    """
    nodes = []
    with open(input_file) as fii:
        for r,line in enumerate(fii):

            nodes.append([FerryNode((r,c), char == "L") for c,char in enumerate(line.rstrip('\n'))])
    return nodes

def reset_all_neighbors(ferry_nodes):
    # clears all the neighbors
    r_max = len(ferry_nodes)
    c_max = len(ferry_nodes[0])
    for i,j in itertools.product(range(r_max),range(c_max)):
        ferry_nodes[i][j].clear_neighbors()

def update_neighbors_to_right(ferry_nodes,i,j):
    # for every cell to the right, it gets a neighbor to the left
    # returns true if any cell was occupied
    # print(f"{i},{j} called right fn")
    for cell in range(j+1, len(ferry_nodes[0])):
        if ferry_nodes[i][cell].seat:
            # print(f"{i},{cell} is a seat, occupied {ferry_nodes[i][cell].occupied}")
            ferry_nodes[i][cell].neighbors[3] = ferry_nodes[i][j].occupied
            return ferry_nodes[i][cell].occupied
    return False

def update_neighbors_down(ferry_nodes,i,j):
    # for every cell down, it gets a neighbor to the top
    # returns true if any cell was occupied
    for cell in range(i+1, len(ferry_nodes)):
        if ferry_nodes[cell][j].seat:
            ferry_nodes[cell][j].neighbors[1] = ferry_nodes[i][j].occupied
            return ferry_nodes[cell][j].occupied
    return False

def update_neighbors_down_right(ferry_nodes,i,j):
    # move diagnally down and to the right, those cells get a neighbor to the top left
    # returns true if any cell was occupied
    for r,c in zip(range(i+1, len(ferry_nodes)),range(j+1, len(ferry_nodes[0]))):
        if ferry_nodes[r][c].seat:
            ferry_nodes[r][c].neighbors[0] = ferry_nodes[i][j].occupied
            return ferry_nodes[r][c].occupied # return teh status of the seat
    # if we made it through the whole loop without finding a seat, return false for no neighbors
    return False

def update_neighbors_down_left(ferry_nodes,i,j):
    # move diagnally down and to the left, those cells get a neighbor to the top left
    # returns true if any cell was occupied
    row_steps = range(i+1, len(ferry_nodes))
    col_steps = range(j-1,-1,-1)
    for r,c in zip(row_steps, col_steps):
        # if the node is a seat, set it as having an up right neighber 
        # and return that a neighbor was founr
        if ferry_nodes[r][c].seat:
            ferry_nodes[r][c].neighbors[2] = ferry_nodes[i][j].occupied
            return ferry_nodes[r][c].occupied # return teh status of the seat
    # if we made it through the whole loop without finding a seat, return false for no neighbors
    return False


def count_LOS_neighbors(ferry_nodes):
    """
    updates the ferry nodes array with neighbors in their line of sight
    """
    # clear the neighbors first
    reset_all_neighbors(ferry_nodes)
    cell_modified = False # tracks if a cell was modified
    r_max = len(ferry_nodes)
    c_max = len(ferry_nodes[0])
    for i,j in itertools.product(range(r_max),range(c_max)):
        # if the ferry's a seat go and project its state on the neighbors 
        if ferry_nodes[i][j].seat:
            # update neighbors to right
            ferry_nodes[i][j].neighbors[4] = update_neighbors_to_right(ferry_nodes,i,j)
            # update neighbors down
            ferry_nodes[i][j].neighbors[6] = update_neighbors_down(ferry_nodes,i,j)
            #update neighbors down right
            ferry_nodes[i][j].neighbors[7] = update_neighbors_down_right(ferry_nodes,i,j)
            #update neighbors down left
            ferry_nodes[i][j].neighbors[5] = update_neighbors_down_left(ferry_nodes,i,j)
            # clear the seat if too many neighbors
            if ferry_nodes[i][j].occupied and ferry_nodes[i][j].n_neighbors>=5:
                ferry_nodes[i][j].clear()
                cell_modified = True
            # assign a seat if no neighbors and empty
            elif (not ferry_nodes[i][j].occupied) and (ferry_nodes[i][j].n_neighbors == 0):
                ferry_nodes[i][j].occupy()
                cell_modified = True
    return cell_modified

def count_occupied_seats(ferry_nodes):
    occupied_count = 0
    for row in ferry_nodes:
        for node in row:
            occupied_count += 1 if node.occupied else 0
    return occupied_count

def part2(input_file):
    """
    check neighbors, using a projection, to avoid iterating unnecessarily the search
    cell gets updates when it finds a cell as well
    """
    # make a ferry node array
    nodes = gen_ferry_node_array(input_file)
    output_stable = False
    while(not output_stable):
        output_stable = not count_LOS_neighbors(nodes)
    return count_occupied_seats(nodes)

def part1(seat_map):
    fill_map = np.zeros(seat_map.shape) # an array of which seats are occupied
    fill_map_next = np.zeros(seat_map.shape) # an array of which seats are occupied
    seats_leaving = np.zeros(seat_map.shape)
    seats_entering = np.zeros(seat_map.shape)

    # make a kernel to do the 2D convolution
    conv_kernal = np.ones((3,3))
    conv_kernal[1,1] = 0
    # loop until teh matrix is stable
    no_change = False
    while not no_change:
        # convolution to count neighbors
        neighbor_count = convolve2d(fill_map,conv_kernal,mode='same')

        # seats leaving is the number of seats with neighbors >-4
        seats_leaving=np.logical_and(fill_map,neighbor_count<4)
        # seats entering is the number of seats that are empty and have no neighbors
        seats_entering=(np.logical_and(np.logical_not(fill_map), np.logical_not(neighbor_count)))

        # you have to and the seats leaving to turn a 1 to 0
        fill_map_next = np.logical_and(fill_map,seats_leaving)
        # you have to or the seats entering to turn a 0 to 1
        fill_map_next = np.logical_or(fill_map_next,seats_entering)
       
        # apply the seat_map bitmask
        fill_map_next = np.logical_and(fill_map_next,seat_map).astype(int)
        no_change = np.all(fill_map == fill_map_next)
        if not no_change:
            fill_map = fill_map_next
    return np.sum(fill_map)


if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day11.txt"
    # this is our original seat map where a 1 denotes a seat and 0 is empty
    seat_map = np_array_from_puzzle_input(input_file)
    part1_soln = part1(seat_map)
    print(f"Part 1 Solution {part1_soln}")
    part2_soln = part2(input_file)
    print(f"Part 2 Solution {part2_soln}")
    