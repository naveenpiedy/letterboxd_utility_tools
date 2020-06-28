import datetime
import unittest
import pandas as pd
import pandas.testing as pd_testing
from src.database_pipeline_tools.dataframe_manipulation import AnalysisSuite


class DataframeManipulationTest(unittest.TestCase):
    movie_df = pd.read_pickle("movie_dataframe.pickle")
    imdb_df = pd.read_pickle("imdb_dataframe.pickle")
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
        ratings_list = set(selected_movie_df["my_rating"].tolist())
        imdb_id_mdf = set(selected_movie_df["imdb_id"].tolist())
        imdb_id_idf = set(selected_imdb_df["imdb_id"].tolist())

        self.assertDataframeEqual(selected_movie_df, pd.read_pickle("movie_range_dataframe.pickle"), msg)
        self.assertDataframeEqual(selected_imdb_df, pd.read_pickle("imdb_range_dataframe.pickle"), msg)
        self.assertEqual({1.0, 1.5, 2.0}, ratings_list)
        self.assertEqual(imdb_id_idf, imdb_id_mdf)
        
    def test_select_date_range(self):
        start_date = datetime.datetime(2020, 6, 1)
        end_date = datetime.datetime(2020, 6, 30)
        selected_movie_df, selected_imdb_df = self.analysis_suite.select_date_range(start_date, end_date)
        imdb_id_mdf = set(selected_movie_df["imdb_id"].tolist())
        imdb_id_idf = set(selected_imdb_df["imdb_id"].tolist())
        watched_date_mdf = set(selected_movie_df["watchdate"].tolist())
        msg = f"Assertion error raised in {self.test_select_date_range.__name__}"

        self.assertDataframeEqual(selected_movie_df, pd.read_pickle("movie_daterange_dataframe.pickle"), msg)
        self.assertDataframeEqual(selected_imdb_df, pd.read_pickle("imdb_daterange_dataframe.pickle"), msg)
        self.assertEqual(imdb_id_idf, imdb_id_mdf)
        self.assertEqual({True}, {start_date <= i <= end_date for i in watched_date_mdf})

    def test_calculate_runtime(self):
        start_date = datetime.datetime(2020, 6, 1)
        end_date = datetime.datetime(2020, 6, 30)
        _, _ = self.analysis_suite.select_date_range(start_date, end_date)
        
        self.assertEqual(self.analysis_suite.calculate_runtime(), "10:16")
        self.assertEqual(self.analysis_suite.calculate_runtime(imdb_period=self.imdb_df), "23:34")
    
    def test_count_item(self):
        start_date = datetime.datetime(2020, 6, 1)
        end_date = datetime.datetime(2020, 6, 30)
        _, _ = self.analysis_suite.select_date_range(start_date, end_date)
        
        self.assertEqual(self.analysis_suite.count_item_imdb("year").most_common(1), [(2001, 3)])
        self.assertEqual(self.analysis_suite.count_item_imdb("genres").most_common(1), [("Romance", 11)])
        self.assertEqual(self.analysis_suite.count_item_imdb("year",
                                                             imdb_df=self.imdb_df).most_common(1), [(2019, 11)])
        self.assertEqual(self.analysis_suite.count_item_imdb("genres",
                                                             imdb_df=self.imdb_df).most_common(1), [('Comedy', 45)])
        self.assertRaises(Exception, self.analysis_suite.count_item_imdb, "genre")
        self.assertEqual(self.analysis_suite.count_item_movie("my_rating").most_common(1), [(4.5, 4)])

    def test_ratings_genre(self):
        start_date = datetime.datetime(2020, 6, 1)
        end_date = datetime.datetime(2020, 6, 30)
        _, _ = self.analysis_suite.select_date_range(start_date, end_date)
        result = self.analysis_suite.ratings_genre()
        
        self.assertEqual(result.get("Drama"),  4.06)
        self.assertEqual(result.get("Comedy"),  3.32)
        
        
if __name__ == '__main__':
    unittest.main()
