from flask import Flask
from app.extensions import db
import utils as utils
import os

from dotenv import load_dotenv


load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static", instance_relative_config=True)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_PATH")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.jinja_env.filters["nl2br"] = utils.nl2br
    app.jinja_env.filters["markdown"] = utils.markdown_to_html

    if test_config is not None:
        # Load the test configuration if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)
    from app.routes import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')
    return app
