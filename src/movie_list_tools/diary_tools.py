import csv
import os
from datetime import datetime

from src.movie_list_tools.dataclass_helpers import CombinedListDiaryObject, DiaryMovieObject, ListMovieObject, \
    ListMovieMetadata
from src.movie_list_tools.movie_list_sorter import ListBaseClass
from typing import Any


class ListDiaryBase(ListBaseClass):
    def _sorter(self, movie_list: list):
        pass

    def _movie_object_sorter(self):
        pass

    def __init__(self, file_location: str, list_name: str):
        super().__init__(file_location, list_name)
        self.diary_file_location = os.path.join(file_location, "diary.csv")
        self.diary_items = dict()

    @staticmethod
    def _check_col(col: str) -> str:
        """
        Checks if specified col can be joined with list object
        """
        columns_available = {"name", "year", "rating", "watched_date"}
        if col not in columns_available:
            raise Exception(f"Mentioned column name is not usable. Please use one of {columns_available}")
        return col

    def _read_diary_entry(self, func=lambda x: True):
        """
        Reads diary csv creates a neat dict with all items.
        """
        with open(self.diary_file_location) as csvfile:
            contents = csv.reader(csvfile, delimiter=',')
            next(contents)
            for line in contents:
                if func(line):
                    if line[1] not in self.diary_items:
                        key = line[1]
                    else:
                        suffix_int = 1
                        while f"{line[1]} ({str(suffix_int)})" in self.diary_items:
                            suffix_int += 1
                        key = f"{line[1]} ({str(suffix_int)})"
                        self.rewatch_dict[line[1]].append(key)

                    self.diary_items[key] = DiaryMovieObject(date_=datetime.strptime(line[0], '%Y-%m-%d').date(),
                                                             name=line[1],
                                                             year=int(line[2]),
                                                             url=line[3],
                                                             rating=float(line[4]),
                                                             rewatch=line[5] == "Yes",
                                                             tags=set(line[6].split(",")),
                                                             watched_date=datetime.strptime(line[7],
                                                                                            '%Y-%m-%d').date())


class SortListDiary(ListDiaryBase):

    def __init__(self, file_location: str, list_name: str, col: str, reverse: bool = False):
        super().__init__(file_location, list_name)
        self.combined_dicts = dict()
        self.col = self._check_col(col)
        self._perform_sort_list(reverse=reverse)

    def _read_diary_list_csv(self):
        self._read_diary_entry(lambda x: x[1] in self.movie_names)

    def _combine_dicts(self):
        """
        Combines details from list csv and diary csv -> self.combined_dict
        """
        for movie in self.movie_names:
            if self.diary_items.get(movie):
                diary_list = [movie]
                if self.rewatch_dict.get(movie):
                    diary_list.extend(self.rewatch_dict.get(movie))

                self.combined_dicts[movie] = CombinedListDiaryObject(rewatch=self.diary_items.get(movie).rewatch,
                                                                     listobj=self.list_item_dicts.get(movie),
                                                                     diaryobjs=[self.diary_items.get(i) for i in
                                                                                diary_list])
            else:
                self.combined_dicts[movie] = CombinedListDiaryObject(rewatch=False,
                                                                     listobj=self.list_item_dicts.get(movie))

    def _sorter(self, movie_list: list = None, reverse: bool = False):
        """
        Sorts the list of movie names using self.combined_dict
        """
        self.movie_names = sorted(self.movie_names, reverse=reverse,
                                  key=lambda x: getattr(self.combined_dicts.get(x).diaryobjs[-1], self.col))

    def _movie_object_sorter(self):
        """
        Sorts items from self.item_dicts into self.sorted_dict (contains MovieObjects) based on order of
        self.movie_names.
        """
        for i, val in enumerate(self.movie_names):
            item = self.list_item_dicts.get(val)
            item.position = i + 1
            self.sorted_dict[val] = item

    def _perform_sort_list(self, reverse: bool = False):
        """
        The whole operation from top to bottom.
        """
        self._read_list_csv()
        self._read_diary_list_csv()
        self._combine_dicts()
        self._sorter(reverse=reverse)
        self._movie_object_sorter()
        self._write_list_csv()


