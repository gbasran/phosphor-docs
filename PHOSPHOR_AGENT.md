# Phosphor — Agent Reference

Phosphor is a static documentation site generator. It takes Markdown files + a YAML config and produces a complete dark-themed docs site with sidebar navigation, search, and rich components.

## Key Concepts

- Phosphor is a **system-wide CLI** installed at `~/phosphor-docs`
- Run `phosphor init` in any project directory to scaffold docs
- Run `phosphor build` to generate `_site/` (static HTML output)
- Run `phosphor serve` to build and preview locally on port 8000
- All content lives in `pages/*.md`, config lives in `docs.yaml`

## Project Structure

```
my-project/
  docs.yaml              # Site configuration
  pages/
    index.md             # Homepage (supports hero section)
    getting-started.md   # Additional pages
    reference.md
  _site/                 # Build output (deploy this)
```

## docs.yaml — Complete Reference

```yaml
site:
  title: "Project Name"           # Sidebar header + browser tab
  tagline: "~/project-name"       # Subtitle below logo
  logo_text: "PN"                 # 1-2 chars for logo icon
  github: "https://github.com/user/repo"  # GitHub link in sidebar
  favicon: ""                     # Optional custom favicon path (auto-themed if empty)

theme:                            # Override CSS color variables (all optional)
  accent: "#8b5cf6"               # Primary accent
  accent_dim: "#7c3aed"           # Accent hover/darker
  accent_glow: "rgba(...)"        # Subtle accent overlay
  accent_glow_strong: "rgba(...)" # Stronger accent overlay
  accent_warm: "#c084fc"          # Warm accent (tips, warnings)
  accent_warm_dim: "rgba(...)"    # Subtle warm overlay
  accent_red: "#f472b6"           # Red (errors)
  accent_blue: "#818cf8"          # Blue (info callouts)
  accent_purple: "#c084fc"        # Purple (code syntax)
  bg_deep: "#070312"              # Body background
  bg_surface: "#0e0822"           # Sidebar, cards
  bg_raised: "#160f2e"            # Elevated elements
  bg_hover: "#1e1438"             # Hover states
  code_bg: "#080418"              # Code blocks
  text: "#b4b0c8"                 # Body text
  text_bright: "#e8e4f0"          # Headings
  text_dim: "#6e6890"             # Labels, captions
  border: "#1c1535"               # Borders
  border_bright: "#2a2048"        # Prominent borders

nav:
  - group: "Section Label"        # Sidebar group heading (uppercase)
    items:
      - label: "Page Title"       # Sidebar link text
        icon: "home"              # Lucide icon name
        page: "page.md"           # Markdown file (auto-converts to .html)
        anchor: "section-id"      # Optional anchor (#section-id)

pages:                            # Build order — every .md file to include
  - index.md
  - getting-started.md
  - reference.md
```

### Nav Icons

