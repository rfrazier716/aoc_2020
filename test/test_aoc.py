import unittest
from aoc2020 import day1,day2,day3,day4,day5,day6,day7, day8, day9,day10, day11, day12, day13, day14, day16
import aoc2020
import numpy as np
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

class TestDay11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input = test_input_dir / "day11_test_input.txt"

    def test_node(self):
        # make a dummy node
        node = day11.FerryNode((0,0),True)
        # set some neighbors
        for j in range(7):
            node.neighbors[j] = True
            self.assertEqual(node.n_neighbors,j+1)

    def test_node_generation(self):
        nodes = day11.gen_ferry_node_array(TestDay11.test_input)
        self.assertTrue(len(nodes),10)
        for row in nodes:
            self.assertEqual(len(row),10)
            for node in row:
                self.assertFalse(node._occupied)
        
        # check that the seats are filled accordingly
        expected_seat_map = (True,False,True,True,True,True,True,False,True,True)
        for expected,actual in zip(expected_seat_map,nodes[-1]):
            self.assertEqual(expected,actual.seat)
      
    def test_neighbors_right_left(self):
        nodes = day11.gen_ferry_node_array(TestDay11.test_input)
        sub_nodes = nodes[:1] # only look at the first row
        # occupy a couple seats to modify to look like L.#L.L#.LL
        sub_nodes[0][2].occupy()
        sub_nodes[0][6].occupy()

        day11.count_LOS_neighbors(sub_nodes)
        # for neighbors to the right expected output is [T F F F F F T F F F]
        # for neighbors to the Left expected output is  [F F F T F F F F T F]
        expected_right_neighbors = (True, *[False for _ in range(4)], True, *[False for _ in range(4)])
        for j,(expected,actual) in enumerate(zip(expected_right_neighbors, sub_nodes[0])):
            self.assertEqual(expected,actual.neighbors[4],f"Sample {j} failed\n{actual.neighbors}")

        expected_left_neighbors = (*[False for _ in range(3)], True, *[False for _ in range(4)], True)
        for j,(expected,actual) in enumerate(zip(expected_left_neighbors, sub_nodes[0])):
            self.assertEqual(expected,actual.neighbors[3],f"Sample {j} failed\n{actual.neighbors}")

    def test_neighbors_up_down(self):
        nodes = day11.gen_ferry_node_array(TestDay11.test_input)
        # occupy left most column with a couple of people
        # should resemble LL#LLL.#LL
        nodes[2][0].occupy()
        nodes[7][0].occupy()

        day11.count_LOS_neighbors(nodes)
        # for neighbors up expected output is [F F F T F F F F T F]
        # for neighbors down expected output is [F T F F F T F F F F]
        expected_up_neighbors = (*[False for _ in range(3)], True, *[False for _ in range(4)], True, False)
        for j,expected in enumerate(expected_up_neighbors):
            self.assertEqual(nodes[j][0].neighbors[1],expected,f"{j} failed with neighbors {nodes[j][0].neighbors}")

        expected_down_neighbors = (False, True, *[False for _ in range(3)], True, *[False for _ in range(4)])
        for j,expected in enumerate(expected_down_neighbors):
            self.assertEqual(nodes[j][0].neighbors[6],expected,f"{j} failed with neighbors {nodes[j][0].neighbors}")

    def test_neighbors_r_diag(self):
        nodes = day11.gen_ferry_node_array(TestDay11.test_input)
        # occupy left most column with a couple of people
        # should resemble L L # L . L . # . L
        nodes[2][2].occupy()
        nodes[7][7].occupy()

        day11.count_LOS_neighbors(nodes)
        expected_r_diag_down_neighbors = (False, True, *[False for _ in range(3)], True, *[False for _ in range(4)])
        for j,expected in enumerate(expected_r_diag_down_neighbors):
            self.assertEqual(nodes[j][j].neighbors[7],expected,f"{j} failed with neighbors {nodes[j][0].neighbors}")

        expected_r_diag_up_neighbors = (*[False for _ in range(3)], True, *[False for _ in range(5)], True)
        for j,expected in enumerate(expected_r_diag_up_neighbors):
            self.assertEqual(nodes[j][j].neighbors[0],expected,f"{j} failed with neighbors {nodes[j][j].neighbors}")

    def test_neighbors_l_diag(self):
        nodes = day11.gen_ferry_node_array(TestDay11.test_input)
        # occupy left most column with a couple of people & right most column
        # should resemble LL#LLL.#LL
        nodes[2][0].occupy()
        nodes[4][0].occupy()
        nodes[3][-1].occupy()
        nodes[5][-1].occupy()
  

        day11.count_LOS_neighbors(nodes)

        expected_l_diag_down_neighbors = (False, True, False, True, *[False for _ in range(6)])
        for j,expected in enumerate(expected_l_diag_down_neighbors):
            self.assertEqual(nodes[j][1].neighbors[5], expected,f"{j} failed with neighbors {nodes[j][1].neighbors}")
        
        # checking the up right test
        expected_l_diag_up_neighbors = (*[False for _ in range(4)], True, *[False for _ in range(5)])
        for j,expected in enumerate(expected_l_diag_up_neighbors):
            self.assertEqual(nodes[j][-2].neighbors[2], expected, f"{j} failed with neighbors {nodes[j][-2].neighbors}")

        self.assertTrue(nodes[7][-3].neighbors[2])


    def test_part_2(self):
        nodes = day11.gen_ferry_node_array(TestDay11.test_input)
        # count and update the neighbors and check the 1st row
        day11.count_LOS_neighbors(nodes)
        # expected output #######.##
        expected_occupied = (*[True for _ in range(7)], False, True, True)
        for j,(expected,actual) in enumerate(zip(expected_occupied,nodes[1])):
            self.assertEqual(expected, actual.occupied,f"col {j} failed with neighbors {actual.neighbors}")
        
        # now update again and recheck, expect #LLLLLL.LL
        day11.count_LOS_neighbors(nodes)
        expected_occupied = (True, *[False for _ in range(9)])
        for j,(expected,actual) in enumerate(zip(expected_occupied,nodes[1])):
            self.assertEqual(expected, actual.occupied,f"col {j} failed with neighbors {actual.neighbors}")

        # now loop until the output is stable
        output_stable = False
        while(not output_stable):
            output_stable = not day11.count_LOS_neighbors(nodes)
        self.assertEqual(day11.count_occupied_seats(nodes),26)

        # now we check the function that does all this 
        self.assertEqual(day11.part2(TestDay11.test_input),26)

