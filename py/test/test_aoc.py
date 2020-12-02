import unittest
from aoc2020 import day1,day2


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

if __name__ == '__main__':
    unittest.main()