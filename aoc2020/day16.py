import re
from collections import namedtuple
import enum
import numpy as np
from pathlib import Path

# make a ticket field object that holds the field name and function to validete
TicketField = namedtuple("PuzzleRule",["name","fn"])

# a ticket holds all the ticketFields, list of inputs, and a 2D array of if each field applies to a rule
class Ticket(object):
    """
    field values is the ordered list of values on the ticket
    """
    ticket_fields = []
    def __init__(self, field_values,*args, **kwargs):
        # load the field values
        self._field_values = np.array(field_values)

        # an array to track which rules a field value follows
        self._field_validation_matrix = np.zeros((len(self._field_values),len(Ticket.ticket_fields))).astype(bool)
        self._fill_matrix()

    @classmethod
    def update_ticket_fields(cls, field_array):
        cls.ticket_fields = field_array

    def _fill_matrix(self):
        # apply the rules on the input values
        for j,field_value in enumerate(self._field_values):
            self._field_validation_matrix[j] = [field.fn(field_value) for field in Ticket.ticket_fields]
    
    def _get_valid_fields(self):
        """
        returns a bool array of which field values don't apply to any rule
        """
        return np.any(self._field_validation_matrix, axis=1)

    def is_valid(self):
        """
        returns a boolean if every ticket value can apply to at least one field
        """
        return np.all(self._get_valid_fields())

    def invalid_sum(self):
        """
        returns the sum of invalid fields
        """
        return np.sum(self._field_values[np.logical_not(self._get_valid_fields())])

def rule_validation_generator(min_1, max_1, min_2, max_2):
    """
    returns a function that's true if the input is in the range otherwise false
    """
    return lambda x: (x>=min_1 and x<=max_1) or (x>=min_2 and x<=max_2)
        


# an enum to keep track of the state machine for the parser
class ParserState(enum.Enum):
    RULES = 1
    MY_TICKET = 2
    ALL_TICKETS = 3

class PuzzleParser(object):
    rule_regex = re.compile(r"([a-z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)")

    def __init__(self, input_file, *arge, **kwargs):
        self._state = ParserState.RULES # initially we're searching for rules
        self._rules = [] # array to hold rules
        self._my_ticket = None # the owners ticket
        self._other_tickets = [] # all other tickets in the input

        self._parse_input(input_file) # parse the input file
    
    def _parse_input(self, input_file):
        with open(input_file) as fii:
            # iterate over all non-empty lines and apply the state machine
            for line in fii:
                if line.strip(): # if the line's nonempty
                    # if we're in rules state apply the regex and append to the rules array
                    if self._state == ParserState.RULES:
                        # check if the line we popped causes a state switch
                        if "your ticket:" in line:
                            self._state = ParserState.MY_TICKET
                            # since we're done with all the rules update the Ticket class method
                            Ticket.update_ticket_fields(self._rules)

                        #otherwise generate a new rule
                        else:
                            rule_match = PuzzleParser.rule_regex.match(line)
                            
                            # if there's a match make a new Ticket Field object and add it to the rules list
                            if rule_match:
                                name = rule_match.group(1)
                                range_fields = [int(rule_match.group(x)) for x in range(2,6)]
                                self._rules.append(TicketField(name, rule_validation_generator(*range_fields)))
                            else:
                                raise ValueError(f"{line} does not match rule regex")

                    # if we're parsing your ticket split it from the commas and make a new ticket object
                    elif self._state == ParserState.MY_TICKET:
                        if "nearby tickets:" in line:
                            self._state = ParserState.ALL_TICKETS
                        else:
                            ticket_values = [int(x) for x in line.split(',')]
                            self._my_ticket = Ticket(ticket_values)
                    
                    # finally if we're in the all_tickets field, append it to the all tickets array
                    elif self._state == ParserState.ALL_TICKETS:
                        ticket_values = [int(x) for x in line.split(',')]
                        self._other_tickets.append(Ticket(ticket_values))

    @property
    def rules(self):
        return self._rules

    @property
    def my_ticket(self):
        return self._my_ticket

    @property
    def other_tickets(self):
        return self._other_tickets


def part1(other_tickets):
    total_sum = 0
    for ticket in other_tickets:
        if not ticket.is_valid():
            total_sum += ticket.invalid_sum()
    return total_sum


if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[1] / "inputs" / "day16.txt"
    parser = PuzzleParser(input_file)
    part1_soln = part1(parser.other_tickets)
    print(f"part 1 solution: {part1_soln}")
