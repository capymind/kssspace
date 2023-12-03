"""
CLI(Command Line Interface)
"""

import copy
from typing import Any

import click

from kssspace.dbsactions import delete_and_insert
from kssspace.types import GiantRecord, TagId, TagName
from kssspace.utils import read_giants_from_toml


def _get_all_tags(giants: list[GiantRecord]) -> set[str]:
    tags = set()
    for giant in giants:
        tags |= set(giant.get("tags"))
    return tags


def _tag_names_to_tag_ids(
    giants: list[GiantRecord],
    tag_map: dict[TagName, TagId],
) -> list[GiantRecord]:
    """Convert GiantRecord's tags of names to tags of ids."""
    giants = copy.deepcopy(giants)
    for giant in giants:
        tag_names = giant.get("tags")
        tag_ids = [tag_map.get(tag_name) for tag_name in tag_names]
        giant.update(dict(tags=tag_ids))
    return giants


def _create_assoc(
    record_type: str,
    records: list[Any],
) -> list[dict[str, Any]]:
    match record_type:
        case "giant":
            assoc = []
            for giant in records:
                giant_id = giant.get("id")
                tag_ids = giant.get("tags")
                for tag_id in tag_ids:
                    assoc.append(dict(giant_id=giant_id, tag_id=tag_id))
            return assoc
        case _:
            raise ValueError(f"지원하지 않는 양식입니다. {record_type}")


@click.group()
def cli():
    pass


@click.command()
def giants_to_sqlite():
    """read giants.toml and save in sqlite."""

    filepath = "kssspace/data/giants/giants.toml"
    giants = read_giants_from_toml(filepath)
    giant_tags = _get_all_tags(giants)

    giants = delete_and_insert("giant", giants)
    giant_tags = delete_and_insert("giant_tag", giant_tags)

    giants = _tag_names_to_tag_ids(giants, giant_tags)
    giant_tag_assoc = _create_assoc("giant", giants)
    delete_and_insert("giant_tag_assoc", giant_tag_assoc)

    click.echo(
        f"[done] giants.toml --> sqlite |"
        f" giants:{len(giants)} | tags: {len(giant_tags)} |"
    )


cli.add_command(giants_to_sqlite)

if __name__ == "__main__":
    cli()
