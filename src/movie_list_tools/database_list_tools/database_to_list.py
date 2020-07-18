import json

from src.database_pipeline_tools.database_query_tool import DatabaseQueryTool
from src.movie_list_tools.dataclass_helpers import ListMovieObject


class DatabaseToList:
    __slots__ = ("output_location", "output_list_metadata", "input_json", "column", "imdb_col")

    def __init__(self, output_location, output_list_metadata, input_json, column):
        self.output_location = output_location
        self.output_list_metadata = output_list_metadata
        self.input_json = input_json

        self.column = column.split(".")
        if 3 > len(self.column) > 1:
            self.column = self.column[1] if self.column[0] == "imdb_info" else None
            self.imdb_col = True
        elif len(self.column) == 1:
            self.column = self.column[0]
            self.imdb_col = False
        else:
            self.column = None
            raise Exception("There is an issue with the column presented. Will not sort")

    def parse_output_json(self):
        dba = DatabaseQueryTool()
        output_json = json.loads(dba.query_db(self.input_json))
        movie_names = []
        sorted_dict = dict()

        for item in output_json.values():
            # print(item)
            if item.get("movie_title") not in movie_names:
                movie_names.append(item.get("movie_title"))

        if self.column and self.imdb_col is not None:
            movie_names = self.sort_output_json(output_json, movie_names)

        for index, name in enumerate(movie_names, 1):
            item = output_json.get(name)
            sorted_dict[name] = ListMovieObject(position=index,
                                                name=item.get("movie_title"),
                                                year=item.get("year_released"),
                                                url=item.get("letterboxd_link"),
                                                metadata=self.output_list_metadata)

        return sorted_dict

    def sort_output_json(self, output_json, movie_names):

        if self.imdb_col:
            return sorted(movie_names, key=lambda x: output_json.get(x).get("imdb_info").get(self.column))
        else:
            return sorted(movie_names, key=lambda x: output_json.get(x).get(self.column))
