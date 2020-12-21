from pathlib import Path
import re
import enum


class PuzzleParser(object):
    number_regex = re.compile(r"([0-9]+)") # regex to match any number
    rule_regex = re.compile(r"([0-9]+): (.*)$") # regex to extract rule


    def __init__(self, input_file, *arge, **kwargs):
        self._rules = {} # array to hold rules
        self._inputs = [] # all other tickets in the input

        self._parse_input(input_file) # parse the input file
        self._flatten_rules()
    
    def _parse_input(self, input_file):
        with open(input_file) as fii:
            # iterate over all non-empty lines and apply the state machine
            for line in fii:
                if line.strip():
                # if we're in rules state apply the regex and append to the rules array
                    match = PuzzleParser.rule_regex.match(line)
                    if match:
                        key = match.group(1)
                        value = match.group(2)
                        self._rules[key] = value
                    else:
                        self._inputs.append(line.rstrip('\n'))
    
    # flattens rules by iteration
    def _flatten_rules(self):
        for key in self._rules.keys():
            self._rules[key],n_subs = PuzzleParser.number_regex.subn(self._flatten_function, self._rules[key])
            # loop until there's no more substitutions
            while n_subs: 
                self._rules[key],n_subs = PuzzleParser.number_regex.subn(self._flatten_function, self._rules[key])
            
            # now remove the quotes and spaces to get a usable regex
            self._rules[key] = re.sub(r"[\" ]","",self._rules[key])



    # Function that's called when a substition occurs for flattening regex
    # returns the string value for the rules
    def _flatten_function(self, re_match): 
        key = re_match.group(1)
        return "(?:"+self._rules[key]+")"

    @property
    def rules(self):
        return self._rules

    @property
    def inputs(self):
        return self._inputs

def part1(parser):
    """
    count the number of imputs that complete match rule zero
    """
    rule_count = 0
    for line in parser.inputs:
        match = re.match("^"+parser.rules['0']+"$", line)
        if match:
            rule_count+=1
    return rule_count

def part2_matches(parser):
    # see how many entries end with rule 31
    # and start with rule 42, don't care right now about the inbetween
    re_filter = re.compile("^((?:"+parser.rules['42']+"){2,})((?:"+parser.rules['31']+")+)$")
    lines = []
    for line in parser.inputs:
        # if we have a match make sure that there's more 42 matches than 31
        match = re_filter.match(line)
        if match:
            n_42 = len(re.findall(parser.rules['42'], match.group(1)))
            n_31 = len(re.findall(parser.rules['31'], match.group(2)))
            print(f"{n_42},{n_31}\t{line}")
            if n_42>n_31:
                lines.append(line)
    return lines


def part2(parser):
    return len(part2_matches(parser))


if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[1] / "inputs" / "day19.txt"
    parser = PuzzleParser(input_file)
    part1_answer = part1(parser)
    print(f"Part 1 Solution: {part1_answer}")
    part2_answer = part2(parser)
    print(f"Part 1 Solution: {part2_answer}")

