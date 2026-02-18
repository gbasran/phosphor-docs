"""Extended Markdown parser for phosphor-docs.

Handles standard Markdown plus custom ::: fenced blocks for components:
callouts, cards, decision grids, command blocks, accordions, pipelines, hero.
Also handles ```terminal blocks and {.class} attribute syntax.
"""

import re
import sys
import html as html_mod


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


# Per-page tracker for heading IDs — ensures uniqueness when headings share text
_used_ids = {}


def _unique_id(base_id):
    """Return a unique ID, appending -2, -3, etc. for duplicates."""
    if base_id not in _used_ids:
        _used_ids[base_id] = 1
        return base_id
    _used_ids[base_id] += 1
    return f"{base_id}-{_used_ids[base_id]}"


def _escape(text):
    """HTML-escape text."""
    return html_mod.escape(text)


def _escape_url(url):
    """Escape a URL for use in HTML attributes; reject javascript: URIs."""
    url = url.strip()
    if re.match(r"^\s*javascript\s*:", url, re.IGNORECASE):
        return "#"
    return html_mod.escape(url, quote=True)


# ── Inline Markdown ──

def _inline(text):
    """Process inline Markdown: bold, italic, code, links, images.

    Code spans are extracted first and replaced with placeholders so their
    content is HTML-escaped and protected from further inline processing.
    """
    # Step 1: Extract inline code spans (double-backtick first, then single)
    code_spans = []

    def _save_code(m):
        idx = len(code_spans)
        code_spans.append(f"<code>{_escape(m.group(1).strip())}</code>")
        return f"\x00CODE{idx}\x00"

    # Double-backtick inline code: `` content `` (may contain single backticks)
    text = re.sub(r"``(.+?)``", _save_code, text)
    # Single-backtick inline code: `content`
    text = re.sub(r"`([^`]+)`", _save_code, text)

    # Step 2: Process other inline elements on the remaining text
    # Images: ![alt](src)
    def _img_replace(m):
        alt, src = _escape(m.group(1)), _escape_url(m.group(2))
        return f'<img src="{src}" alt="{alt}">'
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _img_replace, text)

    # Links with class: [text](url){.class}
    def _link_class(m):
        label, url, cls = m.group(1), _escape_url(m.group(2)), m.group(3)
        return f'<a href="{url}" class="hero-btn {cls}">{label}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)\{\.(\w+)\}', _link_class, text)

    # Regular links: [text](url)
    def _link_replace(m):
        label, url = m.group(1), _escape_url(m.group(2))
        return f'<a href="{url}">{label}</a>'
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_replace, text)

    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    # Step 3: Restore code spans
    for i, code_html in enumerate(code_spans):
        text = text.replace(f"\x00CODE{i}\x00", code_html)

    return text


# ── Terminal Block ──

def _parse_terminal(lines):
    """Parse terminal code block lines into HTML."""
    body_html = ""
    for line in lines:
        if line.startswith("$ "):
            cmd = _escape(line[2:])
            body_html += f'<div><span class="prompt">$ </span><span class="cmd">{cmd}</span></div>\n'
        elif line.startswith("# "):
            body_html += f'<div><span class="comment">{_escape(line)}</span></div>\n'
        else:
            body_html += f'<div><span class="output">{_escape(line)}</span></div>\n'

    return (
        '<div class="terminal">\n'
        '  <div class="terminal-bar">\n'
        '    <span class="terminal-dot red"></span>\n'
        '    <span class="terminal-dot yellow"></span>\n'
        '    <span class="terminal-dot green"></span>\n'
        '    <span class="terminal-title">terminal</span>\n'
        '  </div>\n'
        f'  <div class="terminal-body">\n{body_html}  </div>\n'
        '</div>\n'
    )


# ── Component Parsers ──

def _parse_attrs(attr_str):
    """Parse {key="value" key2="value2"} into dict."""
    attrs = {}
    if not attr_str:
        return attrs
    for m in re.finditer(r'([\w-]+)="([^"]*)"', attr_str):
        attrs[m.group(1)] = m.group(2)
    return attrs


