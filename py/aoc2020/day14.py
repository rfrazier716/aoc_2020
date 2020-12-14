from pathlib import Path
from collections import defaultdict
import re


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
        print(match.group(1))
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

if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day14.txt"
    masker = BitMasker()
    with open(input_file) as fii:
        for line in fii:
            masker.update(line)

    sum = 0
    for value in masker.memory.values():
        sum+=value
    print(sum)
