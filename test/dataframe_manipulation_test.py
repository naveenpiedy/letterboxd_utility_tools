import datetime
import unittest
import pandas as pd
import pandas.testing as pd_testing
from src.dataframe_manipulation import AnalysisSuite


class DataframeManipulationTest(unittest.TestCase):
    movie_df = pd.read_json("movie_dataframe_testdata.json")
    imdb_df = pd.read_json("imdb_dataframe_testdata.json")
    analysis_suite = AnalysisSuite(movie_df, imdb_df)

    def assertDataframeEqual(self, a, b, msg=None):
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_get_ratings_range(self):
        selected_movie_df, selected_imdb_df = self.analysis_suite.get_ratings_range(1.0, 2.0)
        msg = f"Assertion error raised in {self.test_get_ratings_range.__name__}"
        self.assertDataframeEqual(selected_movie_df, pd.read_json("movie_range_dataframe_testdata.json"), msg)
        self.assertDataframeEqual(selected_imdb_df, pd.read_json("imdb_range_dataframe_testdata.json"), msg)

    def test_select_date_range(self):
        start_date = datetime.datetime(2020, 4, 1)
        end_date = datetime.datetime(2020, 4, 30)
        self.analysis_suite.movie_df.watchdate = pd.to_datetime(self.analysis_suite.movie_df.watchdate, unit='ms')
        selected_movie_df, selected_imdb_df = self.analysis_suite.select_date_range(start_date, end_date)
        msg = f"Assertion error raised in {self.test_select_date_range.__name__}"
        test_movie_df = pd.read_json("movie_daterange_dataframe_testdata.json")
        test_imdb_df = pd.read_json("imdb_daterange_dataframe_testdata.json")
        test_movie_df.watchdate = pd.to_datetime(test_movie_df.watchdate, unit="ms")
        test_imdb_df = test_imdb_df.astype({"votes": "float64"})
        self.assertDataframeEqual(selected_movie_df, test_movie_df, msg)
        self.assertDataframeEqual(selected_imdb_df, test_imdb_df, msg)


if __name__ == '__main__':
    unittest.main()
