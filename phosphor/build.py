"""Build orchestrator for phosphor-docs.

Loads config, parses pages, renders templates, generates search index,
writes output to _site/ directory.
"""

import os
import re
import shutil
import sys

from . import config as config_mod
from . import parser as parser_mod
from . import renderer as renderer_mod
from . import search as search_mod


def _is_safe_path(path, allowed_dir):
    """Check that *path* resolves inside *allowed_dir* (prevents traversal)."""
    real = os.path.realpath(path)
    allowed = os.path.realpath(allowed_dir)
    return real == allowed or real.startswith(allowed + os.sep)


_COLOR_RE = re.compile(r"^(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\))$")


def build(project_dir, output_dir=None):
    """Build the documentation site.

    Args:
        project_dir: Directory containing docs.yaml and pages/
        output_dir: Output directory (default: project_dir/_site)
    """
    project_dir = os.path.abspath(project_dir)
    if output_dir is None:
        output_dir = os.path.join(project_dir, "_site")

    # Find phosphor root (where templates/ and theme/ live)
    phosphor_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Load config
    config_path = os.path.join(project_dir, "docs.yaml")
    cfg = config_mod.load_config(config_path)

    # Load base template
    template_path = os.path.join(phosphor_root, "templates", "base.html")
    if not os.path.exists(template_path):
        print(f"Error: base template not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    with open(template_path, "r") as f:
        template = f.read()

    # Load search.js template
    search_js_path = os.path.join(phosphor_root, "theme", "search.js")
    if not os.path.exists(search_js_path):
        print(f"Error: search.js template not found: {search_js_path}", file=sys.stderr)
        sys.exit(1)
    with open(search_js_path, "r") as f:
        search_js_template = f.read()

    # Clean and create output directory
    if os.path.exists(output_dir):
        try:
            shutil.rmtree(output_dir)
        except PermissionError as e:
            print(f"Error: cannot remove output directory: {e}", file=sys.stderr)
            sys.exit(1)
    os.makedirs(output_dir)
    os.makedirs(os.path.join(output_dir, "assets"))

    # Copy theme assets
    theme_dir = os.path.join(phosphor_root, "theme")
    for fname in ("style.css", "script.js"):
        src = os.path.join(theme_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(output_dir, "assets", fname))

    # Generate themed favicon
    custom_favicon = cfg["site"].get("favicon", "")
    if custom_favicon:
        # User-provided custom favicon — copy only if inside project dir
        custom_path = os.path.join(project_dir, custom_favicon)
        if not _is_safe_path(custom_path, project_dir):
            print(f"  Error: favicon path escapes project directory: {custom_favicon}", file=sys.stderr)
            sys.exit(1)
        if os.path.exists(custom_path):
            shutil.copy2(custom_path, os.path.join(output_dir, "assets", "favicon.svg"))
        else:
            print(f"  Warning: favicon not found: {custom_favicon}", file=sys.stderr)
    else:
        # Generate favicon from theme colors and logo_text
        theme = cfg.get("theme", {})
        accent = theme.get("accent", "#22d3a7")
        accent_dim = theme.get("accent_dim", "#1a9e7e")
        bg_deep = theme.get("bg_deep", "#080c14")
        logo_text = cfg["site"].get("logo_text", "PD")

        # Validate that color values look safe before injecting into SVG
        for color_name, color_val in [("accent", accent), ("accent_dim", accent_dim), ("bg_deep", bg_deep)]:
            if not _COLOR_RE.match(str(color_val)):
                print(f"  Error: invalid theme color for {color_name}: {color_val!r}", file=sys.stderr)
                sys.exit(1)

        from . renderer import _escape
        safe_logo = _escape(str(logo_text))

        favicon_svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">\n'
            '  <defs>\n'
            '    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">\n'
            f'      <stop offset="0%" stop-color="{accent}"/>\n'
            f'      <stop offset="100%" stop-color="{accent_dim}"/>\n'
            '    </linearGradient>\n'
            '  </defs>\n'
            f'  <rect width="32" height="32" rx="6" fill="url(#g)"/>\n'
            f'  <text x="16" y="22" text-anchor="middle" '
            f'font-family="system-ui,sans-serif" font-weight="700" '
            f'font-size="14" fill="{bg_deep}">{safe_logo}</text>\n'
            '</svg>\n'
        )

        favicon_path = os.path.join(output_dir, "assets", "favicon.svg")
        with open(favicon_path, "w") as f:
            f.write(favicon_svg)

    # Parse all pages
    pages_data = []
    pages_dir = os.path.join(project_dir, "pages")

    if not os.path.isdir(pages_dir):
        print(f"Error: pages/ directory not found at {pages_dir}", file=sys.stderr)
        sys.exit(1)

    for page_file in cfg["pages"]:
        page_path = os.path.join(pages_dir, page_file)
        if not _is_safe_path(page_path, pages_dir):
            print(f"  Error: page path escapes pages/ directory: {page_file}", file=sys.stderr)
            sys.exit(1)
        if not os.path.exists(page_path):
            print(f"  Warning: Page not found: {page_file}", file=sys.stderr)
            continue

        with open(page_path, "r") as f:
            md_content = f.read()

        html_content, headings = parser_mod.parse_markdown(md_content)
        html_filename = page_file.replace(".md", ".html")

        pages_data.append({
            "filename": html_filename,
            "md_file": page_file,
            "headings": headings,
            "html": html_content,
        })

    # Build search index
    index_json = search_mod.build_search_index(pages_data)
    search_js_final = search_mod.inject_search_index(search_js_template, index_json)

    # Write search.js with injected index
    with open(os.path.join(output_dir, "assets", "search.js"), "w") as f:
        f.write(search_js_final)

    # Build nav HTML (same for all pages)
    nav_html = renderer_mod.build_nav_html(cfg["nav"], "")

    # Render and write each page
    for page in pages_data:
        page_output = renderer_mod.render_page(
            template,
            cfg,
            page["html"],
            nav_html,
            page["filename"],
        )

        out_path = os.path.join(output_dir, page["filename"])
        with open(out_path, "w") as f:
            f.write(page_output)

        print(f"  Built: {page['filename']}")

    print(f"\nSite built to {output_dir}/")
    print(f"  {len(pages_data)} pages, {len(pages_data)} HTML files")
