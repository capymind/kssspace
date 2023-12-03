"""
Database 'S'yncrhonous Actions. (db's'action)
"""
import copy
from typing import Any

from sqlalchemy import create_engine, delete
from sqlalchemy.dialects.sqlite import insert

from kssspace.tables import (
    giant as giant_table,
)
from kssspace.tables import (
    giant_tag as giant_tag_table,
)
from kssspace.tables import (
    giant_tag_assoc as giant_tag_assoc_table,
)

engine = create_engine("sqlite:///instance/kssspace.sqlite")


def upsert(target: str, data: Any):
    match target:
        case "giant":
            stmt = insert(giant_table)
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=[giant_table.c.name],
                set_=dict(
                    description=stmt.excluded.description,
                    mastodon=stmt.excluded.mastodon,
                    github=stmt.excluded.github,
                    homepage=stmt.excluded.homepage,
                    twitter_x=stmt.excluded.twitter_x,
                ),
            )
            with engine.begin() as conn:
                conn.execute(upsert_stmt, data)
        case _:
            return


def delete_and_insert(target: str, data: Any):
    data = copy.deepcopy(data)
    match target:
        case "giant":
            with engine.begin() as conn:
                conn.execute(delete(giant_table))
                giant_ids = conn.execute(
                    insert(giant_table).returning(
                        giant_table.c.id, sort_by_parameter_order=True
                    ),
                    data,
                ).scalars()
                for giant_id, item in zip(giant_ids, data):
                    item["id"] = giant_id
                return data
        case "giant_tag":
            with engine.begin() as conn:
                conn.execute(delete(giant_tag_table))
                result = conn.execute(
                    insert(giant_tag_table).returning(
                        giant_tag_table.c.name,
                        giant_tag_table.c.id,
                    ),
                    [dict(name=tag_name) for tag_name in data],
                )
                tag_map = dict()
                for tag_item in [{k: v} for k, v in result.all()]:
                    tag_map |= tag_item
                return tag_map
        case "giant_tag_assoc":
            with engine.begin() as conn:
                conn.execute(delete(giant_tag_assoc_table))
                conn.execute(insert(giant_tag_assoc_table), data)
