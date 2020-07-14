import os
import unittest
from unittest import mock

from src.movie_list_tools_refactored.mergesort_movielist import MovieListMergeSorter
from src.movie_list_tools_refactored.csv_reader_writer import MovieListCSVReader


class MergeSortTest(unittest.TestCase):
    path = "src.movie_list_tools_refactored.mergesort_movielist"

    @mock.patch(f"{path}.input", create=True)
    def test_mergesort(self, mocked_input):
        mlcr = MovieListCSVReader(os.path.join(os.path.dirname(__file__), "test_csvs"), "list3.csv")
        movie_items = mlcr.read_list_csv()
        merge_sorter = MovieListMergeSorter(movie_items)

        mocked_input.side_effect = ['1', '1', '2', '2', '2', '2', '2', '1', '1', '2', '2']
        sorted_items = merge_sorter.merge_sort_items()
        self.assertEqual(list(sorted_items.keys()),  ['Moonrise Kingdom', 'The Grand Budapest Hotel', 'Parasite',
                                                      'Marriage Story', "Ocean's Eleven", "Molly's Game"])

    def test_mergesort_empty_dict(self):
        self.assertRaises(Exception,  MovieListMergeSorter, dict())


if __name__ == '__main__':
    unittest.main()
