import datetime
from typing import Any

from .sort_by_diary import ReadDiary, check_col


def check_values(col: str, lower_value: Any, higher_value: Any):
    """
    Check if the values are of the proper datatype and col is proper column.
    """
    col = check_col(col)

    col_type_mapper = {
        "date": datetime.date,
        "year": int,
        "rating": float,
        "watched_date": datetime.date}

    if not isinstance(lower_value, col_type_mapper.get(col)):
        raise Exception(f"Mentioned lower value is not of the right data type. You have given {type(lower_value)}"
                        f"For {col} use {col_type_mapper.get(col)}")

    if not isinstance(higher_value, col_type_mapper.get(col)):
        raise Exception(f"Mentioned higher value is not of the right data type. You have given "
                        f"{type(higher_value)}"
                        f"For {col} use {col_type_mapper.get(col)}")

    if lower_value > higher_value:
        raise Exception("Lower Value is greater than higher value, please change")

    return col, lower_value, higher_value


def read_part_diary(diary_location, lower_value, higher_value, col):
    col, lower_value, higher_value = check_values(col, lower_value, higher_value)
    index_col = {
        "date": 0,
        "year": 2,
        "rating": 4,
        "watched_date": 7,
    }

    col_type_lambda = {
        0: lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
        2: lambda x: int(x),
        4: lambda x: float(x),
        7: lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date()
    }

    index = index_col.get(col)
    rd = ReadDiary(diary_location)
    return rd.read_diary(lambda x: lower_value <= col_type_lambda.get(index)(x[index]) <= higher_value)


def sort_diary_items(diary_items: dict, col: str, reverse: bool = False):
    """
    Sorts the movies based on the column, lower_value and higher_value.
    """
    col = check_col(col)
    return sorted(diary_items.keys(),
                  key=lambda x: getattr(diary_items.get(x), col),
                  reverse=reverse)
