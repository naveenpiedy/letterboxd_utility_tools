import itertools

import matplotlib.pyplot as plt
import pandas as pd
from base import engine
from models import MovieDatabase, ExtensionIMDB
from collections import Counter
import numpy as np


movie_df = pd.read_sql_table(MovieDatabase.__tablename__, engine)
imdb_df = pd.read_sql_table(ExtensionIMDB.__tablename__, engine)

plt.style.use('ggplot')

def genre_pie_data():
    genres = imdb_df["genres"].to_list()
    counter = Counter(itertools.chain(*genres))
    return counter


def genre_pie():
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    counter = genre_pie_data()
    genre_type = [key for key in counter.keys()]
    genre_values = [values for values in counter.values()]
    ax.pie(genre_values, labels=genre_type, autopct='%1.2f%%')
    plt.show()


def genre_bar():
    counter = genre_pie_data()
    genre_type = [key for key in counter.keys()]
    genre_values = [values for values in counter.values()]
    plt.figure(figsize=(20, 3))
    plt.bar(genre_type, genre_values, align='center', alpha=0.5)
    plt.xticks(genre_type)
    plt.ylabel('Usage')
    plt.title('Programming language usage')

    plt.show()


if __name__ == '__main__':
   genre_pie()