import csv
import logging
import os
from datetime import datetime

from src.movie_list_tools.dataclass_helpers import ListMovieMetadata, ListMovieObject

LISTS_FOLDER = "lists"
OUTPUT_FOLDER = "output"
HEADERS = ['Position', 'Name', 'Year', 'URL', 'Description']
META_DATA_HEADERS = ["Date", "Name", "Tags", "URL", "Description"]


class MovieListCSVReader:

    __slots__ = ("directory", "list_name")

    def __init__(self, directory: str, list_name: str):
        self.directory, self.list_name = directory, list_name

    def read_list_csv(self):
        """
        Reads LetterBoxd List csv.
        """
        try:
            list_location = os.path.join(self.directory, LISTS_FOLDER, self.list_name)
            list_item_dict = dict()
            with open(list_location) as csvfile:
                contents = csv.reader(csvfile, delimiter=',')
                for index, line in enumerate(contents):
                    if index <= 4:
                        if index == 2:
                            meta = ListMovieMetadata(date=datetime.strptime(line[0], '%Y-%m-%d').date(),
                                                     name=line[1], url=line[3], description=line[4])
                    else:
                        list_item_dict[line[1]] = ListMovieObject(position=int(line[0]), name=line[1],
                                                                  year=int(line[2]), url=line[3],
                                                                  description=line[4], metadata=meta)
            if not list_item_dict:
                raise Exception("This file is empty")
            return list_item_dict
        except FileNotFoundError:
            raise FileNotFoundError


class MovieListCSVWriter:

    __slots__ = ("directory", "list_items")

    def __init__(self, directory: str, list_items: dict):
        self.directory, self.list_items = directory, list_items,

    @staticmethod
    def metadata_line_builder(meta: ListMovieMetadata):

        metadata_str = [f"{meta.date.strftime('%Y-%m-%d')}", f"{meta.name}", '', f"{meta.url}", f"{meta.description}"]
        return [[], META_DATA_HEADERS, metadata_str, [], HEADERS]

    def write_list_csv(self):
        """
        Generates a LetterBoxd compliant list csv based on order in self.sorted_dict
        """
        try:
            output_location = os.path.join(self.directory, OUTPUT_FOLDER)
            try:
                os.makedirs(output_location)
            except FileExistsError:
                logging.info("Output Directory already exists")

            meta = None
            if self.list_items:
                meta = getattr(next(iter(self.list_items.values())), "metadata")

            list_name = None
            if meta:
                list_name = getattr(meta, "name")

            if not list_name:
                list_name = "gen"

            with open(os.path.join(output_location, f"{list_name}_output.csv"), mode='w', newline='') as list_csv:

                first_lines_writer = csv.writer(list_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for line in self.metadata_line_builder(meta=meta):
                    first_lines_writer.writerow(line)

                writer = csv.DictWriter(list_csv, fieldnames=HEADERS)
                for values in self.list_items.values():
                    writer.writerow({"Position": values.position, "Name": values.name, "Year": values.year,
                                     "URL": values.url, "Description": values.description})

        except Exception:
            raise Exception
