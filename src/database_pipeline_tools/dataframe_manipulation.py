import itertools
import statistics

from src.database_pipeline_tools.models import MovieDatabase, ExtensionIMDB
import pandas as pd
from src.database_pipeline_tools.base import engine
import datetime
from collections import Counter, OrderedDict


def load_dataframes():
    movie_df = pd.read_sql_table(MovieDatabase.__tablename__, engine)
    imdb_df = pd.read_sql_table(ExtensionIMDB.__tablename__, engine)
    return movie_df, imdb_df


class AnalysisSuite:

    def __init__(self, movie_df, imdb_df):
        self.movie_df = movie_df
        self.imdb_df = imdb_df
        self.selected_movie_df = self.movie_df
        self.selected_imdb_df = self.imdb_df
        self.flag_imdb = 2
        self.flag_movie = 1

    def _set_selected_df(self, movie_dataframe, imdb_dataframe):
        self.selected_movie_df = movie_dataframe
        self.selected_imdb_df = imdb_dataframe

    def _get_imdb_df(self, movie_dataframe):
        list_imdb = movie_dataframe["imdb_id"].to_list()
        imdb_dataframe = self.imdb_df[self.imdb_df["imdb_id"].isin(list_imdb)]
        return imdb_dataframe

    def _allowable_column_names(self, column_name: str, flag: int):
        movie_col = {"id", "letter_boxd_id", "movie_title", "year_released", "my_rating", "watchdate",
                     "letterboxd_link", "rewatch", "published", "sha", "imdb_id"}

        imdb_col = {"id", "imdb_id", "main_db", "cast", "genres", "director", "rating", "votes", "title", "year",
                    "runtimes", "composers", "languages"}
        if flag == self.flag_imdb and column_name not in imdb_col:
            raise Exception(f"Mentioned column name is not usable. Please use one of {imdb_col}")
        elif flag == self.flag_movie and column_name not in movie_col:
            raise Exception(f"Mentioned column name is not usable. Please use one of {movie_col}")

    def get_ratings_range(self, lower_value: float, higher_value: float) -> (pd.DataFrame, pd.DataFrame):
        df = self.movie_df['my_rating'].between(lower_value, higher_value, inclusive=True)
        range_values = self.movie_df[df]
        imdb_range = self._get_imdb_df(range_values)
        self._set_selected_df(range_values, imdb_range)
        return range_values, imdb_range

    def select_date_range(self, start: datetime.datetime, end: datetime.datetime) -> (pd.DataFrame, pd.DataFrame):
        movies_range = self.movie_df['watchdate'].between(start, end, inclusive=True)
        movies_period = self.movie_df[movies_range]
        imdb_period = self._get_imdb_df(movies_period)
        self._set_selected_df(movies_period, imdb_period)
        return movies_period, imdb_period

    def calculate_runtime(self, imdb_period: pd.DataFrame = None) -> str:
        if imdb_period is None:
            imdb_period = self.selected_imdb_df
        list_runtimes = imdb_period["runtimes"].to_list()
        list_runtimes = filter(None, list_runtimes)
        flattened_list = itertools.chain(*list_runtimes)
        return pd.to_datetime(sum(flattened_list), unit="m").strftime('%H:%M')

    def _count_item(self, dataframe: pd.DataFrame, column: str, flag: int) -> Counter:
        self._allowable_column_names(column, flag)
        list_values = dataframe[column].to_list()
        try:
            flattened_list = itertools.chain(*list_values)
            ret = Counter(flattened_list)
        except TypeError:
            ret = Counter(list_values)
        return ret

    def count_item_imdb(self, column: str, imdb_df: pd.DataFrame = None) -> Counter:
        if imdb_df is None:
            imdb_df = self.selected_imdb_df
        return self._count_item(imdb_df, column, self.flag_imdb)

    def count_item_movie(self, column: str, movie_df: pd.DataFrame = None) -> Counter:
        if movie_df is None:
            movie_df = self.selected_movie_df
        return self._count_item(movie_df, column, self.flag_movie)

    def ratings_genre(self, imdb_period: pd.DataFrame = None, movie_period: pd.DataFrame = None) -> OrderedDict:
        if imdb_period is None:
            imdb_period = self.selected_imdb_df
        if movie_period is None:
            movie_period = self.selected_movie_df
        genre_list = imdb_period["genres"].to_list()
        flattened_list = itertools.chain(*genre_list)
        avg_ratings = {}
        for genre_type in flattened_list:
            mask = imdb_period.genres.apply(lambda x: genre_type in x)
            genre_dataframe = imdb_period[mask]
            imdb_id_list = genre_dataframe["imdb_id"].to_list()
            movie_range = movie_period[movie_period["imdb_id"].isin(imdb_id_list)]
            avg_ratings[genre_type] = round(statistics.mean(movie_range["my_rating"].to_list()), 2)
        return OrderedDict(sorted(avg_ratings.items(), key=lambda x: x[1], reverse=True))


if __name__ == '__main__':
    load_dataframes()
