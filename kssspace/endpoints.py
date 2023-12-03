"""
Take Request and Return Response.
"""

from quart import Blueprint, g, render_template, request, make_response

from kssspace.formvalidators import get_searchword, get_searchtags, get_search_style
from kssspace.dbactions import (
    fetch_all_giants,
    search_giants,
    fetch_all_tags,
    search_giants_by_tags,
)
from kssspace.types import InvalidData

bp = Blueprint("space", __name__)
learn = Blueprint("learn", __name__)
giants = Blueprint("giants", __name__)


@bp.get("/", endpoint="home")
async def home_page():
    return await render_template("pages/home.html")


@giants.get("/", endpoint="page::index")
async def giants_page():
    giants = await fetch_all_giants(g.connection)
    giant_tags = await fetch_all_tags(g.connection, "giant")

    return await render_template(
        "giants/pages/index.html",
        giants=giants,
        giant_tags=giant_tags,
    )


@giants.get("/search", endpoint="search")
async def giants_search():
    search_style = get_search_style(request)

    if search_style == "searchword":
        match get_searchword(request):
            case True, searchword:
                giants = await search_giants(g.connection, searchword)
                return await render_template(
                    "giants/fragments/giant-search__valid.html",
                    giants=giants,
                )
            case False, invalid:
                return await render_template(
                    "giants/fragments/giant-search__invalid.html",
                    invalid=invalid,
                )

    if search_style == "searchtag":
        match get_searchtags(request):
            case True, searchtags:
                giants = await search_giants_by_tags(
                    g.connection,
                    searchtags,
                    request.args.get("tag-search-condition"),
                )
                return await render_template(
                    "giants/fragments/giant-search__valid.html",
                    giants=giants,
                )
            case False, invalid:
                return await render_template(
                    "giants/fragments/giant-search__invalid.html",
                    invalid=invalid,
                )


@learn.get("/", endpoint="page::index")
async def learn_page():
    return await render_template("learn/pages/index.html")
