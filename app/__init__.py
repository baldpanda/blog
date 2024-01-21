from flask import Flask, render_template, url_for, redirect, request
from app.extensions import db
from app.forms import PostForm
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

from app.models import Post  # noqa: E402


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
    post.content = utils.markdown_to_html(post.content)
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


@app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Add authorization check here if needed
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        # Redirect to the post view or homepage after editing
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("edit_post.html", title="Edit Post", form=form)


if __name__ == "__main__":
    """Run the app."""
    app.run(debug=True)
