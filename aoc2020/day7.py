from pathlib import Path #for file import 
import networkx as nx # for building the graph
from collections import namedtuple
import re

bag_string_r = r"([0-9]*) ?([a-z]+ [a-z]+) bags?" # regex string to find bags
bag_string_prog = re.compile(bag_string_r) # compile it to a regex

Bag = namedtuple("Bag",['color','quantity'])

def parse_bag_string(bag_string):
    """
    parses a bag string to extract the parent bag and the sub-bags, returns an array of the extracted bag strings
    """
    bags = [] # make an empty array of bags
    matches = bag_string_prog.findall(bag_string)
    if not matches:
        raise ValueError(f"{bag_string} does not have a regex match")

    for match in matches:
        if "no other" not in match[1]: #disqualify that piece of regex that's matching a no other bag string
            bags.append(Bag(match[1], int(match[0]) if match[0] else 0))

    return bags # return the array of bags

def append_bags_to_graph(graph: nx.DiGraph, bags):
    """
    takes a bag relationship line (tuple of bag objects) and builds it into the graph
    """
    for j,bag in enumerate(bags):
        graph.add_node(bag.color) # add the bag color as a node
        if j!=0: # if we're one of the child bags add an edge connecting it to the parent
            graph.add_edge(bags[0].color,bag.color,count=bag.quantity)


def part_1_solution(graph, search_key):
    """
    Performs a lexographical sort of the graph and finds how many upper level nodes can reach 
    the target node
    """
    connected_nodes = 0
    for j,node in enumerate(nx.algorithms.dag.topological_sort(graph)):
        if node == search_key:
            return connected_nodes
        else:
            connected_nodes += 1 if nx.has_path(graph, node, search_key) else 0
    
    return None # return none if issue finding key

def _part_2_helper(graph, current_node, branch_product, counter):
    """
    perform a depth first search of the tree, accumlating the counter for every bag
    """
    for u,v in graph.out_edges(current_node):
        count = graph[u][v]['count']
        # print(f"{u}\t{v}: {count}, {counter[0]}, {branch_product*count}") # for debug
        _part_2_helper(graph, v, branch_product*count, counter) # recall the helper func
    counter[0] += branch_product # increment the counter with the total product for the branch
        


def part_2_solution(graph, search_key):
    """
    keeps a persistant counter that is recursively passed into a helper function
    for ever depth of the helper function, the branch product gets updated, when a recursive function 
    exits it updates the counter with the product of counts for each sub-bag

    the counter is an array with one entry so that it's passed by reference, somewhat annoying but not
    sure how else to do it.
    """
    counter=[0]
    branch_product = 1
    _part_2_helper(graph, search_key, branch_product, counter)
    # we have to reduce the overall result by 1 since the initial bag is counted in the branch product
    return counter[0]-1
    

if __name__ == "__main__":
    # import the file
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day7.txt"
    graph = nx.DiGraph()
    with open(input_file) as fii:
        for line in fii:
            # parse the bag string
            bags = parse_bag_string(line)
            append_bags_to_graph(graph,bags)
    part_1_answer = part_1_solution(graph,'shiny gold')
    print(f"Part 1 Solution: {part_1_answer}")
    part2_answer = part_2_solution(graph,'shiny gold')
    print(f"Part 2 Solution: {part2_answer}")
    # build a graph for the file
    # for every line 