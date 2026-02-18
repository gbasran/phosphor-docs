## How Phosphor Works

This page documents the internal architecture of Phosphor for maintainers and contributors. If you need to fix a bug, add a component, or modify the build pipeline, start here.

### Data Flow

Every `phosphor build` follows this exact sequence:

:::pipeline
Config -> Parse -> Search -> Render -> Output
:::

1. **`build.py`** orchestrates everything. It calls the other modules in order.
2. **`config.py`** loads `docs.yaml` and merges with defaults.
3. **`parser.py`** converts each `.md` file into HTML + a heading list.
4. **`search.py`** takes all parsed pages and generates a JSON search index.
5. **`renderer.py`** substitutes variables into `templates/base.html` for each page.
6. **`build.py`** writes the final files to `_site/`.

### Module Map

:::cards
::card{icon="file-code" color="teal" title="build.py (60 lines)"}
Orchestrator. Loads config, iterates over pages, calls parser/renderer/search, copies assets, writes output. The only module that does file I/O for the build.
::

::card{icon="settings" color="amber" title="config.py (~60 lines)"}
Loads docs.yaml with PyYAML, merges with DEFAULTS dict. Validates types: `pages` and `nav` must be lists, `site` and `theme` must be mappings. Exits with clear error on invalid types.
::

::card{icon="code" color="blue" title="parser.py (~650 lines)"}
The largest module. Two-pass Markdown-to-HTML converter. Pass 1: fenced component blocks (with code fence tracking). Pass 2: standard Markdown. Includes XSS protection for URLs and `javascript:` URI rejection. No external Markdown library.
::

::card{icon="layout-grid" color="purple" title="renderer.py (98 lines)"}
Simple string substitution. Replaces {{VAR}} placeholders in base.html. Also builds sidebar nav HTML and TOC HTML from config/headings.
::

::card{icon="search" color="red" title="search.py (95 lines)"}
Walks parsed pages, extracts headings + surrounding text, generates JSON array. Injects into search.js template by replacing {{SEARCH_INDEX}}.
::

::card{icon="terminal" color="teal" title="cli.py (~170 lines)"}
Argument parsing with argparse. Three commands: build, init, serve. Also contains _detect_git_info() for auto-populating config.
::
:::

## The Parser In Depth

The parser (`phosphor/parser.py`) is the core of Phosphor and the most complex module. Understanding it is essential for debugging rendering issues or adding new components.

### Two-Pass Architecture

The `parse_markdown(text)` function runs two passes:

**Pass 1 — `_process_fenced_blocks(text)`**

Scans the raw Markdown line by line looking for `:::type` opening patterns. When found, it collects all lines until the matching `:::` closer (tracking nesting depth), then dispatches to the appropriate component parser. The component HTML replaces the `:::` block in the text.

This pass runs first so that component HTML doesn't get re-processed as Markdown in pass 2.

**Pass 2 — `_process_block_content(text)`**

Processes the remaining text (with component HTML already substituted) for standard Markdown:

