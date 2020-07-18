from datetime import datetime

from src.movie_list_tools.dataclass_helpers import ListMovieMetadata, ListMovieObject


class GenerateListFromDiary:
    __slots__ = ("diary_items", "list_metadata", "sorted_movie_list")

    def __init__(self, diary_items, list_metadata, sorted_movie_list):
        self.diary_items = diary_items
        self.list_metadata = list_metadata
        self.sorted_movie_list = sorted_movie_list

    def generate_list_items(self):
        return_dict = dict()
        if not self.list_metadata:
            self.list_metadata = ListMovieMetadata(date=datetime.today(),
                                                   name="Gen List",
                                                   url="")
        meta_data_headers = [[], "Date,Name,Tags,URL,Description".split(",")]
        lm = self.list_metadata
        meta_data_headers.append([f"{lm.date.strftime('%Y-%m-%d')}", f"{lm.name}", f"{lm.url}", f"{lm.description}"])
        meta_data_headers.append([])
        meta_data_headers.append(['Position', 'Name', 'Year', 'URL', 'Description'])

        for pos, movie_name in enumerate(self.sorted_movie_list, start=1):
            item = self.diary_items.get(movie_name)
            return_dict[movie_name] = ListMovieObject(position=pos, name=movie_name, year=item.year, url=item.url,
                                                      metadata=self.list_metadata)

        return return_dict
