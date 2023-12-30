import tomllib
from quart import Quart
from quart_db import QuartDB


from kssspace.endpoints import bp, giants, learn


def create_app(mode: str = "development") -> Quart:
    """Create Quart app instance."""

    match mode:
        case "production":
            instance_path = "/kssspace/instance"
        case "development":
            instance_path = "/home/rodi/projects/kssspace/instance"

    app = Quart(
        __name__,
        instance_path=instance_path,
        instance_relative_config=True,
    )

    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config.from_file("config/config.toml", load=tomllib.load, text=False)

    # Database connection extension.
    db = QuartDB()
    db.init_app(app)

    # Register blueprints.
    app.register_blueprint(bp)
    app.register_blueprint(learn, url_prefix="/learn")
    app.register_blueprint(giants, url_prefix="/giants")

    return app
