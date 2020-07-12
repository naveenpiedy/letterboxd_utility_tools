import json

from src.movie_list_tools.movie_list_sorter import ListBaseClass
from src.database_pipeline_tools.base import engine, Session
from src.database_pipeline_tools.models import MovieDatabase, ExtensionIMDB
from sqlalchemy import ARRAY, cast, String


class DatabaseListTools(ListBaseClass):

    def __init__(self, file_location: str = None, list_name: str = None, database_flag: int = 0, json_input=None):
        super().__init__(file_location, list_name)
        self.session = Session(bind=engine)
        self.database_flag = database_flag
        self.input_json = json.loads(json_input)
        self.main_db_columns, self.imdb_columns = self._check_col(self.input_json)
        self._checl_val(self.main_db_columns, self.imdb_columns, self.input_json)
        self.select_from_database(self.main_db_columns, self.imdb_columns, self.input_json)

    def _check_col(self, json_input):
        main_db_columns = set()
        imdb_columns = set()

        for key in json_input.keys():
            if hasattr(MovieDatabase, key):
                main_db_columns.add(key)
            elif hasattr(ExtensionIMDB, key):
                imdb_columns.add(key)
            else:
                raise Exception(f"{key} column is not found.")
        return main_db_columns, imdb_columns

    @staticmethod
    def _type_builder(cols, db_obj):

        ret = dict()

        for key in cols:
            column = db_obj.__table__.columns._data.get(key)
            column_type = column.type.python_type
            if column_type == list:
                column_type = column.type.item_type.python_type
            ret[key] = column_type

        return ret

    def _checl_val(self, main_db_cols, imdb_cols, input_json):
        main_db_type = self._type_builder(main_db_cols, MovieDatabase)
        imdb_type = self._type_builder(imdb_cols, ExtensionIMDB)

        for key, value in input_json.items():
            try:
                if key in main_db_type:
                    key_type = main_db_type.get(key)
                else:
                    key_type = imdb_type.get(key)
                if isinstance(value, dict):
                    lower = key_type(value.get('lower'))
                    higher = key_type(value.get('higher'))
                    if lower > higher:
                        raise Exception(f"For {key}, the lower and higher values need to be interchanged")
                elif isinstance(value, list):
                    for item in value:
                        if not isinstance(item, key_type):
                            raise Exception(f"For {key}, the data_type of {item} if off. It needs to be of {key_type}")
                else:
                    if not isinstance(value, key_type):
                        raise Exception(f"For {key}, the data_type of {value} if off. It needs to be of {key_type}")
            except Exception:
                raise Exception(f"For {key}, the data_type of {value} if off.")

    def select_from_database(self, main_db_cols, imdb_cols, input_json):
        query = self.session.query(MovieDatabase).join(ExtensionIMDB)
        try:
            for key in main_db_cols:
                value = input_json.get(key)
                if isinstance(value, dict):
                    query = query.filter(getattr(MovieDatabase, key).between(value.get('lower'), value.get('higher')))
                elif isinstance(value, list):
                    query = query.filter(getattr(MovieDatabase, key).any(value)).all()
                else:
                    query = query.filter(getattr(MovieDatabase, key) == value)
            for key in imdb_cols:
                value = input_json.get(key)
                if isinstance(value, dict):
                    query = query.filter(getattr(ExtensionIMDB, key).between(value.get('lower'), value.get('higher')))
                elif isinstance(value, list):
                    query = query.filter(getattr(ExtensionIMDB, key).contains(cast(value, ARRAY(String))))
                else:
                    query = query.filter(getattr(ExtensionIMDB, key) == value)
            for movie in query:
                print(movie.movie_title)
        except Exception:
            raise Exception

        # for movie in self.session.query(MovieDatabase).filter(MovieDatabase.my_rating.between("4.0", "4.5")):
        #     print(movie.imdb_db.title, movie.imdb_db.director)

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
        "languages": ["Tamil"],
        "genres": ["Comedy"],
        "rewatch": True,
    }
    data = json.dumps(data)
    db = DatabaseListTools(json_input=data)
    # db._checl_val("id", 1, "233")
