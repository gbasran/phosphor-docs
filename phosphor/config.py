"""YAML config loader with defaults for phosphor-docs."""

import os
import sys
import yaml


DEFAULTS = {
    "site": {
        "title": "Documentation",
        "tagline": "",
        "logo_text": "PD",
        "github": "",
        "favicon": "",
    },
    "theme": {},
    "nav": [],
    "pages": [],
}


def load_config(config_path):
    """Load docs.yaml and merge with defaults."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path, "r") as f:
        raw = yaml.safe_load(f) or {}

    if not isinstance(raw, dict):
        print(f"Error: docs.yaml must be a YAML mapping, got {type(raw).__name__}", file=sys.stderr)
        sys.exit(1)

    cfg = {}

    # Merge site section
    raw_site = raw.get("site") or {}
    if not isinstance(raw_site, dict):
        print(f"Error: 'site' must be a mapping in docs.yaml, got {type(raw_site).__name__}", file=sys.stderr)
        sys.exit(1)
    site = dict(DEFAULTS["site"])
    site.update(raw_site)
    cfg["site"] = site

    raw_theme = raw.get("theme") or DEFAULTS["theme"]
    if not isinstance(raw_theme, dict):
        print(f"Error: 'theme' must be a mapping in docs.yaml, got {type(raw_theme).__name__}", file=sys.stderr)
        sys.exit(1)
    cfg["theme"] = raw_theme

    raw_nav = raw.get("nav")
    if raw_nav is None:
        raw_nav = DEFAULTS["nav"]
    if not isinstance(raw_nav, list):
        print(f"Error: 'nav' must be a list in docs.yaml, got {type(raw_nav).__name__}", file=sys.stderr)
        sys.exit(1)
    cfg["nav"] = raw_nav

    raw_pages = raw.get("pages")
    if raw_pages is None:
        raw_pages = DEFAULTS["pages"]
    if not isinstance(raw_pages, list):
        print(f"Error: 'pages' must be a list in docs.yaml, got {type(raw_pages).__name__}", file=sys.stderr)
        sys.exit(1)
    cfg["pages"] = raw_pages

    return cfg
