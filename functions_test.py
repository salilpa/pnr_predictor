from functions import *
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def test_createPoints(self):
        x_val = [2, 3, 4, 5]
        y_val = [3, 4, 5, 6]
        y_val_incorrect_length = [3, 4]
        expected_data = [(2,3), (3,4), (4,5), (5,6)]
        self.assertListEqual(expected_data, createPoints(x_val, y_val))
        self.assertListEqual([], createPoints(x_val, y_val_incorrect_length))
        self.assertListEqual([], createPoints(x_val, "blah"))

suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)