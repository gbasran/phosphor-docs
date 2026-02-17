"""YAML config loader with defaults for phosphor-docs."""

import os
import yaml


DEFAULTS = {
    "site": {
        "title": "Documentation",
        "tagline": "",
        "logo_text": "PD",
        "github": "",
        "favicon": "",
    },
    "nav": [],
    "pages": [],
}


def load_config(config_path):
    """Load docs.yaml and merge with defaults."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path, "r") as f:
        raw = yaml.safe_load(f) or {}

    cfg = {}

    # Merge site section
    site = dict(DEFAULTS["site"])
    site.update(raw.get("site", {}))
    cfg["site"] = site

    cfg["nav"] = raw.get("nav", DEFAULTS["nav"])
    cfg["pages"] = raw.get("pages", DEFAULTS["pages"])

    return cfg
