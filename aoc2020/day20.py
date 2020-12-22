from pathlib import Path
import re
import networkx as nx
import enum
import itertools

from collections import namedtuple
from recordtype import recordtype
import numpy as np
import copy

# a namedtuple to handle the puzzle pieces
PuzzlePiece = recordtype("PuzzlePiece", ["id","piece","edges"])

class PuzzleParser(object):
    def __init__(self, input_file, *arge, **kwargs):
        self._pieces = {}
        # parse the input
        self._parse_input(input_file)
    
    
    def _parse_input(self, input_file):
        with open(input_file) as fii:
            # iterate over all non-empty lines and fill a puzzlepiece with the info
            lines_to_read = 12
            while True:
                lines = [line for line in itertools.islice(fii,lines_to_read)]
                if not lines:
                    break
                else:
                    id_match = re.match("[a-zA-Z ]*([0-9]+):",lines[0])
                    if not id_match:
                        raise ValueError(f"{lines[0]} does not match a number regex")
                    id = int(id_match.group(1))
                    puzzle = np.zeros((10,10),dtype=str)
                    for j,line in enumerate(lines[1:11]):
                        puzzle[j,:] = [char for char in line.rstrip("\n")]
                    # make strings of all the edges
                    top = "".join(puzzle[0,:])
                    bottom = ("".join(puzzle[-1,:]))
                    left = ("".join(puzzle[:,0]))
                    right = "".join(puzzle[:,-1])
                    reversed_edges = [x[::-1] for x in [top,bottom, left, right]] # reverse because images can flip
                    edges = set([top, bottom, left, right, *reversed_edges])
                    
                    # make a puzzle piece from the inputs
                    self._pieces[id] = PuzzlePiece(id, puzzle, edges)

    @property 
    def pieces(self):
        return self._pieces
        
class PuzzleAssembler(object):
    """
    Assembles puzzle by building a graph where the connections are based on the puzzle edges
    """
    def __init__(self, pieces, trim_corners = True):
        self._pieces = pieces # the puzzle pieces
        self._graph = nx.Graph()
        puzzle_dim = int(np.sqrt(len(self._pieces.keys())))
        self._trim_corners = trim_corners

        #make an array based on this dim that should be 8 cells per piece
        if self._trim_corners:
            self._puzzle = np.zeros((8*puzzle_dim, 8*puzzle_dim),dtype=str)
        else:
            self._puzzle = np.zeros((10*puzzle_dim, 10*puzzle_dim),dtype=str)
        
        self._side_length = 8 if trim_corners else 10 # the side length of a piece


        self._build_graph()
        self._corners = [n for n,d in self._graph.degree() if d==2] # the corner pieces

        self._solve_puzzle()



    def _build_graph(self):
        self._graph.add_nodes_from(self._pieces.keys()) # make each graph label a node
        #  now iterate over the pieces, for ever edge in the piece check what other pieces have the same edge, then make a graph edge
        for key in self._pieces.keys():
            for edge in  self._pieces[key].edges:
                edges_to_add = [this_key for this_key in self._pieces.keys() if this_key != key and (edge in self._pieces[this_key].edges)]
                self._graph.add_edges_from([(key, edge) for edge in edges_to_add])
    
    def _write_piece_to_puzzle(self, x_offset,y_offset,piece):
        # print(f"placing {piece.id} at {x_offset},{y_offset}")
        piece_to_write = piece.piece[1:-1,1:-1] if self._trim_corners else piece.piece
        self._puzzle[y_offset:(y_offset+self._side_length),x_offset:(x_offset+self._side_length)] = piece_to_write # insert the piece into the puzzle
    
    def _find_next_piece(self, graph, piece):
        prefered_directions = [1,3] # we'd prefer to go right or left
        # find all edge directions and orientations
        piece_edges =  [x[1] for x in list(graph.edges(piece.id)) if graph.degree(x[1])<=3]
        orientations = [orient_pieces(piece, self._pieces[edge]) for edge in piece_edges]

        #check if a preferred direction exists
        for j,orientation in enumerate(orientations):
            if orientation in prefered_directions:
                return self._pieces[piece_edges[j]] # return the next piece
        
        # if we don't have our prefered direction all that's left must be the backup
        return self._pieces[piece_edges[0]]
            


    def _solve_puzzle(self):
        x_offset = 0
        y_offset = 0
        local_graph = copy.deepcopy(self._graph) # copy the graph so we can delete edges
        self._orient_top_left_corner() # orient the first corner to be top left
        piece = self._pieces[self._corners[0]] # the active piece is the top left corner

        # loop until we've removed all edges from the graph and placed the pieces
        while local_graph.number_of_nodes()>1:
            self._write_piece_to_puzzle(x_offset,y_offset,piece)
            # print(f"Edges Left: {local_graph.number_of_nodes()}")
            # now find a new edge
            piece_edges =  [x[1] for x in list(local_graph.edges(piece.id)) if local_graph.degree(x[1])<=3]
            # find the next piece
            if not piece_edges:
                self.print_puzzle()
                raise ValueError(f"Piece {piece.id} has no edges left!")
            else:
                next_piece = self._find_next_piece(local_graph,piece)
            # print(f"Next Piece is {next_piece.id}")

            # reorient the new piece and update the x_offset and y_offset 
            orientation = orient_pieces(piece, next_piece)
            if orientation == 0:
                y_offset -= self._side_length
            if orientation == 1:
                x_offset += self._side_length
            if orientation == 2:
                y_offset += self._side_length
            if orientation == 3:
                x_offset -= self._side_length
            
            # remove the edge that was just traveled from the graph
            local_graph.remove_node(piece.id)

            # assign next_piece to piece
            piece = next_piece
        # after exiting we still have to place the final piece
        self._write_piece_to_puzzle(x_offset,y_offset,piece)

        # self.print_puzzle()



    
    def _orient_top_left_corner(self):
        # takes the four corner pieces and sees which ones return 1 and 2 for edge orientation
        tl_corner = self._pieces[self._corners[0]] # assign a corner to the top left
        # makes a list of which cor
        adjacent_edges = [orient_pieces(*[self._pieces[x] for x in edge]) for edge in self._graph.edges(tl_corner.id)]
        edge_sum = adjacent_edges[0]+adjacent_edges[1]
        # case for a bottom left piece
        if edge_sum == 1:
            tl_corner.piece = np.rot90(tl_corner.piece, 3)
        # bottom right corner
        elif edge_sum == 3 and (3 in adjacent_edges):
            tl_corner.piece = np.rot90(tl_corner.piece, 2)
        # top right corner
        elif edge_sum == 5:
            tl_corner.piece = np.rot90(tl_corner.piece, 1)
        
    def print_puzzle(self):
        for line in self._puzzle:
            print("".join(line))

    @property
    def puzzle(self):
        return self._puzzle
    
    @property
    def corners(self):
        return self._corners
    
    @property
    def graph(self):
        return self._graph




