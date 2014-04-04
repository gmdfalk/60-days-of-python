"""
    Created on 23 Mar 2014
    @author: Max Demian
"""

import unittest
from tictactoe import Board


class TestTicTacToe(unittest.TestCase):


    def test_board(self):
        b = Board()
        b.testattrib = "hey"


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

