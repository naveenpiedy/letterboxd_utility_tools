import os
import unittest

from src.movie_list_tools.diary_tools import SortListDiary, GenerateListFromDiary
from src.movie_list_tools.dataclass_helpers import ListMovieMetadata
from datetime import date


class DiaryToolsTests(unittest.TestCase):
    path = "src.movie_list_tools.mergesort_movielist"

    def test_sort_list_diary(self):
        sld_obj = SortListDiary(file_location=os.path.join(os.path.dirname(__file__), "test_csvs"),
                                list_name="list2.csv",
                                col="watched_date",
                                reverse=True)
        self.assertEqual(sld_obj.movie_names, ['Moonrise Kingdom', 'The Grand Budapest Hotel'])

    def test_generate_list_diary(self):
        metadata = ListMovieMetadata(date=date(year=2020, month=7, day=4), name="generated_list", url="")
        gld_obj = GenerateListFromDiary(file_location=os.path.join(os.path.dirname(__file__), "test_csvs"),
                                        col="rating",
                                        lower_value=2.0,
                                        higher_value=3.0,
                                        listmetadata=metadata)

        self.assertEqual(gld_obj.movie_names, ['The Brothers Bloom', 'True Lies', 'Wonder Woman',
                                               'Neethaane En Ponvasantham', 'OK Kanmani', 'Minnale',
                                               'Extraction', 'Kannum Kannum Kollaiyadithaal'])


if __name__ == '__main__':
    unittest.main()