class GenerateListFromDiary(ListDiaryBase):
    index_col = {
        "date": 0,
        "year": 2,
        "rating": 4,
        "watched_date": 7,
    }

    col_type_lambda = {
        0: lambda x: datetime.strptime(x, '%Y-%m-%d').date(),
        2: lambda x: int(x),
        4: lambda x: float(x),
        7: lambda x: datetime.strptime(x, '%Y-%m-%d').date()
    }

    def __init__(self, file_location: str, col: str, lower_value: Any, higher_value: Any,
                 listmetadata: ListMovieMetadata = None, list_name: str = None, reverse: bool = True):
        """
        Init function

        :param file_location: Where you have your LetterBoxd CSV's.
        :param list_name: Name of the list you want to generate
        :param col: Column which you are using to generate the list -> date, year, rating, watched_date
        :param lower_value: Lower bound value. Make sure to use proper datatype. example: 2.0 if using rating.
        :param higher_value: Higher bound value. Make sure to use proper datatype. example: 5.0 if using rating.
        :param listmetadata: Use dataclass ListMovieMetadata to give the metadata
        :param reverse: If you want to generate the list in reverse order
        """
        super(GenerateListFromDiary, self).__init__(file_location, list_name)
        self.col, self.lower_value, self.higher_value = self._check_values(col, lower_value, higher_value)
        self.listmetadata = listmetadata
        self._perform_operation(reverse=reverse)

    @classmethod
    def _check_values(cls, col: str, lower_value: Any, higher_value: Any):
        """
        Check if the values are of the proper datatype and col is proper column.
        """
        col = cls._check_col(col)

        col_type_mapper = {
            "date": datetime.date,
            "year": int,
            "rating": float,
            "watched_date": datetime.date}

        if not isinstance(lower_value, col_type_mapper.get(col)):
            raise Exception(f"Mentioned lower value is not of the right data type. You have given {type(lower_value)}"
                            f"For {col} use {col_type_mapper.get(col)}")

        if not isinstance(higher_value, col_type_mapper.get(col)):
            raise Exception(f"Mentioned higher value is not of the right data type. You have given "
                            f"{type(higher_value)}"
                            f"For {col} use {col_type_mapper.get(col)}")

        if lower_value > higher_value:
            raise Exception("Lower Value is greater than higher value, please change")

        return col, lower_value, higher_value

    def _read_part_diary_csv(self):
        """
        Reads only the relevant part of the diary.csv
        """
        index = self.index_col.get(self.col)
        self._read_diary_entry(
            lambda x: self.lower_value <= self.col_type_lambda.get(index)(x[index]) <= self.higher_value)

    def _sorter(self, reverse: bool = False, movie_list: list = None):
        """
        Sorts the movies based on the column, lower_value and higher_value.
        :param reverse: Boolean used to specify if the order should be in the reverse order.
        :param movie_list: list but is only there for debugging purposes.
        """
        self.movie_names = sorted(self.diary_items.keys(),
                                  key=lambda x: getattr(self.diary_items.get(x), self.col),
                                  reverse=reverse)

    def _movie_object_sorter(self):
        """
        Creates List object in sorted fashion for self._write_csv()
        """
        if not self.listmetadata:
            self.listmetadata = ListMovieMetadata(date=datetime.today(),
                                                  name=self.list_name if self.list_name else "Gen List",
                                                  url="")
        meta_data_headers = [[], "Date,Name,Tags,URL,Description".split(",")]
        lm = self.listmetadata
        meta_data_headers.append([f"{lm.date.strftime('%Y-%m-%d')}", f"{lm.name}", f"{lm.url}", f"{lm.description}"])
        meta_data_headers.append([])
        meta_data_headers.append(['Position', 'Name', 'Year', 'URL', 'Description'])
        self.first_lines = meta_data_headers
        for pos, movie_name in enumerate(self.movie_names, start=1):
            item = self.diary_items.get(movie_name)
            self.sorted_dict[movie_name] = ListMovieObject(position=pos, name=movie_name, year=item.year, url=item.url,
                                                           metadata=self.listmetadata)

    def _perform_operation(self, reverse):
        """
        The whole operation from top to bottom.
        """
        self._read_part_diary_csv()
        self._sorter(reverse)
        self._movie_object_sorter()
        self._write_list_csv()


if __name__ == '__main__':
    GenerateListFromDiary(file_location="E:\\Movie Data\\letterboxd-naveenpiedy-jun", col="rating", lower_value=5.0,
                          higher_value=5.0)
