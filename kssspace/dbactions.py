"""
Actions to Database.

What are actions?
    CRUD(Create, Read, Update, Delete)
"""
import copy
from typing import Any

from quart_db import Connection
from sqlalchemy import text

from kssspace.sqls import (
    FETCH_ALL_GIANTS_SQL,
    SEARCH_GIANTS_SQL,
    FETCH_ALL_GIANT_TAGS,
    get_search_giants_by_tags_sql,
)


async def fetch_all_giants(conn: Connection):
    stmt = str(text(FETCH_ALL_GIANTS_SQL))
    data = await conn.fetch_all(stmt)
    data = _split_concatenated_values(data, "tag_names", ",")
    return data


async def fetch_all_tags(conn: Connection, taggedclass: str):
    match taggedclass:
        case "giant":
            stmt = str(text(FETCH_ALL_GIANT_TAGS))
            data = await conn.fetch_all(stmt)
            return data
        case _:
            raise ValueError(f"wrong taggedclass: {taggedclass}")


async def search_giants(conn: Connection, searchword: str):
    stmt = str(text(SEARCH_GIANTS_SQL))
    data = await conn.fetch_all(stmt, values=dict(searchword=searchword))
    data = _split_concatenated_values(data, "tag_names", ",")
    return data


async def search_giants_by_tags(
    conn: Connection,
    searchtags: list[str],
    and_or_condition: str,
):
    num_of_tags = len(searchtags)

    if num_of_tags > 0:
        in_ = ", ".join(f":tag{i}" for i in range(num_of_tags))
        stmt = get_search_giants_by_tags_sql(and_or_condition, in_, num_of_tags)
        values = {f"tag{k}": v for k, v in enumerate(searchtags)}
        data = await conn.fetch_all(stmt, values=values)
        data = _split_concatenated_values(data, "tag_names", ",")
    else:
        data = await fetch_all_giants(conn)
    return data


def _split_concatenated_values(
    data: list[dict[str, Any]],
    key: str,
    sep: str,
) -> list[dict[str, Any]]:
    """Split concatenated value in given 'key' to list of values."""

    data = copy.deepcopy(data)
    for d in data:
        d[key] = d[key].split(sep) if d[key] is not None else None
    return data
