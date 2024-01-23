from flask import Flask
from app.extensions import db
import utils as utils
import os

from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_PATH")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.jinja_env.filters["nl2br"] = utils.nl2br
app.jinja_env.filters["markdown"] = utils.markdown_to_html


db.init_app(app)

from app.routes import app


if __name__ == "__main__":
    """Run the app."""
    app.run(debug=True)
