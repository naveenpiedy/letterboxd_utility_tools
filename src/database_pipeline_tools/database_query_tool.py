import itertools
import json
import datetime

from src.database_pipeline_tools.base import engine, Session
from src.database_pipeline_tools.models import MovieDatabase, ExtensionIMDB
from sqlalchemy import ARRAY, cast, String


class DatabaseQueryTool:
    """
    Sample Input Json.

    {
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


    Selecting movies based on a range, for example 3 - 4 stars or between April 1 - June 1, use 'lower' and 'higher'
    Dates should be be of format `yyyy-mm-dd`

    List Arguments example:

    "genres": [["Drama"], ["Romance"]]

    Will return
    Alaipayuthey ['Drama', 'Musical', 'Romance']

    "genres": ["Drama", "Romance"]

    Will return
    The Darjeeling Limited ['Adventure', 'Comedy', 'Drama']
    Alaipayuthey ['Drama', 'Musical', 'Romance']

    The difference being that nested lists will emulate AND while a single list will emulate OR.
    """

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
                    flat_values = itertools.chain(*value)
                    for item in flat_values:
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
                        if any(isinstance(i, list) for i in value):
                            for inner_value in value:
                                query = query.filter(getattr(argument[1], key).overlap(cast(inner_value,
                                                                                            ARRAY(String))))
                        else:
                            query = query.filter(getattr(argument[1], key).overlap(cast(value, ARRAY(String))))
                    else:
                        query = query.filter(getattr(argument[1], key) == value)
            result_list = dict()
            for item in query:
                result_list[item.movie_title] = item.as_dict()
            return json.dumps(result_list)
        except Exception:
            raise Exception

    def query_db(self, json_input):
        self.input_json = json.loads(json_input)
        self.main_db_columns, self.imdb_columns = self._check_col(self.input_json)
        self._checl_val(self.main_db_columns, self.imdb_columns, self.input_json)
        return self._select_from_database(self.main_db_columns, self.imdb_columns, self.input_json)


if __name__ == '__main__':
    # data = {
    #     "watchdate": {
    #         "lower": "2021-02-28",
    #         "higher": "2021-12-31"
    #     },
    # }

    data = {
        "watchdate": {
                    "lower": "2022-11-01",
                    "higher": "2023-01-31"
        },
        # "languages": ["Tamil", "Telugu"],
        # "my_rating": {
        #     "lower": "3.5",
        #     "higher": "5"
        # },
        # 'genres': [["Horror"]],
        # "rewatch": False
        # "year": 2022
    }

    data = json.dumps(data)
    db = DatabaseQueryTool()
    result = json.loads(db.query_db(data))
    # for i, j in enumerate(result.keys(), start=1):
    #     print(i, j, result[j].get("my_rating"))
    # rating_list = []
    # for i in result:
    #     rating = None
    #     try:
    #         rating = result[i].get("imdb_info").get("rating") / 2
    #     except:
    #         pass
    #     rating_list.append({
    #         "my_rating": result[i].get("my_rating"),
    #         "imdb_rating": rating,
    #         "title": result[i].get("movie_title"),
    #         "genres": result[i].get("imdb_info").get("genres"),
    #         "year": result[i].get("year_released"),
    #         "languages": result[i].get("imdb_info").get("languages"),
    #         "watchdate": result[i].get("watchdate"),
    #         "rewatch": result[i].get("rewatch"),
    #     })

    # print(rating_list)
    # with open('bla.json', 'w') as outfile:
    #     json.dump(rating_list, outfile)
    print(result)
