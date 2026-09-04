from html.parser import HTMLParser
from urllib.parse import urljoin


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self._title = False
        self.description = ""
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "title":
            self._title = True
        elif tag == "meta" and data.get("name", "").lower() == "description":
            self.description = data.get("content", "")
        elif tag == "a" and data.get("href"):
            self.links.append(data["href"])
        elif tag == "img" and data.get("src"):
            self.images.append(data["src"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False

    def handle_data(self, data):
        if self._title:
            self.title += data


def extract_metadata(html: str) -> dict:
    parser = _Parser()
    parser.feed(html)
    return {"title": parser.title.strip(), "description": parser.description.strip()}


def extract_links(html: str, base_url: str | None = None) -> list[str]:
    parser = _Parser()
    parser.feed(html)
    if base_url:
        return [urljoin(base_url, value) for value in parser.links]
    return parser.links
