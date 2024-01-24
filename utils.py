import markdown
from markupsafe import Markup
from functools import wraps

from flask import redirect, url_for, request, session


def markdown_to_html(markdown_text):
    html = markdown.markdown(markdown_text)
    return Markup(html)


def nl2br(value):
    """Converts newlines in a string to HTML line breaks."""
    return Markup(value.replace("\n", "<br>\n"))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("blog.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function