def _parse_hero(content, attrs):
    """Parse hero block content into HTML."""
    badge = attrs.get("badge", "")
    lines = content.strip().split("\n")
    title_html = ""
    desc_html = ""
    buttons_html = ""

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            title_text = line[2:]
            # Convert **text** to <span class="accent">text</span>
            title_text = re.sub(r"\*\*(.+?)\*\*", r'<span class="accent">\1</span>', title_text)
            title_html = title_text
        elif line.startswith("["):
            # Button link: [Label](url){.class}
            m = re.match(r'\[([^\]]+)\]\(([^)]+)\)\{\.(\w+)\}', line)
            if m:
                label, url, cls = m.group(1), _escape_url(m.group(2)), m.group(3)
                buttons_html += f'          <a href="{url}" class="hero-btn {cls}">{label}</a>\n'
        elif line:
            desc_html += f"<p>{_inline(line)}</p>\n"

    badge_html = f'<div class="hero-badge">&#9679; {_escape(badge)}</div>\n' if badge else ""

    return (
        f'<div class="hero" id="top">\n'
        f'        {badge_html}'
        f'        <h1>{title_html}</h1>\n'
        f'        {desc_html}'
        f'        <div class="hero-actions">\n{buttons_html}        </div>\n'
        f'      </div>\n'
    )


def _parse_callout(content, attrs, callout_type):
    """Parse callout block (tip/info/warn) into HTML."""
    lines = content.strip().split("\n")
    title = lines[0].strip() if lines else callout_type.title()
    body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
    body_html = _process_block_content(body) if body else ""

    return (
        f'<div class="callout {callout_type}">\n'
        f'  <div class="callout-title">{_escape(title)}</div>\n'
        f'  <div class="callout-body">{body_html}</div>\n'
        f'</div>\n'
    )


def _parse_cards(content):
    """Parse cards container with ::card children."""
    cards = re.findall(
        r'::card\{([^}]*)\}\s*\n(.*?)(?=::card|\Z)',
        content, re.DOTALL
    )
    cards_html = ""
    for attr_str, body in cards:
        attrs = _parse_attrs(attr_str)
        icon = attrs.get("icon", "star")
        color = attrs.get("color", "teal")
        title = attrs.get("title", "")
        body_text = body.strip().rstrip(":").strip()

        cards_html += (
            f'<div class="card">\n'
            f'  <div class="card-header">\n'
            f'    <div class="card-icon {color}"><i data-lucide="{icon}"></i></div>\n'
            f'    <div class="card-title">{_escape(title)}</div>\n'
            f'  </div>\n'
            f'  <p>{_inline(body_text)}</p>\n'
            f'</div>\n'
        )

    return f'<div class="card-grid">\n{cards_html}</div>\n'


def _parse_decision_grid(content):
    """Parse decision grid (markdown table) into HTML."""
    lines = [ln.strip() for ln in content.strip().split("\n") if ln.strip()]
    if len(lines) < 2:
        return f"<p>{_inline(content)}</p>"

    # Parse header
    header_cells = [c.strip() for c in lines[0].strip("|").split("|")]

    # Skip separator line
    data_lines = [ln for ln in lines[1:] if not re.match(r"^\|?\s*[-:]+", ln)]

    header_html = "".join(f'<div class="dg-header">{_escape(c)}</div>' for c in header_cells)

    rows_html = ""
    for line in data_lines:
        cells = [c.strip() for c in line.strip("|").split("|")]
        cells_html = "".join(f'<div class="dg-cell">{_inline(c)}</div>' for c in cells)
        rows_html += f'<div class="dg-row">{cells_html}</div>\n'

    cols = len(header_cells)
    return (
        f'<div class="decision-grid" style="grid-template-columns: {"1fr " * (cols - 1)}auto;">\n'
        f'{header_html}\n{rows_html}</div>\n'
    )


