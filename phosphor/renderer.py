"""Template renderer for phosphor-docs.

Simple {{VAR}} substitution in base.html template.
Builds sidebar nav HTML from config.
"""

import os
import html as html_mod
import urllib.parse


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


def build_theme_css(theme_config):
    """Build CSS variable overrides from theme config."""
    if not theme_config:
        return ""

    # Map docs.yaml theme keys to CSS custom properties
    key_map = {
        "accent": "--accent",
        "accent_dim": "--accent-dim",
        "accent_glow": "--accent-glow",
        "accent_glow_strong": "--accent-glow-strong",
        "accent_warm": "--accent-warm",
        "accent_warm_dim": "--accent-warm-dim",
        "accent_red": "--accent-red",
        "accent_blue": "--accent-blue",
        "accent_purple": "--accent-purple",
        "bg_deep": "--bg-deep",
        "bg_surface": "--bg-surface",
        "bg_raised": "--bg-raised",
        "bg_hover": "--bg-hover",
        "code_bg": "--code-bg",
        "text": "--text",
        "text_bright": "--text-bright",
        "text_dim": "--text-dim",
        "border": "--border",
        "border_bright": "--border-bright",
    }

    overrides = []
    for yaml_key, css_var in key_map.items():
        if yaml_key in theme_config:
            overrides.append(f"    {css_var}: {theme_config[yaml_key]};")

    if not overrides:
        return ""

    lines = "\n".join(overrides)
    return f"<style>\n  :root {{\n{lines}\n  }}\n</style>"


def render_page(template, config, page_content, nav_html, page_filename):
    """Render a page by substituting variables into the template."""
    site = config["site"]

    # Build the page title
    page_title = site["title"]

    # Build favicon — inline data URI so it always matches the theme
    custom_favicon = site.get("favicon", "")
    if custom_favicon:
        favicon = "assets/favicon.svg"
    else:
        theme = config.get("theme", {})
        accent = theme.get("accent", "#22d3a7")
        accent_dim = theme.get("accent_dim", "#1a9e7e")
        bg_deep = theme.get("bg_deep", "#080c14")
        logo_text = _escape(site.get("logo_text", "PD"))

        favicon_svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0%" stop-color="{accent}"/>'
            f'<stop offset="100%" stop-color="{accent_dim}"/>'
            '</linearGradient></defs>'
            f'<rect width="32" height="32" rx="6" fill="url(#g)"/>'
            f'<text x="16" y="22" text-anchor="middle" '
            f'font-family="system-ui,sans-serif" font-weight="700" '
            f'font-size="14" fill="{bg_deep}">{logo_text}</text>'
            '</svg>'
        )
        favicon = "data:image/svg+xml," + urllib.parse.quote(favicon_svg, safe="<>/:='\"#! ")

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

    # Theme overrides
    theme_css = build_theme_css(config.get("theme", {}))

    # Substitutions
    output = template
    output = output.replace("{{THEME_CSS}}", theme_css)
    output = output.replace("{{TITLE}}", _escape(page_title))
    output = output.replace("{{SITE_TITLE}}", _escape(site["title"]))
    output = output.replace("{{TAGLINE}}", _escape(site.get("tagline", "")))
    output = output.replace("{{LOGO_TEXT}}", _escape(site.get("logo_text", "PD")))
    output = output.replace("{{FAVICON}}", favicon)
    output = output.replace("{{NAV}}", nav_html)
    output = output.replace("{{GITHUB_LINK}}", github_html)
    output = output.replace("{{CONTENT}}", page_content)

    return output
