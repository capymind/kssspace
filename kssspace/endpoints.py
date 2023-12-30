"""
Take Request and Return Response.
"""

from quart import Blueprint, g, render_template, request
from kssspace.utils import get_markdown_converter
from kssspace.dbactions import (
    fetch_all_giants,
    fetch_all_tags,
    search_giants,
    fetch_note_by_slug,
    search_giants_by_tags,
    fetch_all_notes,
)
from kssspace.formvalidators import get_search_style, get_searchtags, get_searchword

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
    notes = await fetch_all_notes(g.connection)
    return await render_template("learn/pages/index.html", notes=notes)


@learn.get("/<slug>", endpoint="page::note")
async def learn_note_page(slug: str):
    """show individual note page."""

    note = await fetch_note_by_slug(g.connection, slug)
    mc = get_markdown_converter()
    note["body"] = mc.convert(note["body"])

    return await render_template("learn/pages/note.html", note=note)