def orient_pieces(piece1, piece2):
    # reorients two puzzle pieces so the the second is oriented properly to the first, also returns a number 0-3
    # saying where the second piece goes relative to the first where it means [top, right, bottom, left]
    piece = piece1.piece
    top = "".join(piece[0,:])
    bottom = ("".join(piece[-1,:]))
    left = ("".join(piece[:,0]))
    right = "".join(piece[:,-1])
    main_edges = [top,right,bottom,left]
    orientation = 0
    x_edge = ""
    for j,edge in enumerate(main_edges):
        if edge in piece2.edges:
            orientation = j
            x_edge = edge
            break
    edge_to_find = (orientation + 2) % 4 # so that left searches for right etc

    # now iterate over the pieces to find the matching edge
    rot_piece = piece2.piece
    for j in range(4):
        if ''.join(puzzle_edge(rot_piece, edge_to_find)) == x_edge:
            piece2.piece = rot_piece
            return orientation

        elif ''.join(puzzle_edge(rot_piece.T, edge_to_find)) == x_edge:
            piece2.piece = rot_piece.T
            return orientation
        rot_piece = np.rot90(rot_piece) # rotate the matrix

def puzzle_edge(x, j):
    if j == 0:
        return x[0,:]
    elif j == 1:
        return x[:,-1]
    elif j == 2:
        return x[-1,:]
    elif j == 3:
        return x[:,0]

class MonsterHunter(object):
    """
    Finds Seamonsters
    """
    monster_string=[
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    ]
    monster_array = np.array([[char for char in line] for line in monster_string])

    def __init__(self, map_array):
        self._map = copy.copy(map_array)
        self._monsters_found = False
        self._find_all_monsters()
        

    def _scan_for_monster(self):
        y_max, x_max = np.array(self._map.shape) - np.array(MonsterHunter.monster_array.shape)
        monster_height, monster_width = MonsterHunter.monster_array.shape
        # make a mask for looking at the array
        monster_mask = (MonsterHunter.monster_array == '#')
        for x,y in itertools.product(range(0,x_max),range(0,y_max)):
            subsection = self._map[y:y+monster_height,x:x+monster_width]
            has_monster= np.all(subsection[monster_mask]== '#')
            self._monsters_found |= has_monster # if we've found a monster update so we don't keep flipping the map
            # if there's a monster replace that subsection with "O"
            if has_monster:
                subsection[monster_mask] = "O"
    
    def _find_all_monsters(self):
        for _ in range(4): # should only have to do 4 iterations
            # scan for monsters in both the rotate array and the transposed one in case it's flipped
            self._scan_for_monster() # look in the normal map
            if not self._monsters_found:
                self._map = self._map.T # transpose and re-search
                self._scan_for_monster()
                # if still no monster found rotate the map
                if not self._monsters_found:
                    self._map = np.rot90(self._map)
                else:
                    break
            else:
                break
    
    def print_puzzle(self):
        for line in self._map:
            print("".join(line))
    
    def count_safe_water(self):
        # counts the '#' in map that ar no longer monsters
        return np.sum(self._map == '#')
        


def part2(assembler):
    solved_puzzle = assembler.puzzle # load the solved puzzle
    hunter = MonsterHunter(solved_puzzle)
    return hunter.count_safe_water()

def part1(assembler):
    # corners should have two edges
    return np.prod(assembler.corners)

if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[1] / "inputs" / "day20.txt"
    parser = PuzzleParser(input_file)
    assembler = PuzzleAssembler(parser.pieces)
    part1_soln = part1(assembler)
    print(f"Part 1 Soluction: {part1_soln}")
    part2_soln = part2(assembler)
    print(f"Part 2 Soluction: {part2_soln}")


