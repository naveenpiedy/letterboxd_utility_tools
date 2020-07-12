import json
import datetime

from src.database_pipeline_tools.base import engine, Session
from src.database_pipeline_tools.models import MovieDatabase, ExtensionIMDB
from sqlalchemy import ARRAY, cast, String


class DatabaseListTools:

    def __init__(self):
        self.session = Session(bind=engine)
        self.input_json = None
        self.main_db_columns = None
        self.imdb_columns = None

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

                try:
                    if key_type is datetime.date:
                        if isinstance(value, dict):
                            lower = datetime.datetime.strptime(value.get('lower'), "%Y-%m-%d").date()
                            higher = datetime.datetime.strptime(value.get('higher'), "%Y-%m-%d").date()
                            if lower > higher:
                                raise Exception(f"For {key}, the lower and higher values need to be interchanged")
                            else:
                                input_json[key]['lower'] = lower
                                input_json[key]['higher'] = higher
                        else:
                            input_json[key] = datetime.datetime.strptime(value, "%Y-%m-%d").date()
                        continue
                except Exception:
                    raise Exception(f"For {key}, the date format is off. Please use Y-M-D.")

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

    def _select_from_database(self, main_db_cols, imdb_cols, input_json):
        query = self.session.query(MovieDatabase).join(ExtensionIMDB)
        arguments = [(main_db_cols, MovieDatabase), (imdb_cols, ExtensionIMDB)]
        try:
            for argument in arguments:
                for key in argument[0]:
                    value = input_json.get(key)
                    if isinstance(value, dict):
                        query = query.filter(
                            getattr(argument[1], key).between(value.get('lower'), value.get('higher')))
                    elif isinstance(value, list):
                        query = query.filter(getattr(argument[1], key).contains(cast(value, ARRAY(String))))
                    else:
                        query = query.filter(getattr(argument[1], key) == value)
            result_list = []
            for item in query:
                result_list.append(item.as_dict())
            return json.dumps(result_list)
        except Exception:
            raise Exception

    def query_db(self, json_input):
        self.input_json = json.loads(json_input)
        self.main_db_columns, self.imdb_columns = self._check_col(self.input_json)
        self._checl_val(self.main_db_columns, self.imdb_columns, self.input_json)
        return self._select_from_database(self.main_db_columns, self.imdb_columns, self.input_json)


if __name__ == '__main__':
    data = {
        "my_rating": {
            "lower": 3,
            "higher": 5
        },
        "rewatch": True,
        "director": ["Wes Anderson"],
        "watchdate": {
            "lower": "2020-05-01",
            "higher": "2020-06-30"
        }
    }
    data = json.dumps(data)
    db = DatabaseListTools()
    print(db.query_db(data))
    # db._checl_val("id", 1, "233")
