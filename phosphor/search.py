"""Search index generator for phosphor-docs.

Walks all pages, extracts headings and content per section,
generates a SEARCH_INDEX array for the search.js template.
"""

import json
import re


def _strip_html(html_text):
    """Strip HTML tags and return plain text."""
    text = re.sub(r"<[^>]+>", " ", html_text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_keywords(text, max_words=100):
    """Extract first N words from text as keywords."""
    words = text.split()[:max_words]
    return " ".join(words).lower()


def build_search_index(pages_data):
    """Build search index from parsed pages.

    pages_data: list of {
        "filename": "index.html",
        "headings": [{"level": 2|3, "text": str, "id": str}],
        "html": str  (full page HTML content)
    }

    Returns JSON string for the SEARCH_INDEX variable.
    """
    index = []

    for page in pages_data:
        filename = page["filename"]
        headings = page["headings"]
        html = page["html"]

        # Split content by section
        sections = re.split(r'<div class="section" id="([^"]+)"', html)

        # First chunk is pre-section content (hero, etc.)
        current_section = "Overview"

        for heading in headings:
            if heading["level"] == 2:
                current_section = heading["text"]

            # Extract a chunk of text around this heading
            hid = heading["id"]
            # Find content after this heading ID
            pattern = rf'id="{re.escape(hid)}"[^>]*>.*?</(?:h[23]|div)>'
            match = re.search(pattern, html, re.DOTALL)
            if match:
                start = match.end()
                # Get next ~500 chars of content
                chunk = html[start:start + 2000]
                # Stop at next section
                next_section = re.search(r'<div class="section"', chunk)
                if next_section:
                    chunk = chunk[:next_section.start()]
                plain = _strip_html(chunk)
                keywords = _extract_keywords(plain)
            else:
                keywords = heading["text"].lower()

            section_label = current_section if heading["level"] == 3 else "Navigation"
            if heading["level"] == 2:
                section_label = _find_nav_group(heading["id"], headings)

            index.append({
                "title": heading["text"],
                "section": section_label,
                "url": f"{filename}#{hid}",
                "keywords": keywords,
            })

    return json.dumps(index, indent=2)


def _find_nav_group(section_id, headings):
    """Find the nav group label for a section (just returns section name)."""
    for h in headings:
        if h["id"] == section_id and h["level"] == 2:
            return h["text"]
    return "Documentation"


def inject_search_index(search_js_template, index_json):
    """Replace {{SEARCH_INDEX}} placeholder in search.js with actual index."""
    return search_js_template.replace("{{SEARCH_INDEX}}", index_json)
