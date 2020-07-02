import os
import unittest
from unittest import mock

from src.movie_list_tools.mergesort_movielist import MovieListMergeSorter


class MergeSortTest(unittest.TestCase):
    path = "src.movie_list_tools.mergesort_movielist"

    @mock.patch(f"{path}.input", create=True)
    def test_something(self, mocked_input):
        mocked_input.side_effect = ['1', '1', '2', '2', '2', '2', '2', '1', '1', '2', '2']
        m = MovieListMergeSorter(os.path.join(os.path.dirname(__file__), "test_csvs"), "list3.csv")
        self.assertEqual(m.movie_names,  ['Moonrise Kingdom', 'The Grand Budapest Hotel', 'Parasite', 'Marriage Story',
                                          "Ocean's Eleven", "Molly's Game"])


if __name__ == '__main__':
    unittest.main()
