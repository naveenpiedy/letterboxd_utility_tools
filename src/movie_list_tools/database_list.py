from src.movie_list_tools.movie_list_sorter import ListBaseClass
from src.database_pipeline_tools.base import engine, Session
from src.database_pipeline_tools.models import MovieDatabase, ExtensionIMDB


class DatabaseListTools(ListBaseClass):

    MAIN_DB_FLAG = 0
    IMDB_FLAG = 1

    def __init__(self, file_location: str = None, list_name: str = None, database_flag: int = 0, column: str = None,
                 value: str = None):
        super().__init__(file_location, list_name)
        self.session = Session(bind=engine)
        self.database_flag = database_flag
        # self.column = self._check_col(database_flag, column)
        # self.value = self._checl_val(self.column, self.database_flag, value)

    def _check_col(self, database_flag, column):
        database_obj = ExtensionIMDB if database_flag else MovieDatabase
        columns_available = database_obj.__table__.columns._data.keys()
        if hasattr(database_obj, column):
            return column
        else:
            raise Exception(f"Mentioned column name is not usable. Please use one of {columns_available}")

    def _checl_val(self, column=None, database_flag=0, value=None):
        database_obj = ExtensionIMDB if database_flag else MovieDatabase
        column = database_obj.__table__.columns._data.get(column)

        column_type = column.type.python_type

        if column_type == list:
            column_type = column.type.item_type.python_type
            bool_value = isinstance(value, column_type)
        else:
            bool_value = isinstance(value, column_type)
        if bool_value:
            return value
        else:
            raise Exception(f"Value is not of proper type. Please use one of {column_type}")

    def _sorter(self, movie_list: list):
        pass

    def _movie_object_sorter(self):
        pass

    def _value_parser(self):
        pass

    def select_from_database(self, database_flag=None, column=None, value=None):
        for movie in self.session.query(MovieDatabase).filter(MovieDatabase.my_rating.between("4.0", "4.5")):
            print(movie.imdb_db.title, movie.imdb_db.director)


if __name__ == '__main__':
    db = DatabaseListTools()
    db._checl_val("genres", 1, 233)