class TestDay12(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input = test_input_dir / "day12_test_input.txt"

    def test_boat(self):
        boat = day12.Boat()
        # check that the direction initializes
        self.assertEqual(boat._direction[0],1)
        self.assertEqual(boat._direction[1],0)

        # check rotation 
        boat.move("L180")
        self.assertTrue(np.all(boat._direction==[-1,0]))

        boat.move("R180")
        self.assertTrue(np.all(boat._direction==[1,0]))

        boat.move("R90")
        self.assertTrue(np.all(boat._direction==[0,-1]))

        boat.move("F10")
        self.assertTrue(np.all(boat._position==[0,-10]))
        boat.move("R180")
        boat.move("F10")
        self.assertTrue(np.all(boat._position==[0,0]))

        expected_positions = ((0,1),(0,0),(-1,0),(0,0))
        for expected, direction in zip(expected_positions,"NSWE"):
            boat.move(f"{direction}1")
            self.assertTrue(np.all(boat._position==expected), f"Failed for moving {direction}")
    
    def test_part1(self):
        test_answer = day12.part1(TestDay12.test_input)
        self.assertEqual(test_answer,25)
    
    def test_part2(self):
        test_answer = day12.part2(TestDay12.test_input)
        self.assertEqual(test_answer,286)

class TestDay13(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input = test_input_dir / "day13_test_input.txt" 
    
    def test_timetable_loading(self):
        departure,timetable,gaps = day13.parse_puzzle_input(TestDay13.test_input)
        self.assertEqual(departure,939)
        self.assertTrue(np.all(timetable==[7,13,59,31,19]))
        self.assertTrue(np.all(gaps == [1,3,2,1]))

    def test_part1(self):
        departure,timetable,_ = day13.parse_puzzle_input(TestDay13.test_input)
        part1_answer = day13.part1(departure,timetable)
        self.assertEqual(part1_answer, 295)

    def test_part2(self):
        departure,timetable, gaps = day13.parse_puzzle_input(TestDay13.test_input)
        timetables = [day13.Timetable(0,x) for x in timetable] 
        part2_answer = day13.part2(timetables, gaps)
        self.assertEqual(part2_answer, 1068781)

class TestDay14(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input = test_input_dir / "day14_test_input.txt" 
    
    def test_part1(self):
        part1_ans = day14.part1(TestDay14.test_input)
        self.assertEqual(part1_ans,165)

    def test_mem_bitmasker(self):
        masker = day14.MemoryBitMasker()
        with open(TestDay14.test_input) as fii:
            # first line should update the mask
            masker.update(fii.readline())
            self.assertEqual(len(masker._mask_toggle_indices),34)
            self.assertTrue(1 not in masker._mask_toggle_indices)
            self.assertTrue(6 not in masker._mask_toggle_indices)

    def test_part_2(self):
        part2_ans = day14.part2(test_input_dir / "day14_test_input2.txt")
        self.assertEqual(part2_ans,208)

class TestDay16(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_input = test_input_dir / "day16_test_input.txt" 

    def test_parser(self):
        parser = day16.PuzzleParser(TestDay16.test_input)
        # parser should set the ticket class to have 3 ticket field functions
        self.assertEqual(len(day16.Ticket.ticket_fields),3)
        self.assertTrue(np.all(parser.my_ticket._field_validation_matrix[0] == [True, True, False]))

        # check that the validation function works
        expected_output = [True, False, False, False]
        for j,(expected, actual) in enumerate(zip(expected_output, parser.other_tickets)):
            self.assertEqual(expected,actual.is_valid(),f"ticket {j} failed with matrix \n {actual._field_validation_matrix}")

    def test_part1(self):
        parser = day16.PuzzleParser(TestDay16.test_input)
        part1_answer = day16.part1(parser.other_tickets)
        self.assertEqual(part1_answer,71)

    def test_ticket_solver(self):
        parser = day16.PuzzleParser(test_input_dir / "day16_test_input2.txt")
        all_solutions_matrix = np.array(
            [ticket.field_validation_matrix for ticket in parser.other_tickets if ticket.is_valid()])
        solver = day16.TicketSolver(parser.other_tickets)
        solver.solve()
        print(solver.ordered_fields)
        print(parser.my_ticket.values)


if __name__ == '__main__':
    unittest.main()