Any [Lucide icon](https://lucide.dev/icons) name works. Common ones:
`home`, `zap`, `download`, `file-text`, `terminal`, `code`, `settings`, `search`, `rocket`, `shield`, `puzzle`, `git-branch`, `database`, `globe`, `bot`, `sparkles`, `layers`, `compass`, `palette`, `cpu`, `triangle-alert`, `circle-help`, `layout-grid`

### Anchor IDs

Anchors are auto-generated from headings by lowercasing and replacing spaces with hyphens:
- `## Getting Started` → `getting-started`
- `### CLI Commands` → `cli-commands`
- `## FAQ & Troubleshooting` → `faq--troubleshooting`

## Markdown Syntax — Complete Reference

### Page Structure Rules

- **Start pages with `##`** (h2), never `#` (h1 is reserved for hero titles)
- Use `###` for subsections, `####` for minor headings
- Every `##` and `###` heading appears in the table of contents and search index

### Standard Markdown

All standard Markdown works: **bold**, *italic*, `inline code`, [links](url), images, ordered/unordered lists, tables, code blocks, horizontal rules (`---`).

Internal links use `.html` extension: `[Other Page](other-page.html#section)`

### Component Blocks

Components use `:::type` fenced block syntax.

#### Hero Section (homepage only)

```markdown
:::hero{badge="Badge Text"}
# Title With **Accent Words**
Description paragraph.

[Primary Button](url){.primary}
[Secondary Button](url){.secondary}
:::
```

- `**text**` in the title gets teal accent color
- `{.primary}` = teal filled button, `{.secondary}` = outlined button

#### Callouts

```markdown
:::tip Title text
Body content with **bold** and `code`.
:::

:::info Title text
Informational content.
:::

:::warn Title text
Warning content.
:::
```

Types: `tip` (teal), `info` (blue), `warn` (amber)

#### Terminal Blocks

````markdown
```terminal
$ command-here
Output text (dimmed)
# Comment (dimmed italic)
$ another-command --with-flags
```
````

Line prefixes: `$ ` = green command, `# ` = comment, anything else = output

#### Cards

```markdown
:::cards
::card{icon="icon-name" color="teal" title="Card Title"}
Description text.
::

::card{icon="icon-name" color="blue" title="Another Card"}
Another description.
::
:::
```

Colors: `teal`, `amber`, `blue`, `purple`, `red`

#### Pipeline Diagrams

```markdown
:::pipeline
Stage 1 -> Stage 2 -> Stage 3 -> Stage 4
:::
```

#### Decision Grids

```markdown
:::decision-grid
| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Cell | Cell | Cell |
:::
```

#### Command Blocks

```markdown
:::command{title="cmd-name" usage="cmd-name [args] [flags]"}
::flag{name="--flag" short="-f"}
Flag description.
::
:::
```

#### Accordions

```markdown
:::accordion{title="Summary text"}
Hidden content revealed on click.
Supports **Markdown** formatting.
:::
```

## Build Commands

```bash
# From inside the project directory:
phosphor build          # Build site to _site/
phosphor serve          # Build + serve on localhost:8000
phosphor init           # Scaffold docs.yaml + pages/ with examples

# Or specify a directory:
phosphor build path/to/project
phosphor serve path/to/project

# Without installing (from phosphor-docs dir):
python3 -m phosphor.cli build path/to/project
```

## Common Page Patterns

### Homepage (index.md)

```markdown
:::hero{badge="Project Type"}
# Build **Amazing Things**
Short description of the project.

[Get Started](getting-started.html#quickstart){.primary}
[GitHub](https://github.com/user/repo){.secondary}
:::

## Overview

Description of what the project does.

### Features

:::cards
::card{icon="zap" color="teal" title="Feature 1"}
Description.
::
::card{icon="shield" color="blue" title="Feature 2"}
Description.
::
:::
```

### Reference Page

```markdown
## CLI Commands

:::command{title="my-tool run" usage="my-tool run [file] [-v] [-o output]"}
::flag{name="file" short="f"}
Input file path.
::
::flag{name="--verbose" short="-v"}
Enable verbose output.
::
::flag{name="--output" short="-o"}
Output directory. Defaults to current directory.
::
:::

## Configuration

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `option1` | string | `""` | What it does |
| `option2` | bool | `false` | What it controls |
```

### FAQ Page

```markdown
## FAQ

:::accordion{title="Question one?"}
Answer with **formatting** and `code`.
:::

:::accordion{title="Question two?"}
Another answer.
:::
```

## Workflow for Agents

When asked to create phosphor documentation for a project:

1. Read the project's codebase to understand its structure and purpose
2. Create `docs.yaml` with appropriate site metadata, nav structure, and page list
3. Create `pages/index.md` with a hero section, overview, and feature cards
4. Create `pages/getting-started.md` with installation and quickstart instructions
5. Create additional pages as needed (reference, guides, etc.)
6. Run `phosphor build` to generate the site
7. Verify the build succeeds with no errors
