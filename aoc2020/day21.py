from pathlib import Path
from collections import namedtuple, defaultdict
import re
import numpy as np

# a tuple for holding the ingredient information
Foodstuff = namedtuple("Foodstuff", ["ingredients","allergens"])

class PuzzleParser(object):
    food_regex = re.compile(r"([a-z ]+) \(contains ([a-z, ]+)\)")

    def __init__(self, input_file, *arge, **kwargs):
        self._foodstuffs = [] # array to hold rules
        self._ingredients = set()
        self._allergens = set()
        self._potential_pairings = {} # a dictionary with allergens as keys and a set of potential ingredients as values

        # parse the input
        self._parse_input(input_file)
    
    
    def _parse_input(self, input_file):
        with open(input_file) as fii:
            # iterate over all non-empty lines and fill a foodstuff
            for line in fii:
                if line.strip():
                    match = PuzzleParser.food_regex.match(line)
                    if match:
                        ingredients = match.group(1).split(" ")
                        allergens = match.group(2).split(", ")
                        foodstuff = Foodstuff(ingredients, allergens)
                        self._foodstuffs.append(foodstuff)
                        self._ingredients.update(ingredients)
                        self._allergens.update(allergens)

                        # now update the potential pairings
                        self._update_allergen_pairings(foodstuff)
                    else:
                        raise ValueError(f"{line} is not a valid foodstuff")
    
    def _update_allergen_pairings(self, foodstuff):
        for allergen in foodstuff.allergens:
            allergen_set = self._potential_pairings.get(allergen, None)
            if allergen_set:
                self._potential_pairings[allergen] = allergen_set.intersection(foodstuff.ingredients)
            else:
                self._potential_pairings[allergen] = set(foodstuff.ingredients)

    @property
    def ingredients(self):
        return self._ingredients

    @property
    def allergens(self):
        return self._allergens

    @property
    def foodstuffs(self):
        return self._foodstuffs
    
    @property
    def pairings(self):
        return self._potential_pairings

class AllergenSolver(object):
    def __init__(self, parser, *args, **kwargs):
        self._parser = parser
        self._solved_allergens = {} # a holder for the solved allergens

        self._fill_solution_space()
        self.solve()
        super().__init__(*args, **kwargs)

    def solve(self):
        # iterate over solution space and find rows where there's only one possible ingredient
        row_sums = np.sum(self._solution_space, axis=1)
        # loop until the solution space is all zeros
        while np.any(row_sums):
            # take all the rows that sum to 1 
            single_solution_rows = np.where(row_sums == 1)[0] # get index where there is only one potential solution
            for index in single_solution_rows:
                column = np.where(self._solution_space[index] == 1)[0][0] # the column of the ingredient solution
                ingredient = self._ingredient_lut_inv[column]
                allergen = self._allergen_lut_inv[index]
                self._solved_allergens[allergen] = ingredient

                # now blank out that column because no other allergen can hold that ingredient
                self._solution_space[:,column] = np.zeros(self._solution_space.shape[1])

            # re-prime the loop for the exit condition
            row_sums = np.sum(self._solution_space, axis=1)

    @property
    def solved_allergens(self):
        return self._solved_allergens           

    
    def _fill_solution_space(self):
        potential_ingredients = set().union(*[ingredients for ingredients in parser.pairings.values()])
        self._allergen_lut = {val: j for j,val in enumerate(self._parser.pairings.keys())}
        self._allergen_lut_inv = {val: key for key, val in self._allergen_lut.items()}
        self._ingredient_lut = {val: j for j,val in enumerate(potential_ingredients)}
        self._ingredient_lut_inv = {val: key for key, val in self._ingredient_lut.items()}


        n_allergens = len(self._allergen_lut.keys())
        n_ingredients = len(self._ingredient_lut.keys())
        self._solution_space = np.zeros((n_allergens, n_ingredients)) # an array to hold the solution space

        # now we fill the solution space based on the allergen pairings
        for allergen, ingredients in self._parser.pairings.items():
            i = self._allergen_lut[allergen]
            j = [self._ingredient_lut[ingredient] for ingredient in ingredients]
            self._solution_space[i,j] = np.ones(len(j))

def get_allergen_free_ingredients(parser):
    all_potential_allergens = set().union(*[ingredients for ingredients in parser.pairings.values()])
    ingredients_without_allergens = parser.ingredients - all_potential_allergens
    return ingredients_without_allergens

def part1(parser):
    """
    want how many ingredients cannot have an allergen -- this is the union of all the pairings 
        removed from the set of all ingredients
    """
    # handle all allergens
    allergen_free_ingredients = get_allergen_free_ingredients(parser)
    total_allergen_free_count = 0
    for foodstuff in parser.foodstuffs:
        # subtract the set from the foodstuff ingredient
        total_allergen_free_count += len(foodstuff.ingredients) - len(set(foodstuff.ingredients) - allergen_free_ingredients)
    
    return total_allergen_free_count

def part2(parser):
    # find the allergen-food pairings
    solver = AllergenSolver(parser)
    
    soln_string = ','.join([solver.solved_allergens[key] for key in sorted(solver.solved_allergens.keys())])
    return soln_string
        

if __name__ == "__main__":
    input_file = Path(__file__).resolve().parents[1] / "inputs" / "day21.txt"
    parser = PuzzleParser(input_file)
    part1_answer = part1(parser)
    print(f"Part 1 Solution {part1_answer}")
    part2_answer = part2(parser)
    print(f"Part 2 Solution {part2_answer}")
