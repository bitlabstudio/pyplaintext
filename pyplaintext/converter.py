"""Main module of pyplaintext. Contains the converter class."""
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup


class HTML2PlainParser(HTMLParser):
    """Custom html parser to convert html code to plain text."""
    def __init__(self, ignored_elements=None, newline_before_elements=None,
                 newline_after_elements=None, stroke_before_elements=None,
                 stroke_after_elements=None, stroke_text=None):
        self.reset()
        self.text = ''  # Used to push the results into a variable
        self.links = []  # List of aggregated links

        # Settings
        if ignored_elements is None:
            self.ignored_elements = [
                'html', 'head', 'style', 'meta', 'title', 'img']
        else:
            self.ignored_elements = ignored_elements

        if newline_before_elements is None:
            self.newline_before_elements = [
                'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'li']
        else:
            self.newline_before_elements = newline_before_elements

        if newline_after_elements is None:
            self.newline_after_elements = [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'td']
        else:
            self.newline_after_elements = newline_after_elements

        if stroke_before_elements is None:
            self.stroke_before_elements = ['tr']
        else:
            self.stroke_before_elements = stroke_before_elements

        if stroke_after_elements is None:
            self.stroke_after_elements = ['tr']
        else:
            self.stroke_after_elements = stroke_after_elements

        if stroke_text is None:
            self.stroke_text = '------------------------------\n'
        else:
            self.stroke_text = stroke_text

    def handle_starttag(self, tag, attrs):
        """Handles every start tag like e.g. <p>."""
        if (tag in self.newline_before_elements):
            self.text += '\n'
        if (tag in self.stroke_before_elements
                and not self.text.endswith(self.stroke_text)):
            # Put a stroke in front of every relevant element, if there is some
            # content between it and its predecessor
            self.text += self.stroke_text
        if tag == 'a':
            # If it's a link, append it to the link list
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append((len(self.links) + 1, attr[1]))

    def handle_data(self, data):
        """Handles data between tags."""
        # Only proceed with unignored elements
        if self.lasttag not in self.ignored_elements:
            # Remove any predefined linebreaks
            text = data.replace('\n', '')
            # If there's some text left, proceed!
            if text:
                if self.lasttag == 'li':
                    # Use a special prefix for list elements
                    self.text += '  * '
                self.text += text
                if self.lasttag in self.newline_after_elements:
                    # Add a linebreak at the end of the content
                    self.text += '\n'

    def handle_endtag(self, tag):
        """Handles every end tag like e.g. </p>."""
        if tag in self.stroke_after_elements:
            if self.text.endswith(self.stroke_text):
                # Only add a stroke if there isn't already a stroke posted
                # In this case, there was no content between the tags, so
                # remove the starting stroke
                self.text = self.text[:-len(self.stroke_text)]
            else:
                # If there's no linebreak before the stroke, add one!
                if not self.text.endswith('\n'):
                    self.text += '\n'
                self.text += self.stroke_text
        if tag == 'a':
            # If it's a link, add a footnote
            self.text += '[{}]'.format(len(self.links))
        elif tag == 'br' and self.text and not self.text.endswith('\n'):
            # If it's a break, check if there's no break at the end of the
            # content. If there's none, add one!
            self.text += '\n'
        # Reset the lasttag, otherwise this parse can geht confused, if the
        # next element is not wrapped in a new tag.
        if tag == self.lasttag:
            self.lasttag = None

    def html_to_plain_text(self, html):
        """Converts html code into formatted plain text."""
        # Use BeautifulSoup to normalize the html
        soup = BeautifulSoup(html)
        # Init the parser
        self.feed(str(soup))
        # Strip the end of the plain text
        result = self.text.rstrip()
        # Add footnotes
        if self.links:
            result += '\n\n'
            for link in self.links:
                result += '[{}]: {}\n'.format(link[0], link[1])
        return result
