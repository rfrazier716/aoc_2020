from pathlib import Path
import re
from recordtype import recordtype

# make a regex to search instruction strings
instruction_parse_r = r"^([a-z]{3}) ([+-][0-9]+)$"
instruction_parse_prog = re.compile(instruction_parse_r) 

# a named tuple to hold the instructions
GameBoyASSY = recordtype('GameBoyASSY',['opcode','value','count'], default = 0)

# a gameboy class to run the imported "code"
class GameBoy(object):
    def __init__(self, memory,*args,**kwargs):
        self._memory = memory.copy() # assign the memory
        self._program_counter = 0 # the current program counter
        self._accumulator = 0
        self._pc_stack = []
    
    def reset(self):
        """
        resets the PC
        """
        self._program_counter = 0
        self._accumulator = 0
    
    def run_to_loop(self):
        """
        runs until it find the first instruction that's already been executed
        """
        while(self._memory[self._program_counter].count == 0):
            self.step()
        
    def step(self):
        self._pc_stack.append(self._program_counter)
        instruction = self._memory[self._program_counter]
        instruction.count+=1 # increment the count
        self.execute_instruction(instruction)

    
    def execute_instruction(self, instruction):
        if instruction.opcode == 'jmp':
            self._program_counter += instruction.value
        elif instruction.opcode == 'acc':
            self._accumulator += instruction.value
            self._program_counter+=1
        elif instruction.opcode == 'nop':
            self._program_counter+=1
        else:
            raise ValueError(f"operation {opcode} is not a valid operation at memory address {self._program_counter}")

    @property
    def accumulator(self):
        return self._accumulator

    @property
    def program_counter(self):
        return self._program_counter

    @property
    def pc_stack(self):
        return self._pc_stack

def parse_input_string(input_string):
    """
    parses the input line, returning a GameBoyASSY object holding the instruction
    """
    match = instruction_parse_prog.match(input_string) # get a match object for the string
    if match:
        opcode = match.group(1)
        value = int(match.group(2))
        return GameBoyASSY(opcode, value)
    else:
        raise ValueError(f"{input_string} does not match regex")

def part1(memory):
    gameboy = GameBoy(memory)
    gameboy.run_to_loop()
    print(gameboy.pc_stack)
    return gameboy.accumulator

if __name__ == '__main__':
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day8.txt"
    gameboy_memory = {} # make an empty dict to act as the gameboy's memory
    with open(input_file) as fii:
        for j,line in enumerate(fii):
            # make an instruction from the gameboy line
            gameboy_memory[j] = parse_input_string(line)
    
    part1_answer = part1(gameboy_memory)
    print(f"Part 1 Solution: {part1_answer}")
    

