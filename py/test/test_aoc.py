import unittest
from aoc2020 import day1,day2,day3,day4


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

if __name__ == '__main__':
    unittest.main()