"""Template renderer for phosphor-docs.

Simple {{VAR}} substitution in base.html template.
Builds sidebar nav HTML from config.
"""

import os
import html as html_mod


def _escape(text):
    return html_mod.escape(text)


def build_nav_html(nav_config, current_page):
    """Build sidebar navigation HTML from nav config."""
    html = ""
    for group in nav_config:
        group_label = group.get("group", "")
        html += f'<div class="nav-group">\n'
        html += f'  <div class="nav-group-label">{_escape(group_label)}</div>\n'

        for item in group.get("items", []):
            label = item.get("label", "")
            icon = item.get("icon", "file")
            page = item.get("page", "")
            anchor = item.get("anchor", "")

            # Convert .md to .html
            page_html = page.replace(".md", ".html") if page else ""
            href = f"{page_html}#{anchor}" if anchor else page_html

            html += (
                f'  <a href="{href}">'
                f'<i data-lucide="{_escape(icon)}" class="nav-icon"></i>'
                f'{_escape(label)}'
                f'</a>\n'
            )

        html += '</div>\n'

    return html


def build_toc_html(headings):
    """Build table of contents HTML from heading list."""
    if len(headings) <= 1:
        return ""

    html = '<div class="toc-label">On this page</div>\n'
    for h in headings:
        cls = "toc-h3" if h["level"] == 3 else ""
        cls_attr = f' class="{cls}"' if cls else ""
        html += f'<a href="#{h["id"]}"{cls_attr}>{_escape(h["text"])}</a>\n'

    return html


def render_page(template, config, page_content, nav_html, page_filename):
    """Render a page by substituting variables into the template."""
    site = config["site"]

    # Build the page title
    page_title = site["title"]

    # Determine favicon path
    favicon = site.get("favicon", "")
    if not favicon:
        favicon = "assets/favicon.svg"
    elif not favicon.startswith("assets/"):
        favicon = "assets/favicon.svg"

    # GitHub link
    github_url = site.get("github", "")
    github_html = ""
    if github_url:
        github_html = (
            f'<a href="{_escape(github_url)}" '
            f'style="display:flex;align-items:center;gap:8px;padding:12px 16px;'
            f'color:var(--text-dim);font-size:12px;text-decoration:none;'
            f'border-top:1px solid var(--border);margin-top:auto;">'
            f'<i data-lucide="github" style="width:14px;height:14px;"></i>'
            f'GitHub'
            f'</a>'
        )

    # Substitutions
    output = template
    output = output.replace("{{TITLE}}", _escape(page_title))
    output = output.replace("{{SITE_TITLE}}", _escape(site["title"]))
    output = output.replace("{{TAGLINE}}", _escape(site.get("tagline", "")))
    output = output.replace("{{LOGO_TEXT}}", _escape(site.get("logo_text", "PD")))
    output = output.replace("{{FAVICON}}", _escape(favicon))
    output = output.replace("{{NAV}}", nav_html)
    output = output.replace("{{GITHUB_LINK}}", github_html)
    output = output.replace("{{CONTENT}}", page_content)

    return output
