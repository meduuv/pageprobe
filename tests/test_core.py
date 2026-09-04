from pageprobe import extract_links, extract_metadata


def test_metadata():
    html = '<title>Example</title><meta name="description" content="Demo">'
    assert extract_metadata(html) == {"title": "Example", "description": "Demo"}


def test_links_resolve():
    html = '<a href="/docs">Docs</a><a href="https://example.com/x">X</a>'
    assert extract_links(html, "https://example.com/base") == [
        "https://example.com/docs",
        "https://example.com/x",
    ]
