"""
Utility functions.

성격이 제각각인 놈들이 모여있는데, 디렉토리, 
모듈 재구성 및 리네임(rename)을 생각해봐야함.
"""

import markdown
from collections import Counter
from typing import Any

import tomllib

from kssspace.types import GiantRecord


class DuplicatedNameError(Exception):
    pass


def exclude_keys(
    dict_: dict[str, Any],
    keys: list[str],
) -> dict[str, Any]:
    """Return new dict without `keys`."""
    target_keys = dict_.keys() - set(keys)
    return dict([item for item in dict_.items() if item[0] in target_keys])


def include_keys(
    dict_: dict[str, Any],
    keys: list[str],
) -> dict[str, Any]:
    """Return new dict with `keys` only."""
    return dict([item for item in dict_.items() if item[0] in keys])


def read_giants_from_toml(filename: str) -> list[GiantRecord]:
    """read given filename."""

    try:
        with open(filename, "rb") as file:
            data = tomllib.load(file)
    except Exception as exc:
        print(exc)
        raise (exc)
    else:
        giants = data.get("giants")
        names = [giant["name"] for giant in giants]
        counter = Counter(names)
        duplicates = []
        for name, count in counter.most_common():
            if count > 1:
                duplicates.append(name)
            else:
                break
        if len(duplicates) > 0:
            raise DuplicatedNameError(f"동일한 이름이 존재합니다. {duplicates}")

        return giants


def get_markdown_converter() -> markdown.Markdown:
    """convert given markdown text to html."""
    return markdown.Markdown(
        extensions=[
            "meta",
            "fenced_code",
            "codehilite",
            "toc",
        ],
        output_format="html",
    )
