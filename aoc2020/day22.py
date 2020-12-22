from pathlib import Path
import re
from collections import deque
import copy

class PuzzleParser(object):
    card_value_match = re.compile("([0-9]+)")
    def __init__(self, input_file, *arge, **kwargs):
        self._deck1 = deque() # array to hold rules
        self._deck2 = deque() # all other tickets in the input

        self._parse_input(input_file) # parse the input file
    
    def _parse_input(self, input_file):
        with open(input_file) as fii:
            # iterate over all non-empty lines and apply the state machine
            active_deck = self._deck1
            for line in fii:
                if line.strip():
                    match = PuzzleParser.card_value_match.match(line)
                    if match:
                        active_deck.append(int(match.group(1)))
                    else:
                        if "Player 2" in line:
                            # change the active deck
                            active_deck = self._deck2
    
    @property
    def decks(self):
        return self._deck1, self._deck2

class AutoCombat(object):
    def __init__(self, deck1, deck2):
        self._deck1 = copy.copy(deck1)
        self._deck2 = copy.copy(deck2) 
        self._winner = 0 # by default there's no winner
        self._game_exhausted = False
           
    def turn(self):
        # play a turn, pop the top card off and the winner keeps both
        cards_to_play = [x.popleft() for x in (self._deck1, self._deck2)]
        if cards_to_play[0] > cards_to_play[1]:
            [self._deck1.append(x) for x in cards_to_play]
        else:
            [self._deck2.append(x) for x in cards_to_play[::-1]]
    
    def play_game(self):
        # play until somebody loses cards
        while not self._game_exhausted:
            self.turn()
            self._game_exhausted = not (self._deck1 and self._deck2)
        if self._game_exhausted: # if teh game ended from lack of cards       
            self._winner = 2 if self.calculate_scores()[0] == 0 else 1

    def calculate_scores(self):
        scores=[]
        for deck in self.decks:
            score = 0
            for j,card in enumerate(deck):
                score+=card*(len(deck)-j)
            scores.append(score)
        return scores
    
    @property
    def decks(self):
        return self._deck1, self._deck2
    
    @property
    def winner(self):
        return self._winner

class RecursiveCombat(AutoCombat):
    n_instances = 0

    @classmethod
    def get_id(cls):
        cls.n_instances +=1 
        return cls.n_instances

    def __init__(self, *args,**kwargs):
        self._round = 1
        self._id = RecursiveCombat.get_id() # assign an id to keep track of how many recursive combats are happening
        self._deck_history = set() # this is a set of hashes that have been played in this deck
        self._game_recursed = False
        self._verbose = kwargs.pop('verbose',False)
        super().__init__(*args, **kwargs)

    def play_game(self):
        # play until somebody loses cards
        while not self._game_exhausted and not self._game_recursed:
            self.turn()
            self._game_exhausted = not (self._deck1 and self._deck2)
        if self._game_exhausted: # if teh game ended from lack of cards
            self._winner = 1 if self._deck1 else 2
    
    @staticmethod
    def make_subdeck(deck,length):
        return deque(list(deck)[:length])

    def turn(self):
        # print(self.decks)
        # play a turn, pop the top card off and the winner keeps both
        game_state = str(tuple(self._deck1)) + str(tuple(self._deck2))
        # print(game_state)
        if game_state in self._deck_history: # if the hand has been played before player 1 automatically wins
            if self._verbose:
                print("Recursed!")
            self._game_recursed = True 
            self._winner = 1
        else:
            if self._verbose:
                print(f"current decks")
                print("\t"+ ', '.join([str(x) for x in self.decks[0]]))
                print("\t"+ ', '.join([str(x) for x in self.decks[1]]))
            self._deck_history.add(game_state) # add this state into history
            cards_to_play = [x.popleft() for x in (self._deck1, self._deck2)]
            # if each player has more cards in their hand than the value of their popped cards the victory is found recursively
            this_winner = 0
            if (len(self._deck1)>=cards_to_play[0]) and (len(self._deck2) >= cards_to_play[1]):

                subdecks = [self.make_subdeck(deck,length) for deck,length in zip(self.decks,cards_to_play)]
                new_combat = RecursiveCombat(*subdecks)
                # print(f"entering {new_combat.id}")
                new_combat.play_game()
                # print(f"exiting {new_combat.id}, player {new_combat.winner} won")
                this_winner = new_combat.winner # the winner of the round is the one who won the recursive combat
                # print(f"Player {this_winner} won")

            # otherwise it's just a normal match of combat
            else:
                this_winner = 1 if cards_to_play[0] > cards_to_play[1] else 2
            if self._verbose:
                print(f"Player {this_winner} won round {self._round} of game {self._id}, cards on line : {cards_to_play}")
                print()
            # put the cards on the appropriate winners deck so the game can continue
            if this_winner == 1:
                [self._deck1.append(x) for x in cards_to_play]
            elif this_winner == 2:
                [self._deck2.append(x) for x in cards_to_play[::-1]]
            else:
                raise ValueError(f"Invalid winner {this_winner}")

        self._round +=1 # inrement the round

    @property
    def id(self):
        return self._id

def part1(parser):
    player = AutoCombat(*parser.decks)
    player.play_game()
    return player.calculate_scores()[player.winner-1]

def part2(parser):
    player = RecursiveCombat(*parser.decks)
    player.play_game()
    return player.calculate_scores()[player.winner-1]

if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[1] / "inputs" / "day22.txt"
    parser = PuzzleParser(input_file)
    part1_answer = part1(parser)
    print(f"Part 1 Solution {part1_answer}")
    part2_answer = part2(parser)
    print(f"Part 2 Solution {part2_answer}")