def _parse_command(content, attrs):
    """Parse command block with ::flag children."""
    title = attrs.get("title", "command")
    usage = attrs.get("usage", title)

    flags = re.findall(
        r'::flag\{([^}]*)\}\s*\n(.*?)(?=::flag|\Z)',
        content, re.DOTALL
    )

    flags_html = ""
    for attr_str, body in flags:
        flag_attrs = _parse_attrs(attr_str)
        name = flag_attrs.get("name", "")
        short = flag_attrs.get("short", "")
        desc = body.strip().rstrip(":").strip()
        flag_label = f"<code>{_escape(name)}</code>"
        if short:
            flag_label += f", <code>{_escape(short)}</code>"
        flags_html += (
            f'<tr>\n'
            f'  <td>{flag_label}</td>\n'
            f'  <td>{_inline(desc)}</td>\n'
            f'</tr>\n'
        )

    table_html = ""
    if flags_html:
        table_html = (
            '<table class="cmd-arg-table">\n'
            '<thead><tr><th>Flag</th><th>Description</th></tr></thead>\n'
            f'<tbody>\n{flags_html}</tbody>\n</table>\n'
        )

    return (
        f'<div class="cmd-block">\n'
        f'  <div class="cmd-block-header">\n'
        f'    <span class="cmd-block-name">{_escape(title)}</span>\n'
        f'  </div>\n'
        f'  <div class="cmd-block-body">\n'
        f'    <div class="cmd-block-usage">{_escape(usage)}</div>\n'
        f'    {table_html}'
        f'  </div>\n'
        f'</div>\n'
    )


def _parse_accordion(content, attrs):
    """Parse accordion block into details/summary HTML."""
    title = attrs.get("title", "Details")
    body_html = _process_block_content(content.strip())

    return (
        f'<details class="trouble-item">\n'
        f'  <summary class="trouble-summary">{_escape(title)}</summary>\n'
        f'  <div class="trouble-body">\n{body_html}\n  </div>\n'
        f'</details>\n'
    )


def _parse_pipeline(content):
    """Parse pipeline block: Stage1 -> Stage2 -> Stage3."""
    text = content.strip()
    stages = [s.strip() for s in re.split(r"\s*->\s*", text) if s.strip()]

    html = '<div class="pipeline-flow">\n'
    for i, stage in enumerate(stages):
        if i > 0:
            html += (
                '<div class="pipeline-arrow">'
                '<i data-lucide="arrow-right"></i>'
                '</div>\n'
            )
        num = f"0{i + 1}" if i < 9 else str(i + 1)
        html += (
            f'<div class="pipeline-stage">\n'
            f'  <div class="pipeline-node">\n'
            f'    <span class="stage-num">{num}</span>\n'
            f'    {_escape(stage)}\n'
            f'  </div>\n'
            f'</div>\n'
        )
    html += '</div>\n'
    return html


# ── Block-level Processing ──

