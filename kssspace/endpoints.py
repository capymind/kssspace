"""
Take Request and Return Response.
"""

from quart import Blueprint, render_template

bp = Blueprint("space", __name__)


@bp.get("/", endpoint="home")
async def home_page():
    return await render_template("pages/home.html")


@bp.get("/giants", endpoint="giants")
async def giants_page():
    return await render_template("pages/giants.html")
