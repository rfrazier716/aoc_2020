from pathlib import Path #for file import 
import networkx as nx # for building the graph
from collections import namedtuple
import re

bag_string_r= r"^([a-z ]+)bags contain (?:([0-9]+) ([a-z ]+) bags?(?:, )?)(?:([0-9]+) ([a-z ]+) bags?)?" # regex string for bags
bag_string_prog = re.compile(bag_string_r) # compile it to a regex

Bag = namedtuple("Bag",['color','quantity'])

def parse_bag_string(bag_string):
    """
    parses a bag string to extract the parent bag and the sub-bags, returns an array of the extracted bag strings
    """
    match = bag_string_prog.match(bag_string)
    print(match.group(1))
    for quantity,color in zip(match.groups()[1::2],match.groups()[2::2]):
        print(f"{color}\t{quantity}")


if __name__ == "__main__":
    # import the file
    # build a graph for the file
    # for every line 
    parse_bag_string("light red bags contain 1 bright white bag, 2 muted yellow bags.")