from pathlib import Path
import re
from recordtype import recordtype
import copy

# make a regex to search instruction strings
instruction_parse_r = r"^([a-z]{3}) ([+-][0-9]+)$"
instruction_parse_prog = re.compile(instruction_parse_r) 

# a named tuple to hold the instructions
GameBoyASSY = recordtype('GameBoyASSY',['opcode','value','count'], default = 0)

# a gameboy class to run the imported "code"
class GameBoy(object):
    def __init__(self, memory,*args,**kwargs):
        self._memory = memory # assign the memory
        self.reset() # reset teh system
    
    def reset(self):
        """
        resets the PC
        """
        self._program_looping = False
        self._program_terminated = False
        self._pc_stack = []
        self._program_counter = 0
        self._accumulator = 0
        for key in self._memory.keys():
            self._memory[key].count = 0
    
    def run_to_loop(self):
        """
        runs until it find the first instruction that's already been executed
        """
        while (not self._program_looping) and (not self._program_terminated):
            self.step()

        
    def step(self):
        self._pc_stack.append(self._program_counter)
        try:
            instruction = self._memory[self._program_counter]
            if instruction.count!=0:
                self._program_looping = True
            else:
                instruction.count+=1 # increment the count
                self.execute_instruction(instruction)
        except KeyError: # if we have a KeyError we've exited the program
            self._program_terminated = True

    
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

    @property
    def program_terminated(self):
        return self._program_terminated

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
    return gameboy.accumulator

def part2(memory):
    # make a new gameboy and run to loop, then pull the PC stack
    gameboy = GameBoy(memory)
    gameboy.run_to_loop()
    pc_stack = gameboy.pc_stack.copy() # do a hard copy since we'll be updating it
    for stack_address in pc_stack:
        tmp_memory = copy.copy(memory[stack_address]) # hold the current memory value
        # for every address that is either jmp or nop, swap the instruction and rerun
        if memory[stack_address].opcode != 'acc':
            opcode = memory[stack_address].opcode
            # swap the opcode
            memory[stack_address].opcode = 'jmp' if (opcode=='nop') else 'nop' 
            # debug print statements
            # print(f"changing stack address {stack_address} to {memory[stack_address].opcode}")
            # print(gameboy._memory)

            # reset and boot up the gameboy
            gameboy.reset()
            gameboy.run_to_loop()
            memory[stack_address] = tmp_memory # reset the memory to it's initial state
            if gameboy.program_terminated: # if the program terminated return the accumulator value
                return gameboy.accumulator
    return None # Return none if the gameboy never found an instruction swap that worked
                
            

if __name__ == '__main__':
    input_file = Path(__file__).resolve().parents[2] / "inputs" / "day8.txt"
    gameboy_memory = {} # make an empty dict to act as the gameboy's memory
    with open(input_file) as fii:
        for j,line in enumerate(fii):
            # make an instruction from the gameboy line
            gameboy_memory[j] = parse_input_string(line)
    
    part1_answer = part1(gameboy_memory)
    print(f"Part 1 Solution: {part1_answer}")

    part2_answer = part2(gameboy_memory)
    print(f"Part 2 Solution: {part2_answer}")
    

