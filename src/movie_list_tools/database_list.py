from src.movie_list_tools.movie_list_sorter import ListBaseClass
from src.database_pipeline_tools.base import engine, Session
from src.database_pipeline_tools.models import MovieDatabase  # , ExtensionIMDB


class DatabaseListTools(ListBaseClass):
    def __init__(self, file_location: str = None, list_name: str = None, database_flag: int = 0, column: str = None,
                 value: str = None):
        super().__init__(file_location, list_name)
        self.session = Session(bind=engine)
        self.database_flag = database_flag
        self.column = self._check_col(database_flag, column)
        self.value = self._checl_val(self.column, self.database_flag)

    def _sorter(self, movie_list: list):
        pass

    def _movie_object_sorter(self):
        pass

    def select_from_database(self, database_flag=None, column=None, value=None):
        for movie in self.session.query(MovieDatabase).filter(MovieDatabase.my_rating.between("4.0", "4.5")):
            print(movie.imdb_db.title, movie.imdb_db.director)

    def _check_col(self, database_flag, column):
        return None

    def _checl_val(self, column, database_flag):
        return None


if __name__ == '__main__':
    db = DatabaseListTools()
    db.select_from_database()
