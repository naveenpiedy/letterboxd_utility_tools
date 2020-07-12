import json
from datetime import datetime

from src.database_pipeline_tools.database_query_tool import DatabaseQueryTool
from src.movie_list_tools.movie_list_sorter import ListBaseClass
from src.movie_list_tools.dataclass_helpers import ListMovieObject, ListMovieMetadata


class DatabaseToList(ListBaseClass):

    def __init__(self, file_location: str, list_name: str, input_json):
        super().__init__(file_location, list_name)
        self.input_json = input_json
        self.output_json = None
        self.list_name = list_name if list_name else "Gen List"
        self.listmetadata = ListMovieMetadata(date=datetime.today(),
                                              name=self.list_name,
                                              url="")

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

        for item in self.output_json:
            print(item)
            if item.get("movie_title") not in self.list_item_dicts:
                self.movie_names.append(item.get("movie_title"))
                self.list_item_dicts[item.get("movie_title")] = ListMovieObject(position=len(self.movie_names),
                                                                                name=item.get("movie_title"),
                                                                                year=item.get("year_released"),
                                                                                url=item.get("letterboxd_link"),
                                                                                metadata=self.listmetadata)
        self.sorted_dict = self.list_item_dicts

    def _sorter(self, movie_list: list):
        pass

    def _movie_object_sorter(self):
        pass


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
                        input_json=json.dumps(data))
    db.get_details()
    db.json_list_objects()
    db.gen_first_lines()
    db._write_list_csv()
