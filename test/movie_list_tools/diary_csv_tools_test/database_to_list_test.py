import json
import os
import unittest

import pytest

from src.database_pipeline_tools.letterboxd_rss_parser import LetterBoxdRss
from src.movie_list_tools.dataclass_helpers import ListMovieMetadata
from src.movie_list_tools_refactored.database_list_tools.database_to_list import DatabaseToList
from datetime import date

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_csvs")
metadata = ListMovieMetadata(date=date(year=2020, month=7, day=4), name="generated_list", url="")

rss_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "letterboxd_rss_feed_test.xml")


@pytest.fixture(scope='function')
def dataset():
    obj = LetterBoxdRss(feed_url=rss_path)
    obj.feed_db_pipeline()


@pytest.mark.usefixtures("dataset")
class DatabaseToListTest(unittest.TestCase):

    def test_generate_normal_list(self):
        data = {
            "my_rating": {
                "lower": 3,
                "higher": 5
            },
            "genres": [["Drama"], ["Romance"]],
            "watchdate": {
                "lower": "2020-04-01",
                "higher": "2020-06-30"
            },
            "director": ["Wes Anderson", "Mani Ratnam"]
        }

        db = DatabaseToList(output_location=path, output_list_metadata=metadata,
                            input_json=json.dumps(data), column="imdb_info.languages")

        parsed_json = db.parse_output_json()
        movie_names = list(parsed_json.keys())

        english_movies = ['Moonrise Kingdom', 'Hotel Chevalier', 'The Life Aquatic with Steve Zissou']
        tamil_movies = ['Alaipayuthey', 'Mouna Raagam']

        self.assertEqual(movie_names[:3], english_movies)
        self.assertEqual(movie_names[3:], tamil_movies)


if __name__ == '__main__':
    pytest.main()
