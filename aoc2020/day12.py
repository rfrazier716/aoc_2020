from pathlib import Path
import numpy as np
import re

class Boat(object):
    """
    Boat object holds it local coordinate, and accepts instructions to move
    """
    rotate_left = np.array([[0,-1],[1,0]], dtype=int)
    rotate_right = np.array([[0,1],[-1,0]], dtype=int)
    instruction_regex = re.compile(r"([NSEWLRF])([0-9]+)") # the regex to match an instruction line

    def __init__(self,x=0,y=0,*args,**kwargs):
        self._position = np.array((x, y),dtype=int)
        self._direction = np.array((1,0),dtype = int)
        super().__init__(*args,**kwargs)

    def move(self, move_string):
        match = Boat.instruction_regex.match(move_string)
        instruction = match.group(1)
        value = int(match.group(2))

        # iterate over the instructions
        if instruction == "N":
            # move north, so add to the y component of position
            self._north(value)

        elif instruction == "S":
            # move south, so subtract the y component of position
            self._south(value)

        elif instruction == "E":
            # move east, so add the x component of position
            self._east(value)

        elif instruction == "W":
            # move west, so add the x component of position
            self._west(value)

        elif instruction == "L":
            # rotate left, take the multiplication matrix n times where n is teh value/90
            n_rotations = round(value/90)
            self._rotate_left(n_rotations)
            

        elif instruction == "R":
            # rotate right, take the multiplication matrix n times where n is teh value/90
            n_rotations = round(value/90)
            self._rotate_right(n_rotations)
            # print(np.linalg.multi_dot([Boat.rotate_right for _ in range(n_rotations)]))

        elif instruction == "F":
            # moving forward a certain amount
            self._forward(value)

    def _north(self, value):
        self._position[1]+=int(value)

    def _south(self, value):
        self._position[1]-=int(value)


    def _east(self, value):
        self._position[0]+=int(value)
        
    def _west(self,value):
        self._position[0]-=int(value)

    def _rotate_right(self,n_rotations):
        self._direction = np.linalg.multi_dot([*[Boat.rotate_right for _ in range(n_rotations)],self._direction.T]).T

    def _rotate_left(self,n_rotations):
        self._direction = np.linalg.multi_dot([*[Boat.rotate_left for _ in range(n_rotations)],self._direction.T]).T
    
    def _forward(self, magnitude):
        self._position += (self._direction*magnitude)



    
    def get_manhattan(self):
        return np.sum(np.abs(self._position))

class WayPointBoat(Boat):
    """
    a waypoint inherits from a boat only it's rotation and forward instructions are modified
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._waypoint = np.array((10,1)) # the waypoint position relative to the ship

    def _north(self,value):
        # move waypoint north by given value
        self._waypoint[1]+=value
    
    def _south(self, value):
        # move waypoint south by given value
        self._waypoint[1]-=value

    def _east(self,value):
        # move waypoint east by given value
        self._waypoint[0]+=value

    def _west(self, value):
        # move waypoint west by given value
        self._waypoint[0]-=value

    def _rotate_right(self, n_rotations):
        self._waypoint = np.linalg.multi_dot([*[Boat.rotate_right for _ in range(n_rotations)], self._waypoint.T]).T

    def _rotate_left(self, n_rotations):
        self._waypoint = np.linalg.multi_dot([*[Boat.rotate_left for _ in range(n_rotations)], self._waypoint.T]).T

    def _forward(self, magnitude):
        # moves the boat forward a the product of the magnitude times the waypoint distance
        self._position+=(magnitude*self._waypoint)


        
def part1(input_file):
    boat = Boat() # make a new boat to move about
    with open(input_file) as fii:
        for line in fii:
            boat.move(line)
            #print(boat._position)
    return boat.get_manhattan()

def part2(input_file):
    boat = WayPointBoat() # make a new boat to move about
    with open(input_file) as fii:
        for line in fii:
            boat.move(line)
            # print(boat._position)
            # print(boat._waypoint)
            # print()
    return boat.get_manhattan()


if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day12.txt"
    part1_soln = part1(input_file) 
    print(f"Part 1: {part1_soln}")
    part2_soln = part2(input_file) 
    print(f"Part 2: {part2_soln}")