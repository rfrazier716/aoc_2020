import itertools

class PocketNetherWorld(object):
    def __init__(self, input_file):
        self._max_x = 0
        self._max_y = 0
        self._max_z = 0
        self._nodes = {}
    
    @property
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y

    @property
    def max_z(self):
        return self._max_z
        
class Node(object):
    def __init__(self,dimension, coordinate, state, *args, **kwargs):
        self._dimension = dimension # the pocket dimension this node is associate with
        self._position = tuple(coordinate) # where the node exists
        self._state = state # the current state (on or off)
        self._generate_neighbors()
        super().__init__(*args,**kwargs)
    
    def _generate_neighbors(self):
        """
        check the pocket dimension's nodes for values of neighbors.
        default to zero
        """
        self._neighbors = tuple((dx,dy,dz) for dx,dy,dz in itertools.product(*[[-1,0,1] for _ in range(3)]) if not dx==dy==dz==0)

    @property
    def neighbors(self):
        return self._neighbors

    @property
    def state(self):
        return self._state

    def _count_neighbors(self):
        for neighbor in self._neighbors:
            if self._dimension.in_search_space(neighbor):
                # if teh neighbor is in the search space get it's stateus
