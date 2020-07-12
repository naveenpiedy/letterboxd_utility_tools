import json
from datetime import datetime

from src.database_pipeline_tools.database_query_tool import DatabaseQueryTool
from src.movie_list_tools.movie_list_sorter import ListBaseClass
from src.movie_list_tools.dataclass_helpers import ListMovieObject, ListMovieMetadata


class DatabaseToList(ListBaseClass):

    def __init__(self, file_location: str, list_name: str, input_json: json, column: str = None):
        super().__init__(file_location, list_name)
        self.input_json = input_json
        self.output_json = None
        self.list_name = list_name if list_name else "Gen List"
        self.listmetadata = ListMovieMetadata(date=datetime.today(),
                                              name=self.list_name,
                                              url="")
        self.column = column.split(".")
        if len(self.column) > 1:
            self.column = self.column[1] if self.column[0] == "imdb_info" else None
            self.imdb_col = True
        else:
            self.column = self.column[0]
            self.imdb_col = False

    def get_details(self):
        dba = DatabaseQueryTool()
        self.output_json = json.loads(dba.query_db(self.input_json))

    def gen_first_lines(self):
        meta_data_headers = [[], "Date,Name,Tags,URL,Description".split(",")]
        lm = self.listmetadata
        meta_data_headers.append([f"{lm.date.strftime('%Y-%m-%d')}", f"{lm.name}", f"{lm.url}", f"{lm.description}"])
        meta_data_headers.append([])
        meta_data_headers.append(['Position', 'Name', 'Year', 'URL', 'Description'])
        self.first_lines = meta_data_headers

    def json_list_objects(self):

        for item in self.output_json.values():
            print(item)
            if item.get("movie_title") not in self.movie_names:
                self.movie_names.append(item.get("movie_title"))

    def _sorter(self, imdb_col: bool = False, movie_list: list = None):
        if imdb_col:
            self.movie_names = sorted(self.movie_names,
                                      key=lambda x: self.output_json.get(x).get("imdb_info").get(self.column))
        else:
            self.movie_names = sorted(self.movie_names, key=lambda x: self.output_json.get(x).get(self.column))
        print(self.movie_names)

    def _movie_object_sorter(self):
        for index, name in enumerate(self.movie_names, 1):
            item = self.output_json.get(name)
            self.sorted_dict[name] = ListMovieObject(position=index,
                                                     name=item.get("movie_title"),
                                                     year=item.get("year_released"),
                                                     url=item.get("letterboxd_link"),
                                                     metadata=self.listmetadata)

    def generate_list(self):
        db.get_details()
        db.json_list_objects()
        db.gen_first_lines()
        db._sorter(imdb_col=self.imdb_col)
        db._movie_object_sorter()
        db._write_list_csv()


if __name__ == '__main__':
    data = {
        "my_rating": {
            "lower": 3,
            "higher": 5
        },
        "genres": [["Drama"], ["Romance"]],
        "watchdate": {
            "lower": "2020-04-01",
            "higher": "2020-06-30"
        },
        "director": ["Wes Anderson", "Mani Ratnam"]
    }

    db = DatabaseToList(file_location="E:\\Movie Data\\letterboxd-naveenpiedy-jun", list_name="gen_test",
                        input_json=json.dumps(data), column="imdb_info.director")
    db.generate_list()
