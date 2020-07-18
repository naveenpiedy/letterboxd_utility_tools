import os
import unittest
from datetime import datetime

from src.movie_list_tools_refactored.csv_reader_writer import MovieListCSVReader
from src.movie_list_tools_refactored.diary_csv_tools.sort_by_diary import ReadDiary, CombineListDiaryItems, \
    SortListDiaryItems

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_csvs")
diary_path = os.path.join(path, "diary.csv")


class ReadDiaryTest(unittest.TestCase):
    def test_read_diary(self):
        rd = ReadDiary(diary_location=diary_path)
        diary_items, rewatch_dict = rd.read_diary()
        expected_movienames = ['Once Upon a Time.. in Hollywood', 'Jojo Rabbit', "Molly's Game",
                               'Kannum Kannum Kollaiyadithaal',
                               'Parasite', 'The Nice Guys', 'The Grand Budapest Hotel', 'Knives Out',
                               'Portrait of a Lady on Fire',
                               'Scott Pilgrim vs. the World', 'Moonrise Kingdom', 'Moonrise Kingdom (1)', 'Lady Bird',
                               'The Brothers Bloom', 'Extraction', 'Star Wars: The Rise of Skywalker', 'La La Land',
                               'True Lies',
                               'Barely Lethal', 'Zoom', 'Little Women', 'Alaipayuthey', 'The Darjeeling Limited',
                               'Hotel Chevalier', 'The Royal Tenenbaums', 'The Royal Tenenbaums (1)',
                               'When Harry Met Sally...',
                               'Wonder Woman', 'Neethaane En Ponvasantham', 'OK Kanmani', 'Minnale']

        expected_rewatches = {'Moonrise Kingdom': ['Moonrise Kingdom (1)'],
                              'The Royal Tenenbaums': ['The Royal Tenenbaums (1)']}

        self.assertEqual(list(diary_items.keys()), expected_movienames, msg="Test Diary Items")
        self.assertEqual(expected_rewatches, rewatch_dict, msg="Test Rewatch Items")

    def test_wrong_path(self):
        rd = ReadDiary(diary_location="diary_path")
        self.assertRaises(FileNotFoundError, rd.read_diary)


class CombineListDiaryItemsTest(unittest.TestCase):

    def test_combine_diary(self):
        rd = ReadDiary(diary_location=diary_path)
        diary_items, rewatch_dict = rd.read_diary()

        mlcr = MovieListCSVReader(directory=path, list_name="list1.csv")
        list_items = mlcr.read_list_csv()

        cldi = CombineListDiaryItems(diary_items, rewatch_dict, list_items)
        combined_dict = cldi.combine_dict()

        self.assertEqual(list(combined_dict.keys()), ["The Nice Guys", "True Lies"])

        self.assertEqual(combined_dict.get("True Lies").diaryobjs[0].watched_date,
                         datetime.strptime("2020/5/15", '%Y/%m/%d').date())

    def test_wrong_vairables(self):
        diary_items = None
        rewatch_dict = None
        list_items = None
        cldi = CombineListDiaryItems(diary_items, rewatch_dict, list_items)

        self.assertRaises(Exception, cldi.combine_dict)


class SortListDiaryItemsTest(unittest.TestCase):

    def test_sort_diary(self):
        rd = ReadDiary(diary_location=diary_path)
        diary_items, rewatch_dict = rd.read_diary()

        mlcr = MovieListCSVReader(directory=path, list_name="list1.csv")
        list_items = mlcr.read_list_csv()

        cldi = CombineListDiaryItems(diary_items, rewatch_dict, list_items)
        combined_dict = cldi.combine_dict()

        sldi = SortListDiaryItems(combined_dict, "rating", False)
        sorted_dict = sldi.sorter()

        self.assertEqual(list(sorted_dict.keys()), ['True Lies', 'The Nice Guys'])

    def test_wrong_vairables(self):

        sldi = SortListDiaryItems(None, "rating", False)
        self.assertRaises(Exception, sldi.sorter)

    def test_wrong_column(self):
        rd = ReadDiary(diary_location=diary_path)
        diary_items, rewatch_dict = rd.read_diary()

        mlcr = MovieListCSVReader(directory=path, list_name="list1.csv")
        list_items = mlcr.read_list_csv()

        cldi = CombineListDiaryItems(diary_items, rewatch_dict, list_items)
        combined_dict = cldi.combine_dict()

        self.assertRaises(Exception, SortListDiaryItems, combined_dict, "wrong_col", False)


if __name__ == '__main__':
    unittest.main()
