from quart import Quart
from kssspace.endpoints import bp

app = Quart(__name__)

app.register_blueprint(bp)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run()