def _process_block_content(text):
    """Process a chunk of text that may contain paragraphs, lists, code blocks, etc."""
    lines = text.split("\n")
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Code block (``` fenced) — supports variable fence lengths (```, ````, etc.)
        fence_match = re.match(r"^(`{3,})(\w*)", line.strip())
        if fence_match:
            fence = fence_match.group(1)  # e.g., ``` or ````
            lang = fence_match.group(2)
            code_lines = []
            i += 1
            while i < len(lines):
                stripped = lines[i].strip()
                # Closing fence must be exactly the same length (or longer)
                if stripped == fence or (stripped.startswith(fence) and not stripped[len(fence):].strip()):
                    break
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence

            if lang == "terminal":
                result.append(_parse_terminal(code_lines))
            else:
                code_content = _escape("\n".join(code_lines))
                result.append(f'<pre><code>{code_content}</code></pre>\n')
            continue

        # Heading h2
        if line.startswith("## "):
            heading_text = line[3:].strip()
            hid = _unique_id(slugify(heading_text))
            result.append(
                f'<div class="section" id="{hid}">\n'
                f'  <span class="section-anchor"></span>\n'
                f'  <h2>{_inline(heading_text)}</h2>\n'
                f'  <hr class="section-rule">\n'
            )
            # Collect section content until next h2, respecting code fences
            i += 1
            section_lines = []
            in_fence = False
            fence_str = ""
            while i < len(lines):
                cur = lines[i]
                stripped = cur.strip()
                # Track code fence state
                if not in_fence:
                    fm = re.match(r"^(`{3,})", stripped)
                    if fm:
                        in_fence = True
                        fence_str = fm.group(1)
                else:
                    if stripped == fence_str or (stripped.startswith(fence_str) and not stripped[len(fence_str):].strip()):
                        in_fence = False
                # Only break on h2 if not inside a code fence
                if not in_fence and cur.startswith("## "):
                    break
                section_lines.append(cur)
                i += 1
            section_content = _process_block_content("\n".join(section_lines))
            result.append(section_content)
            result.append("</div>\n")
            continue

        # Heading h3
        if line.startswith("### "):
            heading_text = line[4:].strip()
            hid = _unique_id(slugify(heading_text))
            result.append(f'<h3 id="{hid}">{_inline(heading_text)}</h3>\n')
            i += 1
            continue

        # Heading h4
        if line.startswith("#### "):
            heading_text = line[5:].strip()
            result.append(f'<h4>{_inline(heading_text)}</h4>\n')
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^---+\s*$", line):
            result.append("<hr>\n")
            i += 1
            continue

        # Unordered list
        if re.match(r"^[\-\*]\s", line.strip()):
            list_items = []
            while i < len(lines) and re.match(r"^[\-\*]\s", lines[i].strip()):
                item_text = re.sub(r"^[\-\*]\s+", "", lines[i].strip())
                list_items.append(f"  <li>{_inline(item_text)}</li>")
                i += 1
            result.append("<ul>\n" + "\n".join(list_items) + "\n</ul>\n")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s", line.strip()):
            list_items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                item_text = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                list_items.append(f"  <li>{_inline(item_text)}</li>")
                i += 1
            result.append("<ol>\n" + "\n".join(list_items) + "\n</ol>\n")
            continue

        # Table (markdown)
        if "|" in line and i + 1 < len(lines) and re.match(r"^\|?\s*[-:|]+", lines[i + 1]):
            table_lines = []
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1
            result.append(_parse_markdown_table(table_lines))
            continue

        # HTML block — pass through lines starting with block-level HTML tags
        # (opening or closing, or self-closing elements)
        stripped = line.strip()
        _html_block_re = r"^</?(?:div|details|summary|table|thead|tbody|tr|th|td|section|nav|aside|header|footer|article|button|pre|ul|ol|hr|h[1-6]|a\s+class=\"hero)\b"
        if re.match(_html_block_re, stripped):
            # Collect consecutive HTML lines
            block_lines = [line]
            i += 1
            while i < len(lines):
                cur = lines[i].strip()
                if not cur:
                    i += 1
                    break
                # Continue if it looks like HTML or content within HTML
                if re.match(_html_block_re, cur) or cur.startswith("</") or cur.startswith("<") or (block_lines and not cur.startswith("#") and not cur.startswith("```") and not re.match(r"^:::", cur)):
                    block_lines.append(lines[i])
                    i += 1
                else:
                    break
            result.append("\n".join(block_lines) + "\n")
            continue

        # Default: paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].startswith("```") and not re.match(r"^<(?:div|details|table|section)\b", lines[i].strip()) and not re.match(r"^[\-\*]\s", lines[i].strip()) and not re.match(r"^\d+\.\s", lines[i].strip()) and not re.match(r"^---+\s*$", lines[i]):
            para_lines.append(lines[i])
            i += 1
        if para_lines:
            result.append(f"<p>{_inline(' '.join(para_lines))}</p>\n")

    return "".join(result)


def _parse_markdown_table(lines):
    """Parse a standard markdown table into HTML."""
    if len(lines) < 2:
        return ""

    header_cells = [c.strip() for c in lines[0].strip("|").split("|")]
    # Skip separator (line 1)
    data_lines = lines[2:] if len(lines) > 2 else []

    col_count = len(header_cells)
    thead = "<thead><tr>" + "".join(f"<th>{_escape(c)}</th>" for c in header_cells) + "</tr></thead>\n"
    tbody_rows = ""
    for line in data_lines:
        if not line.strip():
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # Pad short rows with empty cells to match header count
        while len(cells) < col_count:
            cells.append("")
        tbody_rows += "<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>\n"

    return (
        '<div class="table-wrap">\n'
        f'<table>\n{thead}<tbody>\n{tbody_rows}</tbody>\n</table>\n'
        '</div>\n'
    )


# ── Main Parser ──

