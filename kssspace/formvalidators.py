"""
All kinds of form validators.

What is form?
- any kind of data __from user__.
"""

from flask import Request

from kssspace.types import InvalidData


class MessageCode:
    TOO_SHORT_OR_TOO_LONG = 1
    TOO_MANY_TAGS = 2


def giant_searchword_validator(searchword: str):
    if len(searchword) <= 20:
        return True, searchword
    return False, InvalidData(
        dict(
            code=MessageCode.TOO_SHORT_OR_TOO_LONG,
            message=f"인물명은 20자 이내여야 합니다.(현재: {len(searchword)}자)",
        )
    )


def giant_searchtags_validator(searchtags: list[str | None]):
    if len(searchtags) <= 3:
        return True, searchtags
    return False, InvalidData(
        dict(
            code=MessageCode.TOO_MANY_TAGS,
            message=f"태그 검색은 최대 3개까지 가능합니다. (현재: {len(searchtags)}개)",
        )
    )


def get_searchword(request: Request):
    searchword = request.args["q"]
    return giant_searchword_validator(searchword)


def get_searchtags(request: Request):
    searchtags = request.args.getlist("tag")
    return giant_searchtags_validator(searchtags)


def get_search_style(request: Request):
    """
    현재는 검색어로 인한 검색과 태그로 인한 검색을 각각 하는 기능만 제공한다.

    즉,
        - Python 태그로 검색
        - Guido 검색어로 검색
    은 가능 하지만, 아래처럼
        - Python 태그와 Guido 검색어로 검색
    은 불가능하다.
    """
    if request.args.get("q") is not None:
        return "searchword"
    if request.args.getlist("tag-search-condition") is not None:
        return "searchtag"
