from pathlib import Path
from collections import defaultdict
import re
import itertools
import numpy as np


class BitMasker(object):
    instruction_regex = re.compile(r"((?:mask)|(?:mem))(?:\[([0-9]+)\])? = ([0-9X]+)")
    def __init__(self, *args,**kwargs):
        # make a mask for OR and AND
        self._or_mask = 0x00
        self._and_mask = 0x00
        self._memory = defaultdict(int)
        # call parent class constructor
        super().__init__(*args,**kwargs)

    def update(self, input_line):
        match = BitMasker.instruction_regex.match(input_line)
        if match.group(1) == 'mask':
            self._update_mask(match.group(3))
        elif match.group(1) == 'mem':
            self._write_memory(int(match.group(2)),int(match.group(3)))

    def _update_mask(self, mask_string):
        # replace all the x's with 0's, this is the or mask
        self._or_mask = int(mask_string.replace('X','0'),2)

        # the and mask replace the x's with 1's 
        self._and_mask = int(mask_string.replace('X','1'),2)
    
    def _mask_value(self, value):
        return (self._or_mask | value) & (self._and_mask)

    def _write_memory(self, address, value):
        # apply the mask and write to memory
        self._memory[address] = self._mask_value(value)

    @property 
    def memory(self):
        return self._memory   

class MemoryBitMasker(BitMasker):
    """
    Memory Bitmasker inherits from BitMasker but has different mask instructions
    """
    def __init__(self,*args,**kwargs):
        self._mask_toggle_indices = []
        super().__init__(*args,**kwargs) # call the parent constructor

    def _update_mask(self,mask_string):
        # replace all the x's with 0's, this is the or mask
        self._or_mask = int(mask_string.replace('X','0'),2)

        #also need to keep track of where the bits can flip
        self._mask_toggle_indices = [len(mask_string)-1-j for j,char in enumerate(mask_string) if char=="X"]
        self._mask_bit_clear = ~ np.sum([1<<shift for shift in self._mask_toggle_indices]) # this is used to set the value of the 
        # toggle indices to zero so they can be OR'd later

    def _write_memory(self, address, value):
        """
        writes to all possible memory addresses as set by the bit toggle
        """

        # make a new variable which is the address with the fields to toggle blanked
        blanked_address = address & self._mask_bit_clear
        for bit_shifts in itertools.product(*[[0,1] for _ in range(len(self._mask_toggle_indices))]):
            toggled_mask = np.sum([bit<<shift for bit,shift in zip(bit_shifts, self._mask_toggle_indices)]) | (self._or_mask | blanked_address)
            self._memory[toggled_mask] = value # update the togggled memory address with the value

def part2(input_file):
    masker = MemoryBitMasker()
    with open(input_file) as fii:
        for line in fii:
            masker.update(line)
    sum = 0
    for value in masker.memory.values():
        sum+=value
    return sum

def part1(input_file):
    masker = BitMasker()
    with open(input_file) as fii:
        for line in fii:
            masker.update(line)

    sum = 0
    for value in masker.memory.values():
        sum+=value
    return sum

if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day14.txt"
    part1_soln = part1(input_file)
    print(f"Part 1 Solution: {part1_soln}")

    part2_soln = part2(input_file)
    print(f"Part 2 Solution: {part2_soln}")