def parse_markdown(text):
    """Parse extended Markdown into HTML.

    Returns (html_content, headings) where headings is a list of
    {"level": 2|3, "text": str, "id": str} for TOC generation.
    """
    # Reset the per-page ID counter so duplicate headings get unique suffixes
    _used_ids.clear()

    # First pass: extract and process ::: fenced blocks
    text = _process_fenced_blocks(text)

    # Second pass: process remaining standard markdown
    html = _process_block_content(text)

    # Extract headings for TOC
    headings = []
    for m in re.finditer(r'<(?:div class="section" id|h3 id)="([^"]+)"[^>]*>\s*(?:<[^>]+>\s*){0,5}(?:<h[23][^>]*>)?(.*?)</h[23]>', html):
        tag_id = m.group(1)
        # Determine level from context
        if 'class="section"' in m.group(0):
            level = 2
        else:
            level = 3
        text_content = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        headings.append({"level": level, "text": text_content, "id": tag_id})

    # Also find h2 headings inside sections
    for m in re.finditer(r'<div class="section" id="([^"]+)"[^>]*>.*?<h2>(.*?)</h2>', html, re.DOTALL):
        tag_id = m.group(1)
        text_content = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        # Check if already captured
        if not any(h["id"] == tag_id for h in headings):
            headings.append({"level": 2, "text": text_content, "id": tag_id})

    # Find h3 headings
    for m in re.finditer(r'<h3 id="([^"]+)">(.*?)</h3>', html):
        tag_id = m.group(1)
        text_content = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if not any(h["id"] == tag_id for h in headings):
            headings.append({"level": 3, "text": text_content, "id": tag_id})

    return html, headings


def _process_fenced_blocks(text):
    """Process ::: fenced blocks and replace them with HTML.

    Tracks code fence state so that ```::: ``` inside a code fence is not
    treated as a component delimiter.  Warns on unclosed ::: blocks.
    """
    result = []
    lines = text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip over code fences — pass lines through until fence closes
        fence_match = re.match(r"^(`{3,})", stripped)
        if fence_match:
            fence_str = fence_match.group(1)
            result.append(line)
            i += 1
            while i < len(lines):
                s = lines[i].strip()
                result.append(lines[i])
                i += 1
                if s == fence_str or (s.startswith(fence_str) and not s[len(fence_str):].strip()):
                    break
            continue

        # Check for ::: block start (supports hyphenated types like decision-grid)
        m = re.match(r"^:::([a-z][a-z0-9-]*)\s*(\{[^}]*\})?\s*(.*)$", stripped)
        if m:
            block_type = m.group(1)
            attr_str = m.group(2) or ""
            inline_title = m.group(3).strip()
            attrs = _parse_attrs(attr_str)
            start_line = i + 1

            # Collect block content until closing :::, respecting code fences
            i += 1
            block_lines = []
            depth = 1
            in_fence = False
            code_fence_str = ""
            while i < len(lines):
                s = lines[i].strip()

                # Track code fence state inside ::: blocks
                if not in_fence:
                    fm = re.match(r"^(`{3,})", s)
                    if fm:
                        in_fence = True
                        code_fence_str = fm.group(1)
                else:
                    if s == code_fence_str or (s.startswith(code_fence_str) and not s[len(code_fence_str):].strip()):
                        in_fence = False

                # Only match ::: delimiters outside code fences
                if not in_fence:
                    if s == ":::":
                        depth -= 1
                        if depth == 0:
                            break
                    elif re.match(r"^:::[a-z][a-z0-9-]*", s):
                        depth += 1

                block_lines.append(lines[i])
                i += 1

            if depth != 0:
                # Unclosed block — warn and treat collected content as the block
                print(
                    f"  Warning: Unclosed :::{block_type} block (started near line {start_line}); "
                    f"treating rest of file as block content",
                    file=sys.stderr,
                )
            else:
                i += 1  # skip closing :::

            block_content = "\n".join(block_lines)

            # Dispatch to component parser
            if block_type in ("tip", "info", "warn"):
                # If title was on the ::: line, prepend it to content
                if inline_title:
                    block_content = inline_title + "\n" + block_content
                result.append(_parse_callout(block_content, attrs, block_type))
            elif block_type == "cards":
                result.append(_parse_cards(block_content))
            elif block_type == "decision-grid":
                result.append(_parse_decision_grid(block_content))
            elif block_type == "command":
                result.append(_parse_command(block_content, attrs))
            elif block_type == "accordion":
                result.append(_parse_accordion(block_content, attrs))
            elif block_type == "pipeline":
                result.append(_parse_pipeline(block_content))
            elif block_type == "hero":
                result.append(_parse_hero(block_content, attrs))
            else:
                # Unknown component type — pass through as-is
                result.append(line)
                result.extend(block_lines)
        else:
            result.append(line)
            i += 1

    return "\n".join(result)
