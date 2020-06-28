from dataclasses import dataclass, field
from datetime import date, datetime
import csv
from src.movie_list_tools.movie_list_sorter import MovieSorterBaseClass, ListMovieObject
from collections import defaultdict
from typing import List
from tabulate import tabulate


@dataclass
class DiaryMovieObject:
    date_: date
    name: str
    year: int
    url: str
    rating: float
    tags: list
    watched_date: date
    rewatch: bool = False

    def __str__(self):
        table = [["Name", self.name], ["Year", self.year], ["Rating", self.rating], ["Watch Date", self.watched_date],
                 ["Rewatch", self.rewatch]]
        output = tabulate(table, tablefmt='psql')
        return output


def make_default_diaryobj():
    return [DiaryMovieObject(date_=datetime.strptime('1700-1-1', '%Y-%m-%d').date(),
                            name="None", year=1700, url="None", rating=float(-1), rewatch=False,
                            tags=["None"], watched_date=datetime.strptime('1700-1-1', '%Y-%m-%d').date())]


@dataclass
class CombinedListDiaryObject:
    rewatch: bool
    listobj: ListMovieObject
    diaryobjs: List[DiaryMovieObject] = field(default_factory=make_default_diaryobj)

    def __str__(self):
        final_list = [["Name", self.listobj.name], ["List Entry", f"{self.listobj!s}"]]
        for index, item in enumerate(self.diaryobjs):
            if index == 0:
                final_list.append(["Diary Entry", f"{item!s}"])
            else:
                final_list.append(["", f"{item!s}"])
        output = tabulate(final_list, tablefmt='psql')
        return output


class SortByAttribute(MovieSorterBaseClass):

    def __init__(self, list_file_location: str, diary_file_location: str, col):
        super().__init__(list_file_location)
        self.diary_file_location = diary_file_location
        self.diary_items = dict()
        self.combined_dicts = dict()
        self.rewatch_dict = defaultdict(list)
        self.col = self._check_col(col)

    @staticmethod
    def _check_col(col):

        columns_available = {"name", "year", "rating", "watched_date"}
        if col not in columns_available:
            raise Exception(f"Mentioned column name is not usable. Please use one of {columns_available}")
        return col

    def _read_diary_csv(self):
        with open(self.diary_file_location) as csvfile:
            contents = csv.reader(csvfile, delimiter=',')
            headers = next(contents)
            for line in contents:
                if line[1] not in self.diary_items:
                    self.diary_items[line[1]] = DiaryMovieObject(date_=datetime.strptime(line[0], '%Y-%m-%d').date(),
                                                                 name=line[1], year=int(line[2]), url=line[3],
                                                                 rating=float(line[4]), rewatch=line[5] == "Yes",
                                                                 tags=line[6].split(","),
                                                                 watched_date=datetime.strptime(line[7],
                                                                                                '%Y-%m-%d').date())
                else:
                    suffix_int = 1
                    while f"{line[1]} ({str(suffix_int)})" in self.diary_items:
                        suffix_int += 1
                    self.diary_items[f"{line[1]} ({str(suffix_int)})"] = DiaryMovieObject(
                        date_=datetime.strptime(line[0], '%Y-%m-%d').date(), name=line[1], year=int(line[2]),
                        url=line[3], rating=float(line[4]), rewatch=line[5] == "Yes", tags=line[6].split(","),
                        watched_date=datetime.strptime(line[7], '%Y-%m-%d').date())
                    self.rewatch_dict[line[1]].append(f"{line[1]} ({str(suffix_int)})")

        # print(self.diary_items["Marriage Story"])

    def _combine_dicts(self):
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

        print(self.combined_dicts.get("Moonrise Kingdom"))

    def _sorter(self, movie_list: list):
        sorted_list = sorted(self.movie_names, reverse=True, key=lambda x: self.combined_dicts.get(x).diaryobjs[-1].rating)
        self.movie_names = sorted_list
        pass

    def _movie_object_sorter(self):
        for i, val in enumerate(self.movie_names):
            item = self.list_item_dicts.get(val)
            item.position = i + 1
            self.sorted_dict[val] = item


if __name__ == '__main__':
    sortee = SortByAttribute("E:\\Movie Data\\letterboxd-naveenpiedy-jun\\lists\\watched-in-2020.csv",
                             "E:\\Movie Data\\letterboxd-naveenpiedy-jun\\diary.csv", col="rating")
    sortee._read_diary_csv()
    sortee._read_list_csv()
    sortee._combine_dicts()
    sortee._sorter([None])
    sortee._movie_object_sorter()
    sortee._write_list_csv()