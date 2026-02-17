"""Build orchestrator for phosphor-docs.

Loads config, parses pages, renders templates, generates search index,
writes output to _site/ directory.
"""

import os
import shutil

from . import config as config_mod
from . import parser as parser_mod
from . import renderer as renderer_mod
from . import search as search_mod


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
    with open(template_path, "r") as f:
        template = f.read()

    # Load search.js template
    search_js_path = os.path.join(phosphor_root, "theme", "search.js")
    with open(search_js_path, "r") as f:
        search_js_template = f.read()

    # Clean and create output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    os.makedirs(os.path.join(output_dir, "assets"))

    # Copy theme assets
    theme_dir = os.path.join(phosphor_root, "theme")
    for fname in ("style.css", "script.js", "favicon.svg"):
        src = os.path.join(theme_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(output_dir, "assets", fname))

    # Copy custom favicon if specified
    custom_favicon = cfg["site"].get("favicon", "")
    if custom_favicon:
        custom_path = os.path.join(project_dir, custom_favicon)
        if os.path.exists(custom_path):
            shutil.copy2(custom_path, os.path.join(output_dir, "assets", "favicon.svg"))

    # Parse all pages
    pages_data = []
    pages_dir = os.path.join(project_dir, "pages")

    for page_file in cfg["pages"]:
        page_path = os.path.join(pages_dir, page_file)
        if not os.path.exists(page_path):
            print(f"  Warning: Page not found: {page_file}")
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
