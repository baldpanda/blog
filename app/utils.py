import markdown
from markupsafe import Markup

def markdown_to_html(markdown_text):
    html = markdown.markdown(markdown_text)
    return Markup(html)


def nl2br(value):
    """Converts newlines in a string to HTML line breaks."""
    return Markup(value.replace("\n", "<br>\n"))