import datetime
from typing import Any, Dict, List

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


def read_part_diary(diary_location: str, lower_value: Any, higher_value: Any, col: str) -> (Dict, Dict):
    """
    This function is used to read only part of the diary CSV. Should be useful in generating lists based on select
    values from certain columns. Example: List of movies between rating 3-5.
    :param diary_location: Path to diary csv location
    :param lower_value: Lower bound value
    :param higher_value: Higher bound value
    :param col: Column which contains the lower bound and upper bound values
    :return: tuple containing diary_items and rewatch_dict
    """
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


def sort_diary_items(diary_items: Dict, col: str, reverse: bool = False) -> List:
    """
    Sorts the movies based on the column, lower_value and higher_value.
    :param diary_items: Diary items which needs to be sorted
    :param col: Column based on which the diary_items needs to be sorted
    :param reverse: Bool to specify Ascending or Descending order.
    :return: List of sorted movie names based on input column.
    """
    col = check_col(col)
    return sorted(diary_items.keys(),
                  key=lambda x: getattr(diary_items.get(x), col),
                  reverse=reverse)
