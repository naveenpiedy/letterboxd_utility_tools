import itertools
import statistics

from models import MovieDatabase, ExtensionIMDB
import pandas as pd
from base import engine
import datetime
from collections import Counter, OrderedDict

movie_df = pd.read_sql_table(MovieDatabase.__tablename__, engine)
imdb_df = pd.read_sql_table(ExtensionIMDB.__tablename__, engine)


def get_ratings_range(lower_value, higher_value):
    df = movie_df['my_rating'].between(lower_value, higher_value, inclusive=True)
    range_values = movie_df[df]
    return range_values


def select_date_range(start_date, end_date):
    movies_range = movie_df['watchdate'].between(start_date, end_date, inclusive=True)
    movies_period = movie_df[movies_range]
    list_imdb = movies_period["imdb_id"].to_list()
    imdb_period = imdb_df[imdb_df["imdb_id"].isin(list_imdb)]
    return movies_period, imdb_period


def calculate_runtime(imdb_period):
    list_runtimes = imdb_period["runtimes"].to_list()
    flattened_list = itertools.chain(*list_runtimes)
    return pd.to_datetime(sum(flattened_list), unit="m").strftime('%H:%M')


def count_item(imdb_period, column):
    list_values = imdb_period[column].to_list()
    flattened_list = itertools.chain(*list_values)
    return Counter(flattened_list)


def ratings_genre(imdb_period, movie_period):
    list_runtimes = imdb_period["genres"].to_list()
    flattened_list = itertools.chain(*list_runtimes)
    avg_ratings = {}
    for genre_type in flattened_list:
        mask = imdb_period.genres.apply(lambda x: genre_type in x)
        genre_dataframe = imdb_period[mask]
        imdb_id_list = genre_dataframe["imdb_id"].to_list()
        movie_range = movie_period[movie_period["imdb_id"].isin(imdb_id_list)]
        avg_ratings[genre_type] = round(statistics.mean(movie_range["my_rating"].to_list()), 2)
    sorted_avg_ratings = OrderedDict(sorted(avg_ratings.items(), key=lambda x: x[1], reverse=True))
    return sorted_avg_ratings


if __name__ == '__main__':
    start_date = datetime.datetime(2020, 4, 1)
    end_date = datetime.datetime(2020, 4, 30)
    movies, imdb = select_date_range(start_date, end_date)
    print(calculate_runtime(imdb))
    print(count_item(imdb, "genres").most_common())
    print(count_item(imdb, "director"))
    print(count_item(imdb, "cast").most_common())
    print(ratings_genre(imdb, movies))
