import abc
import csv
from collections import defaultdict
import os

from src.movie_list_tools.dataclass_helpers import ListMovieMetadata, ListMovieObject


class ListBaseClass(metaclass=abc.ABCMeta):

    def __init__(self, file_location: str, list_name: str):
        """
        The __init__ function should perform end to end operation from reading the CSV to sorting to generating a csv.
        """
        self.list_location = file_location
        self.list_item_dicts = dict()
        self.sorted_dict = dict()
        self.movie_names = list()
        self.rewatch_dict = defaultdict(list)
        self.first_lines = []
        self.list_name = list_name

    def _read_list_csv(self):
        """
        Reads LetterBoxd List csv. Preserves first four lines containing list metadata in self.first_lines
        for csv generation later.
        """
        list_location = os.path.join(self.list_location, "lists", self.list_name)
        with open(list_location) as csvfile:
            contents = csv.reader(csvfile, delimiter=',')
            meta = None
            for index, line in enumerate(contents):
                if index <= 4:
                    self.first_lines.append(line)
                    if index == 2:
                        meta = ListMovieMetadata(line[0], line[1], line[2], line[3])
                else:
                    self.list_item_dicts[line[1]] = ListMovieObject(position=line[0], name=line[1], year=line[2],
                                                                    url=line[3], description=line[4], metadata=meta)
                    self.movie_names.append(line[1])

    def _write_list_csv(self):
        """
        Generates a LetterBoxd compliant list csv based on order in self.sorted_dict
        """
        with open('../../sorted_list.csv', mode='w', newline='') as sorted_list_csv:
            headers = ['Position', 'Name', 'Year', 'URL', 'Description']
            first_lines_writer = csv.writer(sorted_list_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in self.first_lines:
                first_lines_writer.writerow(line)
            writer = csv.DictWriter(sorted_list_csv, fieldnames=headers)
            for item in self.sorted_dict.values():
                writer.writerow({"Position": item.position, "Name": item.name, "Year": item.year, "URL": item.url,
                                 "Description": item.description})

    @abc.abstractmethod
    def _sorter(self, movie_list: list):
        raise NotImplementedError

    @abc.abstractmethod
    def _movie_object_sorter(self):
        raise NotImplementedError
