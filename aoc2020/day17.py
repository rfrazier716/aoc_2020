import itertools
from pathlib import Path
import copy


class PocketNetherWorld(object):
    def __init__(self, input_file, dimension=3):
        self._nodes = {}
        self._dimension = dimension # how many dimensions the space is
        self.load_nodes(input_file)

    def load_nodes(self, input_file):
        """
        Loads nodes from a given input file
        """
        dim_padding = [0 for _ in range(self._dimension-2)] # for every dimension over 2 pad the node position with zeros
        with open(input_file) as fii:
            # iterate over lines and make a new node for every one with a "#"
            for y, line in enumerate(fii):
                for x, char in enumerate(line.rstrip('\n')):
                    if char == "#":
                        coord = (x, y, *dim_padding)  # this must be a tuple
                        self._nodes[coord] = Node(self, coord, True)

    def cycle(self):
        # does one cycle, turning on new nodes and expanding search space if needed
        # build a search space which is (1) all nodes that are on and (2) all of the active nodes neighbors
        search_space_coordinates = set(
            itertools.chain(self._nodes.keys(), *[node.neighbors for node in self._nodes.values()]))
        # print(f"Search space contains {len(search_space_coordinates)}")
        # for all the coordinates in the search space, if they're not already in the dict it must be an empty node
        # these are all the positions that we have to check to see if they turn on or off
        new_nodes = {}
        for coord in search_space_coordinates:
            this_node = copy.copy(self._nodes.get(coord, Node(self, coord, False)))

            # now check how many lit neighbors
            count = this_node.n_enabled_neighbors()
            # print(f"{this_node._position}, {bool(this_node)}, {count}")
            # if the node is not lit and has 3 neighbors it becomes lit
            if not this_node.state:
                this_node.state = (count == 3)

            # otherwise check if it's lit and has between 2 and three neighbors
            else:
                this_node.state = (2 <= count <= 3)

            # if the node is on add it to the new nodes
            if this_node.state:
                new_nodes[coord] = this_node

        # update the current nodes with the new nodes
        self._nodes = new_nodes.copy()
        # print(self._nodes)

    @property
    def nodes(self):
        return self._nodes


class Node(object):
    def __init__(self, dimension, coordinate, state, *args, **kwargs):
        self._dimension = dimension  # the pocket dimension this node is associate with
        self._position = tuple(coordinate)  # where the node exists
        self.state = state  # the current state (on or off)
        self._generate_neighbors()
        super().__init__(*args, **kwargs)

    def __bool__(self):
        return self.state

    def _generate_neighbors(self):
        """
        create a list of all neighbors the node has, this will define the search space
        """
        self._neighbors = []
        for offset in itertools.product(*[[-1, 0, 1] for _ in range(len(self._position))]):
            # if the offset isn't 0
            if any(offset):
                self._neighbors.append(tuple(x-dx for x, dx in zip(self._position, offset)))

    @property
    def neighbors(self):
        return self._neighbors

    def n_enabled_neighbors(self):
        neighbor_count = 0
        for neighbor in self._neighbors:
            neighbor_count += 1 if self._dimension.nodes.get(neighbor, False) else 0
        return neighbor_count



def cells_after_startup(input_file, dimension):
    netherworld = PocketNetherWorld(input_file, dimension)
    [netherworld.cycle() for j in range(6)]
    return len(netherworld.nodes.keys())

if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[1] / "inputs" / "day17.txt"
    part1_answer = cells_after_startup(input_file, 3)
    print(f"Part 1 Solution: {part1_answer}")
    part2_answer = cells_after_startup(input_file, 4)
    print(f"Part 2 Solution: {part2_answer}")
