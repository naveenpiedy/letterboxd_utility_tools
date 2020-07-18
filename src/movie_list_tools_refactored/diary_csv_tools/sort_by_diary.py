import csv
from collections import defaultdict
from datetime import datetime

from src.movie_list_tools.dataclass_helpers import DiaryMovieObject, CombinedListDiaryObject


def check_col(col: str) -> str:
    """
    Checks if specified col can be joined with list object
    """
    columns_available = {"name", "year", "rating", "watched_date"}
    if col not in columns_available:
        raise Exception(f"Mentioned column name is not usable. Please use one of {columns_available}")
    return col


class ReadDiary:
    __slots__ = "diary_location"

    def __init__(self, diary_location):
        self.diary_location = diary_location

    def read_diary(self, func=lambda x: True):
        """
        Reads diary csv creates a neat dict with all items.
        """
        diary_items = dict()
        rewatch_dict = defaultdict(list)
        try:
            with open(self.diary_location) as csvfile:
                contents = csv.reader(csvfile, delimiter=',')
                next(contents)
                for line in contents:
                    if func(line):
                        if line[1] not in diary_items:
                            key = line[1]
                        else:
                            suffix_int = 1
                            while f"{line[1]} ({str(suffix_int)})" in diary_items:
                                suffix_int += 1
                            key = f"{line[1]} ({str(suffix_int)})"
                            rewatch_dict[line[1]].append(key)

                        diary_items[key] = DiaryMovieObject(date_=datetime.strptime(line[0], '%Y-%m-%d').date(),
                                                            name=line[1], year=int(line[2]), url=line[3],
                                                            rating=float(line[4]), rewatch=line[5] == "Yes",
                                                            tags=set(line[6].split(",")),
                                                            watched_date=datetime.strptime(line[7], '%Y-%m-%d').date())

            return diary_items, rewatch_dict
        except FileNotFoundError:
            raise FileNotFoundError


class CombineListDiaryItems:
    __slots__ = ("diary_items", "rewatch_dict", "list_items")

    def __init__(self, diary_items, rewatch_dict, list_items):
        self.diary_items = diary_items
        self.rewatch_dict = rewatch_dict
        self.list_items = list_items

    def combine_dict(self):
        """
        Combines details from list csv and diary csv -> self.combined_dict
        """
        try:
            movie_names = self.list_items.keys()
            combined_dicts = dict()
            for movie in movie_names:
                if self.diary_items.get(movie):
                    diary_list = [movie]
                    if self.rewatch_dict.get(movie):
                        diary_list.extend(self.rewatch_dict.get(movie))

                    combined_dicts[movie] = CombinedListDiaryObject(rewatch=self.diary_items.get(movie).rewatch,
                                                                    listobj=self.list_items.get(movie),
                                                                    diaryobjs=[self.diary_items.get(i) for i in
                                                                               diary_list])
                else:
                    combined_dicts[movie] = CombinedListDiaryObject(rewatch=False,
                                                                    listobj=self.list_items.get(movie))

            return combined_dicts
        except AttributeError:
            raise Exception("Something off with the inputs. Please use the appropriate classes to generate the input")


class SortListDiaryItems:
    __slots__ = ("combined_dict", "column", "reverse")

    def __init__(self, combined_dict, column, reverse=False):
        self.combined_dict = combined_dict
        self.column = check_col(column)
        self.reverse = reverse

    def sorter(self):
        try:
            sorted_dict = dict()
            movie_names = self.combined_dict.keys()

            movie_names = sorted(movie_names,
                                 reverse=self.reverse,
                                 key=lambda x: getattr(self.combined_dict.get(x).diaryobjs[-1], self.column))

            for i, val in enumerate(movie_names):
                item = self.combined_dict.get(val).listobj
                item.position = i + 1
                sorted_dict[val] = item

            return sorted_dict

        except AttributeError:
            raise Exception("Something off with the inputs. Please use the appropriate classes to generate the input")
