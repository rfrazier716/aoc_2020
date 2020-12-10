import unittest
from aoc2020 import day1,day2,day3,day4,day5,day6,day7, day8, day9,day10
import networkx as nx

from pathlib import Path
test_input_dir = Path(__file__).resolve().parent / "test_inputs"

class TestDay1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input = [1721, 979, 366, 299, 675, 1456]

    def test_part_one_examples(self):
        gen_2020 = day1.find_2020(TestDay1.test_input,2)
        self.assertEqual(next(gen_2020), 514579)
    
    def test_part_two_examples(self):
        gen_2020 = day1.find_2020(TestDay1.test_input,3)
        self.assertEqual(next(gen_2020), 241861950)

class TestDay2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input = ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc","1-3 a: cbade","1-3 a: abade"]

    def test_regex_match(self):
        input = TestDay2.test_input
        res = day2.parse_password_string(input[0])
        self.assertEqual(res.password, "abcde")
        self.assertEqual(res.key, "a")
        self.assertEqual(res.min_occurances, 1)
        self.assertEqual(res.max_occurances, 3)

    def test_password_validation(self):
        expected_results = [True, False, True, True, True]
        for j,input in enumerate(TestDay2.test_input):
            valid_password = day2.validate_password(*day2.parse_password_string(input))
            self.assertEqual(valid_password,expected_results[j])

    def test_password_validation_TCP(self):
        expected_results = [True, False, False, True, False]
        for j,input in enumerate(TestDay2.test_input):
            valid_password = day2.validate_password_TCP(*day2.parse_password_string(input))
            self.assertEqual(valid_password,expected_results[j])

class TestDay3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_input_string ="""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""
        cls.test_input = [line.rstrip('\n') for line in test_input_string.splitlines()]


    def test_tree_detection(self):
        # Checks that you get true returned if a pound sign is in the path
        test_input = TestDay3.test_input
        map_line = test_input[1]

        tree_detection_functional = True
        for j,char in enumerate(map_line):
            tree_detection_functional &= (day3.tree_in_path(map_line,j) == (char == '#'))
        self.assertTrue(tree_detection_functional)
        
    def test_map_navigation(self):
        # tests that map navication returns the correct number of hits
        input = TestDay3.test_input
        slopes_to_test = [[1,1],[3,1],[5,1],[7,1],[1,2]]
        expected_hits = [2,7,3,4,2]
        
        for slope,hits in zip(slopes_to_test,expected_hits):
            self.assertEqual(day3.traverse_map(input,*slope),hits)


class TestDay4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input_string ="""ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

    def test_batch_passport_generator(self):
        # load the test cases
        splitter = day4.batch_passport_splitter(TestDay4.test_input_string.splitlines())
        all_passports=list(splitter)
        
        self.assertEqual(len(all_passports),2)
        self.assertEqual(all_passports[0].cid,"147")
        self.assertEqual(all_passports[1].cid,None)

    def test_passport_validation(self):
        valid_passport_strings = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

        splitter = day4.batch_passport_splitter(valid_passport_strings.splitlines())
        all_passports=list(splitter)
        for passport in all_passports:
            self.assertTrue(day4.year_field_valid(passport.byr,1920,2002))
            self.assertTrue(day4.year_field_valid(passport.iyr,2010,2020))
            self.assertTrue(day4.year_field_valid(passport.eyr,2020,2030))
            self.assertTrue(day4.height_valid(passport.hgt))
            self.assertTrue(day4.hair_color_valid(passport.hcl))
            self.assertTrue(day4.eye_color_valid(passport.ecl))
            self.assertTrue(day4.passport_id_valid(passport.pid))

class TestDay5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_inputs = ["BFFFBBFRRR",
            "FFFBBBFRRR",
            "BBFFBBFRLL"]
    
    def test_part_one_examples(self):
        inputs = TestDay5.test_inputs
        expected_row_columns = ((70,7),(14,7),(102,4))
        for test_string,rc in zip(inputs,expected_row_columns):
            test_r,test_c = day5.bp_string_to_row_col(test_string)
            self.assertEqual(test_r,rc[0])
            self.assertEqual(test_c,rc[1])


