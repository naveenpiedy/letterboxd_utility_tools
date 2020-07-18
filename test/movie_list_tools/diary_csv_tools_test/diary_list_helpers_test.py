import os
import unittest
from datetime import datetime

from src.movie_list_tools.diary_csv_tools.diary_list_helpers import check_values, read_part_diary, \
    sort_diary_items

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_csvs")
diary_path = os.path.join(path, "diary.csv")


class DiaryListHelpersTest(unittest.TestCase):

    def test_check_wrong_values(self):
        self.assertRaises(Exception, check_values, 'rating', 'as', 'as')

    def test_check_right_values(self):
        col, lower, higher = check_values("rating", 2.0, 3.0)
        self.assertEqual(col, 'rating')
        self.assertEqual(lower, 2.0)
        self.assertEqual(higher, 3.0)

    def test_read_part_diary(self):
        start_date = datetime.strptime("2020/5/1", '%Y/%m/%d').date()
        end_date = datetime.strptime("2020/5/31", '%Y/%m/%d').date()
        diary_items, rewatch_dict = read_part_diary(diary_path, lower_value=start_date, higher_value=end_date,
                                                    col="watched_date")
        diary_items_list = list(diary_items.values())
        watched_dates = [i.watched_date for i in diary_items_list]

        self.assertTrue(all([start_date <= i <= end_date for i in watched_dates]))

    def test_sort_diary_items(self):
        start_date = datetime.strptime("2020/5/1", '%Y/%m/%d').date()
        end_date = datetime.strptime("2020/5/31", '%Y/%m/%d').date()
        diary_items, rewatch_dict = read_part_diary(diary_path, lower_value=start_date, higher_value=end_date,
                                                    col="watched_date")

        movie_list = sort_diary_items(diary_items, col='rating', reverse=True)

        expected = ['Moonrise Kingdom', 'Moonrise Kingdom (1)', 'La La Land', 'Little Women', 'Lady Bird',
                    'Alaipayuthey', 'The Darjeeling Limited', 'Hotel Chevalier', 'The Brothers Bloom', 'True Lies',
                    'Extraction', 'Star Wars: The Rise of Skywalker', 'Barely Lethal', 'Zoom']

        self.assertEqual(expected, movie_list)


if __name__ == '__main__':
    unittest.main()
