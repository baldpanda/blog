from flask import render_template, url_for, redirect, request, flash, session, Blueprint
from app.extensions import db
from app.forms import PostForm
from app.models import Category
import utils as utils
import os
from dotenv import load_dotenv

from app.models import Post  # noqa: E402


load_dotenv()

bp = Blueprint("blog", __name__)


@bp.route("/")
def home():
    """Home page for blog."""
    categories = Category.query.all()
    posts_by_category = {}

    for category in categories:
        posts = Post.query.filter_by(category_id=category.id).all()
        posts_by_category[category.name] = posts

    return render_template("index.html", posts_by_category=posts_by_category)


@bp.route("/post/new", methods=["GET", "POST"])
@utils.login_required
def create_post():
    """Page for creating a new post."""
    form = PostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category_id=form.category.data,
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("blog.home"))
    return render_template("create_post.html", title="New Post", form=form)


@bp.route("/post/<int:post_id>")
def post(post_id):
    """Page for viewing a single post."""
    post = Post.query.get_or_404(post_id)
    post.content = utils.markdown_to_html(post.content)
    return render_template("post.html", post=post)


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
@utils.login_required
def delete_post(post_id):
    """Endpoint for deleting a single post."""
    post = Post.query.get_or_404(post_id)
    # Add verification here to make sure the current user is the author of the post
    db.session.delete(post)
    db.session.commit()
    # Flash a message or log the deletion
    return redirect(url_for("blog.home"))


@bp.errorhandler(404)
def page_not_found(e):
    """404 page."""
    # Note that we set the 404 status explicitly
    return render_template("404.html"), 404


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv(
            "ADMIN_PASSWORD"
        ):
            session["logged_in"] = True
            flash("You were successfully logged in")
            return redirect(url_for("blog.home"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("blog.home"))


@bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@utils.login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Add authorization check here if needed
    form = PostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for("blog.home"))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("edit_post.html", title="Edit Post", form=form)
