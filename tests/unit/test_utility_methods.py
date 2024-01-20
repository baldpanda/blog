from utils import nl2br, markdown_to_html

from markupsafe import Markup

class TestUtilMethods:
    def test_nl2br(self):
        assert nl2br("Hello\nWorld") == Markup("Hello<br>\nWorld")

    def test_markdown_to_html(self):
        """"Should convert markdown to HTML."""

        # Arrange
        expected_result = Markup("<h1>Hello</h1>")

        # Act
        actual_result = markdown_to_html("# Hello")

        # Assert
        assert actual_result == expected_result