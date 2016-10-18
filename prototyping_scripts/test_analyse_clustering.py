import unittest
import doctest

from GAFER import analyse_clustering

class Test(unittest.TestCase):
    """Unit tests for analyse_clustering."""

    def test_doctests(self):
        """Run analyse_clustering doctests"""
        doctest.testmod(analyse_clustering)

if __name__ == "__main__":
    unittest.main()