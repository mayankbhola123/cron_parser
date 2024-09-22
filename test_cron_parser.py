import unittest
from io import StringIO
import sys
from cron_parser import expand_range, parse_cron_expression, format_output

class TestCronParser(unittest.TestCase):

    def test_expand_range_all_values(self):
        self.assertEqual(expand_range('*', 0, 59), list(range(0, 60)))
        self.assertEqual(expand_range('*', 1, 12), list(range(1, 13)))
    
    def test_expand_range_step(self):
        self.assertEqual(expand_range('*/15', 0, 59), [0, 15, 30, 45])
        self.assertEqual(expand_range('*/5', 0, 23), [0, 5, 10, 15, 20])
    
    def test_expand_range_list(self):
        self.assertEqual(expand_range('1,15', 1, 31), [1, 15])
        self.assertEqual(expand_range('2,3,5', 1, 7), [2, 3, 5])
    
    def test_expand_range_range(self):
        self.assertEqual(expand_range('1-5', 0, 10), [1, 2, 3, 4, 5])
        self.assertEqual(expand_range('3-6', 0, 7), [3, 4, 5, 6])

    def test_parse_cron_expression_valid(self):
        cron_expression = "*/15 0 1,15 * 1-5 /usr/bin/find"
        parsed_cron = parse_cron_expression(cron_expression)
        self.assertEqual(parsed_cron['minute'], [0, 15, 30, 45])
        self.assertEqual(parsed_cron['hour'], [0])
        self.assertEqual(parsed_cron['day of month'], [1, 15])
        self.assertEqual(parsed_cron['month'], list(range(1, 13)))
        self.assertEqual(parsed_cron['day of week'], [1, 2, 3, 4, 5])
        self.assertEqual(parsed_cron['command'], "/usr/bin/find")
    
    def test_parse_cron_expression_invalid(self):
        with self.assertRaises(ValueError):
            parse_cron_expression("*/15 0 1,15 * /usr/bin/find")
    
    def test_format_output(self):
        cron_expression = "*/15 0 1,15 * 1-5 /usr/bin/find"
        parsed_cron = parse_cron_expression(cron_expression)
        
        # Redirect stdout to capture the output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        format_output(parsed_cron)
        
        # Reset redirect.
        sys.stdout = sys.__stdout__
        
        expected_output = (
            "minute        0 15 30 45\n"
            "hour          0\n"
            "day of month  1 15\n"
            "month         1 2 3 4 5 6 7 8 9 10 11 12\n"
            "day of week   1 2 3 4 5\n"
            "command       /usr/bin/find\n"
        )
        
        self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()