import re
import yaml

import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from typing import List, Type


def read_yaml(yaml_file_path: str) -> dict:
    with open(yaml_file_path, "r") as file:
        return yaml.safe_load(file)


def _match_string_column_with_length(column_type: str):
    pattern = r"String\((\d+)\)"
    match = re.search(pattern, column_type)
    if match:
        return int(match.group(1))
    else:
        return None


def _get_sqlalchemy_type(type_str_represention: str) -> Type:

    try:
        sqlalchemy_module = __import__("sqlalchemy", fromlist=[type_str_represention])
        len_string_col = _match_string_column_with_length(type_str_represention)
        if len_string_col:
            return _sql.String(len_string_col)

        return getattr(sqlalchemy_module, type_str_represention)
    except AttributeError:
        raise ImportError(
            f"Type string representation'{type_str_represention}' not found in the 'sqlalchemy' module."
        )


def _build_column(name: str, column_type: Type, **kwargs) -> Type[_sql.Column]:
    return _sql.Column(name, column_type, **kwargs)


def _columns_from_dic(columns: dict) -> List[Type[_sql.Column]]:
    parsed_columns = []
    for col in columns:
        col["column_type"] = _get_sqlalchemy_type(col["column_type"])
        parsed_col = _build_column(**col)
        parsed_columns.append(parsed_col)
    return parsed_columns


def build_model_from_yaml(yaml_file_path):

    # Read yaml file with string representation of columns:
    model_data: str = read_yaml(yaml_file_path)

    # Retreive table name or set default:
    table_name = model_data.get("table_name", "PULSE_TABLE")

    # Parse column string representation into a list of sqlalchemy.Column objects
    columns: List[Type[_sql.Column]] = _columns_from_dic(model_data["columns"])

    # Dynamically build sqlalchemy Model:
    base = (_orm.declarative_base(),)
    columns_dic = {col.name: col for col in columns}
    attributes = {"__tablename__": table_name, **columns_dic}
    model_class = type(table_name, base, attributes)
    return model_class
