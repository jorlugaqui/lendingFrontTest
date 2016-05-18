import unittest
from app import analyze_data_and_take_decision


class DecisionTestCase(unittest.TestCase):

    def test_decision(self):
        response = analyze_data_and_take_decision(46)
        self.assertEqual(response, 'Approved')

        response = analyze_data_and_take_decision(50000)
        self.assertEqual(response, 'Undecided')

        response = analyze_data_and_take_decision(460000)
        self.assertEqual(response, 'Declined')

if __name__ == '__main__':
    unittest.main()
