# Phosphor Documentation Generator — Agent Instructions

This project is a Phosphor docs site. Phosphor is a static documentation site generator that takes Markdown + YAML config and produces a dark-themed docs site.

## Quick Reference

- **Build**: `phosphor build` (or `python3 -m phosphor.cli build .` from this directory)
- **Serve**: `phosphor serve` (or `python3 -m phosphor.cli serve .`)
- **Config**: `docs.yaml` — site metadata, nav structure, page list
- **Content**: `pages/*.md` — Markdown files with Phosphor component syntax
- **Output**: `_site/` — static HTML (deploy this)

## Full Syntax Reference

See `PHOSPHOR_AGENT.md` in this directory for the complete reference including:
- All `docs.yaml` config fields
- All Markdown component block syntax (`:::tip`, `:::cards`, `:::hero`, etc.)
- Page structure rules (start with `##`, use `###` for subsections)
- Build commands and common page patterns

## Key Rules

- Pages start with `##` headings, never `#` (h1 is reserved for hero sections)
- Internal links use `.html` extension: `[Page](page.html#section)`
- Every page must be listed in the `pages:` array in `docs.yaml` to be built
- Nav `anchor` values must match auto-generated heading IDs (lowercase, hyphens)
- Icons are Lucide icon names: https://lucide.dev/icons
