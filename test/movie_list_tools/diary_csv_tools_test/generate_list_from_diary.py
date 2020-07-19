import os
import unittest
from datetime import datetime

from src.movie_list_tools.dataclass_helpers import ListMovieMetadata, ListMovieObject
from src.movie_list_tools.diary_csv_tools.diary_list_helpers import sort_diary_items, read_part_diary
from src.movie_list_tools.diary_csv_tools.generate_list_from_diary import GenerateListFromDiary

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_csvs")
diary_path = os.path.join(path, "diary.csv")


class GenerateListFromDiaryTest(unittest.TestCase):

    def test_generate_list_items(self):
        start_date = datetime.strptime("2020/5/1", '%Y/%m/%d').date()
        end_date = datetime.strptime("2020/5/31", '%Y/%m/%d').date()
        diary_items, rewatch_dict = read_part_diary(diary_path, lower_value=start_date, higher_value=end_date,
                                                    col="watched_date")

        movie_list = sort_diary_items(diary_items, col='rating', reverse=True)

        lmd = ListMovieMetadata(date=datetime.strptime("2020-04-13", '%Y-%m-%d').date(), name='generated_from_diary',
                                url='https://letterboxd.com/test_user/list/list_1/', description='')

        glfd = GenerateListFromDiary(diary_items, lmd, movie_list)

        sorted_movie_dict = glfd.generate_list_items

        expected_moonrise_obj = ListMovieObject(position=1, name='Moonrise Kingdom', year=2012,
                                                url='https://letterboxd.com/test_user/film/moonrise-kingdom/',
                                                metadata=ListMovieMetadata(
                                                    date=datetime.strptime("2020/4/13", '%Y/%m/%d').date(),
                                                    name='generated_from_diary',
                                                    url='https://letterboxd.com/test_user/list/list_1/',
                                                    description=''), description='')

        self.assertEqual(movie_list, list(sorted_movie_dict.keys()))
        self.assertEqual(sorted_movie_dict.get("Moonrise Kingdom"), expected_moonrise_obj)


if __name__ == '__main__':
    unittest.main()