class TestDay6(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_string = """abc

a
b
c

ab
ac

a
a
a
a

b"""
        cls.test_inputs = test_string.splitlines()
    def test_set_generator(self):
        inputs = TestDay6.test_inputs
        str_gen = day6.customs_importer(inputs)

        ml_strings=[]
        for _,customs_string in str_gen:
            ml_strings.append(customs_string)

        sets = [set(x) for x in ml_strings]
        expected_lengths = (3,3,3,1,1)
        for j,this_set in enumerate(sets):
            self.assertEqual(len(this_set),expected_lengths[j],ml_strings[j])

class TestDay7(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input = test_input_dir / "day7_test_input.txt"
    
    def test_bag_string_parsing(self):
        expected_bag_lengths = (3,3,2,3,3,3,3,1,1)
        with open(TestDay7.test_input) as fii:
            for line, length in zip(fii,expected_bag_lengths):
                bags = day7.parse_bag_string(line)
                self.assertEqual(len(bags),length)
    
        # now check that specific bags get generated correctlyl
        test_string = "shiny cyan bags contain 4 plaid green bags, 4 dim coral bags, 4 dull indigo bags."
        bags = day7.parse_bag_string(test_string)
        self.assertEqual(bags[0].color, "shiny cyan")
        self.assertEqual(bags[1].color, "plaid green")
        self.assertEqual(bags[2].color, "dim coral")
        self.assertEqual(bags[3].color, "dull indigo")
        self.assertEqual(bags[0].quantity, 0)
        self.assertEqual(bags[1].quantity, 4)
        self.assertEqual(bags[2].quantity, 4)
        self.assertEqual(bags[3].quantity, 4)

        # check for a root bag
        test_string = "dotted black bags contain no other bags."
        bags = day7.parse_bag_string(test_string)
        self.assertEqual(bags[0].color, "dotted black")

    def test_graph_generation(self):
        graph = nx.DiGraph()
        with open(TestDay7.test_input) as fii:
            for line in fii:
                day7.append_bags_to_graph(graph, day7.parse_bag_string(line))
        print(list(nx.algorithms.dag.topological_sort(graph)))

    def test_part1_soln(self):
        graph = nx.DiGraph()
        with open(TestDay7.test_input) as fii:
            for line in fii:
                day7.append_bags_to_graph(graph, day7.parse_bag_string(line))
        self.assertEqual(day7.part_1_solution(graph,"shiny gold"),4)

    def test_part2_soln(self):
        graph = nx.DiGraph()
        with open(TestDay7.test_input) as fii:
            for line in fii:
                day7.append_bags_to_graph(graph, day7.parse_bag_string(line))
        self.assertEqual(day7.part_2_solution(graph,'dark olive'), 7)
        self.assertEqual(day7.part_2_solution(graph,'vibrant plum'), 11)
        self.assertEqual(day7.part_2_solution(graph,'shiny gold'), 32)

class TestDay8(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_input = test_input_dir / "day8_test_input.txt"
        cls.memory = {}
        with open(test_input) as fii:
            for j,line in enumerate(fii):
                # make an instruction from the gameboy line
                cls.memory[j] = day8.parse_input_string(line)
    
    def test_memory_loaded(self):
        memory = TestDay8.memory
        self.assertEqual(len(memory.values()),9)

    def test_opcodes(self):
        gameboy = day8.GameBoy(TestDay8.memory)
        expected_accumulator_values = (0,1,1,2,2,5)
        for test_val in expected_accumulator_values:
            gameboy.step() # step an instruction
            #print(gameboy.accumulator)
            self.assertEqual(gameboy.accumulator, test_val)

    def test_part1_soln(self):
        acc_value = day8.part1(TestDay8.memory)
        self.assertEqual(acc_value, 5)

    def test_part2_soln(self):
        acc_value = day8.part2(TestDay8.memory)
        self.assertEqual(acc_value, 8)

class TestDay9(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input = test_input_dir / "day9_test_input.txt"

    def test_xma_validation(self):
        validation_set = set(range(20))
        self.assertTrue(day9.xma_valid(validation_set,21))
        
        validation_set = set([3,7,8,9,10])
        self.assertFalse(day9.xma_valid(validation_set,6))
        self.assertTrue(day9.xma_valid(validation_set,10))
        self.assertFalse(day9.xma_valid(validation_set,20))
        self.assertTrue(day9.xma_valid(validation_set,16))
        self.assertTrue(day9.xma_valid(validation_set,17))

    def test_part1(self):
        part1_answer = day9.part1_solution(TestDay9.test_input, 5)
        self.assertEqual(part1_answer, 127)

    def test_part1(self):
        part2_answer = day9.part2_solution(TestDay9.test_input, 127)
        self.assertEqual(part2_answer,62)

class TestDay10(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input_short = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
        cls.test_input_long = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49,
             45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]

    def test_part_one(self):
        self.assertEqual(day10.part1(TestDay10.test_input_short),35)

    def test_part_two(self):
        self.assertEqual(day10.part2(TestDay10.test_input_short),8)
        self.assertEqual(day10.part2(TestDay10.test_input_long),19208)


if __name__ == '__main__':
    unittest.main()