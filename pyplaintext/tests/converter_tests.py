"""Tests for the converter module."""
import textwrap
import unittest

from .. import converter


class HTML2PlainParserTestCase(unittest.TestCase):
    """Tests for the ``HTML2PlainParser`` class."""
    def test_instantiation(self):
        instance = converter.HTML2PlainParser(
            ignored_elements=[],
            newline_before_elements=[],
            newline_after_elements=[],
            stroke_before_elements=[],
            stroke_after_elements=[],
            stroke_text='',
        )
        self.assertTrue(instance, msg=(
            'Should instantiate the class'))

    def test_html_to_plain_text(self):
        html = (
            """
            <html>
                    <head></head>
                    <body>
                        <ul>
                            <li>List element</li>
                            <li>List element</li>
                            <li>List element</li>
                        </ul>
                    </body>
                </html>
            """
        )
        parser = converter.HTML2PlainParser()
        result = parser.html_to_plain_text(html)
        self.assertEqual(
            result,
            '\n  * List element\n  * List element\n  * List element',
            msg='Should return a formatted plain text.')

    def test_replace_links(self):
        html = (
            """
            <span>T1<span> <a href="www.example.com">link</a> <span>T2</span>
            <br />
            <span>T3</span>
            """
        )
        expected = (
            "T1 link[1] T2\nT3\n\n[1]: www.example.com\n"
        )
        parser = converter.HTML2PlainParser()
        result = parser.html_to_plain_text(html)
        self.assertEqual(result, expected, msg=(
            'Should replace links nicely'))

    def test_replace_br(self):
        html = (
            """
            <span>Text1</span>
            <br />
            <br />
            <span>Text2</span>
            """
        )
        expected = (
            "Text1\n\nText2"
        )

        parser = converter.HTML2PlainParser()
        result = parser.html_to_plain_text(html)
        self.assertEqual(result, expected, msg=(
            'Should replace links nicely'))

    def test_stroke_before_elements(self):
        html = (
            """
            <table>
                <tr>
                    <td>Headline1</td>
                    <td>Headline2</td>
                </tr>
                <tr>
                    <td>Value 1</td>
                    <td>Value 2</td>
                </tr>
            </table>
            """
        )

        expected = (
            """
            ------------------------------
            Headline1
            Headline2
            ------------------------------
            Value 1
            Value 2
            ------------------------------
            """
        )
        expected = textwrap.dedent(expected).strip()
        parser = converter.HTML2PlainParser()
        result = parser.html_to_plain_text(html)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
