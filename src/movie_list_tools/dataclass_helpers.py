from typing import List
from tabulate import tabulate
from dataclasses import dataclass, field
from datetime import date, datetime


def make_default_diaryobj():
    return [DiaryMovieObject(date_=datetime.strptime('1700-1-1', '%Y-%m-%d').date(), name="None", year=1700,
                             url="None", rating=float(-1), rewatch=False, tags=["None"],
                             watched_date=datetime.strptime('1700-1-1', '%Y-%m-%d').date())]


@dataclass
class ListMovieMetadata:
    date: date
    name: str
    url: str
    description: str = ''


@dataclass
class ListMovieObject:
    position: int
    name: str
    year: date
    url: str
    metadata: ListMovieMetadata
    description: str = ''

    def __str__(self):
        table = [["Position", self.position], ["Name", self.name],
                 ["List Name", self.metadata.name], ["Year", self.year]]
        output = tabulate(table, tablefmt='psql')
        return output


@dataclass
class DiaryMovieObject:
    date_: date
    name: str
    year: int
    url: str
    rating: float
    tags: set
    watched_date: date
    rewatch: bool = False

    def __str__(self):
        table = [["Name", self.name], ["Year", self.year], ["Rating", self.rating], ["Watch Date", self.watched_date],
                 ["Rewatch", self.rewatch]]
        output = tabulate(table, tablefmt='psql')
        return output


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