1. Code blocks (``` fenced, with variable fence lengths for ```` support)
2. Headings (##, ###, ####)
3. Horizontal rules (---)
4. Unordered lists (- item)
5. Ordered lists (1. item)
6. Tables (| col | col |)
7. HTML blocks (passed through untouched)
8. Paragraphs (default fallback)

### How Sections Work

When the parser encounters a `## Heading`, it wraps everything until the next `## Heading` in a `<div class="section" id="slug">` container. This is important because:

- The section ID is used by sidebar navigation anchors
- The scroll spy JavaScript tracks these section divs
- The search indexer splits content by section boundaries

The h2 heading gets an auto-generated slug ID via `slugify()`. The h3 headings also get IDs for the table of contents.

### How Fenced Blocks Match

The regex for `:::` block detection:

```
^:::([a-z][a-z0-9-]*)\s*(\{[^}]*\})?\s*(.*)$
```

- Group 1: block type — supports hyphenated names like `decision-grid` (required)
- Group 2: attribute string like `{title="..." usage="..."}` (optional)
- Group 3: inline text after the type (used for callout titles like `:::tip My Title`)

Nesting is tracked with a depth counter. Each `:::type` increments depth, each `:::` (bare) decrements. When depth hits 0, the block is closed.

**Code fence awareness**: The fenced block scanner tracks code fence state. A `:::` delimiter inside a code fence (`` ``` ``) is ignored — it does not open or close a component block. This prevents content corruption when showing `:::` syntax examples inside code blocks.

**Unclosed blocks**: If a `:::type` block never finds its closing `:::`, the parser emits a warning to stderr and treats the remaining content as the block body rather than silently consuming it.

### How Code Fences Work

The parser supports variable-length code fences. A ```` (4-backtick) opening fence is only closed by another ```` fence. This lets you embed ``` inside ```` blocks for showing code examples that contain code blocks.

The fence detection regex: `` ^(`{3,})(\w*) `` — captures the backtick string length and optional language identifier.

### Component Parsers

Each component type has its own parser function:

| Component | Function | Accepts Attrs | Has Children |
| --- | --- | --- | --- |
| Callout (tip/info/warn) | `_parse_callout()` | No (title from inline text) | No |
| Hero | `_parse_hero()` | `badge` | No (structured content) |
| Cards | `_parse_cards()` | No | `::card` children |
| Decision Grid | `_parse_decision_grid()` | No | Markdown table content |
| Command | `_parse_command()` | `title`, `usage` | `::flag` children |
| Accordion | `_parse_accordion()` | `title` | Markdown body |
| Pipeline | `_parse_pipeline()` | No | `->` separated stages |

### Child Element Parsing

Cards and commands use `::child{attrs}` syntax (double colon, no triple). These are parsed with regex inside the parent parser:

```
::card\{([^}]*)\}\s*\n(.*?)(?=::card|\Z)
::flag\{([^}]*)\}\s*\n(.*?)(?=::flag|\Z)
```

Each child's attribute string is parsed by `_parse_attrs()` which extracts `key="value"` pairs. Attribute names support hyphens (e.g., `data-x="value"`) in addition to standard alphanumeric names.

### Inline Processing

The `_inline(text)` function handles inline Markdown within any line:

1. **Code spans extracted first** — replaced with placeholders to protect from further processing
2. Images: `![alt](src)` -> `<img>` (URL escaped, alt text escaped)
3. Links with classes: `[text](url){.class}` -> `<a class="hero-btn class">`
4. Regular links: `[text](url)` -> `<a>`
5. Bold: `**text**` -> `<strong>`
6. Italic: `*text*` -> `<em>`
7. **Code spans restored** from placeholders

Order matters — images are processed before links to prevent `![` being matched as a regular link.

**URL security**: All URLs in links, images, and hero buttons are processed through `_escape_url()`, which HTML-escapes special characters (quotes, ampersands) and rejects `javascript:` URIs by replacing them with `#`.

### HTML Block Pass-Through

After pass 1, the text contains embedded HTML from component parsers. Pass 2 must not wrap these in `<p>` tags. The HTML block detection regex matches lines starting with known block-level HTML tags (both opening and closing):

```
^</?(?:div|details|summary|table|thead|tbody|tr|th|td|section|...)
```

When detected, all consecutive HTML lines are collected and passed through as-is.

### Heading Extraction

After both passes, `parse_markdown()` extracts headings from the generated HTML for the table of contents and search index. It looks for:

- `<div class="section" id="...">` followed by `<h2>` for h2 headings
- `<h3 id="...">` for h3 headings

Returns a list of `{"level": 2|3, "text": str, "id": str}` dicts.

## The Build Pipeline In Depth

### build.py Walk-Through

The `build(project_dir)` function:

1. **Resolves paths**: Finds the phosphor root (for templates/theme), the project directory, and the output directory (`_site/`).

2. **Loads config**: Calls `config.load_config()` which reads `docs.yaml` and merges with defaults. The defaults are defined in `config.DEFAULTS`.

3. **Loads templates**: Reads `templates/base.html` and `theme/search.js` into memory.

4. **Cleans output**: Deletes `_site/` entirely and recreates it. Every build is a clean build.

5. **Copies assets**: Copies `style.css`, `script.js`, and `favicon.svg` from `theme/` to `_site/assets/`. If a custom favicon is specified in config, it's copied only if the path resolves within the project directory (path traversal protection). Auto-generated favicons validate that theme colors match safe patterns (`#hex` or `rgba()`) before injecting them into SVG.

6. **Validates and parses pages**: Checks that `pages/` directory exists. For each `.md` file in the `pages` config array, verifies the resolved path stays within `pages/` (path traversal protection), then reads the file and calls `parser.parse_markdown()`.

7. **Generates search**: Calls `search.build_search_index()` with all parsed page data. Injects the JSON index into the search.js template and writes it to `_site/assets/search.js`.

8. **Renders pages**: For each parsed page, calls `renderer.render_page()` which substitutes template variables and writes the HTML to `_site/`.

### Config Validation and Defaults

The config loader validates types before merging with defaults. `pages` and `nav` must be lists (or null/absent for defaults). `site` and `theme` must be mappings. Invalid types produce a clear error message and exit.

When `docs.yaml` is missing a field, these defaults apply:

| Field | Default |
| --- | --- |
| `site.title` | `"Documentation"` |
| `site.tagline` | `""` |
| `site.logo_text` | `"PD"` |
| `site.github` | `""` |
| `site.favicon` | `""` |
| `nav` | `[]` |
| `pages` | `[]` |

### Template Variables

The `renderer.render_page()` function does simple string replacement on the base template:

| Variable | Source | Notes |
| --- | --- | --- |
| `{{TITLE}}` | `site.title` | HTML-escaped |
| `{{SITE_TITLE}}` | `site.title` | Used in sidebar header |
| `{{TAGLINE}}` | `site.tagline` | Below sidebar logo |
| `{{LOGO_TEXT}}` | `site.logo_text` | Inside the gradient icon |
| `{{FAVICON}}` | Computed | `assets/favicon.svg` unless custom |
| `{{NAV}}` | Generated | From `build_nav_html()` |
| `{{GITHUB_LINK}}` | Generated | From `site.github` or empty |
| `{{CONTENT}}` | Parsed HTML | Full page content |

### Search Index Structure

The search index is a JSON array where each entry represents a heading:

```
{
  "title": "Section Title",
  "section": "Parent Section Name",
  "url": "page.html#section-id",
  "keywords": "extracted text from content around this heading..."
}
```

The `keywords` field contains the first ~100 words of plain text extracted from the HTML content following that heading. HTML tags are stripped, entities decoded.

## The Theme

### CSS Architecture

`theme/style.css` is organized into sections:

1. **CSS Variables** (`:root`) — all colors, sizes, spacing
2. **Reset** — box-sizing, margin/padding reset
3. **Scrollbar** — custom scrollbar styling
4. **Sidebar** — fixed sidebar, logo, nav links, search box
5. **Main content** — content area, max-width, padding
6. **Hero** — hero section, badge, title, buttons
7. **Terminal** — terminal window chrome, colored output
8. **Typography** — headings, paragraphs, links, code
9. **Tables** — wrapped tables with header styling
10. **Cards** — grid layout, card borders, icon colors
11. **Pipeline** — flex layout, stage nodes, arrows
12. **Decision Grid** — CSS grid, header/cell styling
13. **Callouts** — bordered boxes with color variants
14. **Lists** — basic list styling
15. **Command Block** — header, usage line, arg table
16. **Accordion** — details/summary with chevron animation
17. **Back to Top** — fixed button with scroll visibility
18. **Footer** — centered footer with border
19. **Table of Contents** — sticky TOC on wide screens
20. **Responsive** — media queries at 900px and 480px

### JavaScript Files

**`script.js`** handles:

- Auto-generating IDs for h3 headings (slugification)
- Building the TOC innerHTML from h2/h3 headings
- Scroll spy for both sidebar nav and TOC
- Back-to-top button visibility
- Mobile sidebar close on nav click

**`search.js`** handles:

- Search algorithm: full-query matching, per-word matching, prefix matching
- Score-based ranking with title/keyword/section weights
- Result highlighting with `<mark>` tags
- Keyboard navigation (arrows, enter, escape)
- Global `/` shortcut to focus search
- Click-outside to close results

### Lucide Icons

Icons are loaded from the Lucide CDN (`unpkg.com/lucide@latest`). After the page loads, `lucide.createIcons()` scans for `<i data-lucide="icon-name">` elements and replaces them with inline SVGs. This means:

- Icons require internet connectivity on first load (CDN)
- Any Lucide icon name works in nav items and cards
- Icons are SVG so they scale and color perfectly

## Adding a New Component

To add a new component type (e.g., `:::timeline`):

### Step 1: Add the Parser

In `parser.py`, create a new function:

```
def _parse_timeline(content, attrs):
    """Parse timeline block into HTML."""
    # Parse content and generate HTML
    # Return an HTML string
    return '<div class="timeline">...</div>'
```

### Step 2: Register in Fenced Blocks

In `_process_fenced_blocks()`, add the type to the regex:

```
r"^:::(tip|info|warn|cards|...|timeline)\s*..."
```

And add the dispatch case:

```
elif block_type == "timeline":
    result.append(_parse_timeline(block_content, attrs))
```

### Step 3: Add CSS

In `theme/style.css`, add the styles for your new component:

```
/* Timeline */
.timeline { ... }
.timeline-item { ... }
```

### Step 4: Document It

Add a section to `pages/writing-content.md` showing the syntax and rendered example.

## Git Auto-Detection

### How It Works

When `phosphor init` is called, the CLI tries to detect the GitHub repository:

1. Runs `git remote get-url origin` in the target directory
2. If that fails, tries the parent directory (for `docs/` subdirectories inside repos)
3. Parses the URL with regex to extract owner and repo name
4. Supports both HTTPS and SSH URL formats:
   - `https://github.com/user/repo-name.git`
   - `git@github.com:user/repo-name.git`
5. Generates config values:
   - **title**: repo name with hyphens/underscores replaced by spaces, title-cased
   - **tagline**: `~/repo-name`
   - **logo_text**: first 2 characters of repo name (letters only), uppercase
   - **github**: full HTTPS GitHub URL

### Fallback

If no git remote is found (not a repo, or no remote configured), the example defaults are used instead. The auto-detection is best-effort and never fails the init process.

## Extending Phosphor

### Adding a New Template Variable

1. Define the variable in `renderer.py`'s `render_page()` function
2. Add the `{{VAR}}` placeholder to `templates/base.html`
3. Optionally add a config field in `config.py`'s `DEFAULTS`

### Adding a Config Field

1. Add the default value to `DEFAULTS` in `config.py`
2. The `load_config()` function merges user config with defaults, so new fields are automatically available
3. Use the field in `renderer.py` or `build.py` as needed

### Modifying the Build Process

All build logic is in `build.py`'s `build()` function. The steps are sequential and straightforward. To add a new step (e.g., image optimization, sitemap generation):

1. Add your logic as a new function in the appropriate module
2. Call it from `build()` at the right point in the sequence
3. The output directory is `output_dir`, assets go in `output_dir/assets/`

### Testing Changes

After modifying any module, test with:

```terminal
$ cd ~/phosphor-docs
$ python3 -m phosphor.cli build .
$ python3 -m phosphor.cli serve .
```

The Phosphor docs themselves serve as the most comprehensive test case since they use every component type.
