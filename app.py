from flask import Flask, render_template, url_for, redirect
from extensions import db
from forms import PostForm
import os

from dotenv import load_dotenv
from markupsafe import Markup


def nl2br(value):
    """Converts newlines in a string to HTML line breaks."""
    return Markup(value.replace("\n", "<br>\n"))


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "site.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.jinja_env.filters['nl2br'] = nl2br

db.init_app(app)

from models import Post  # noqa: E402


@app.route("/")
def home():
    """Home page for blog."""
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/post/new", methods=["GET", "POST"])
def create_post():
    """Page for creating a new post."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    """Page for viewing a single post."""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Endpoint for deleting a single post."""
    post = Post.query.get_or_404(post_id)
    # Add verification here to make sure the current user is the author of the post
    db.session.delete(post)
    db.session.commit()
    # Flash a message or log the deletion
    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(e):
    """404 page."""
    # Note that we set the 404 status explicitly
    return render_template("404.html"), 404


if __name__ == "__main__":
    """Run the app."""
    app.run(debug=True)
