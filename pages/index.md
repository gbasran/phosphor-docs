:::hero{badge="Static Site Generator"}
# Build **Beautiful Docs** From Markdown
A zero-config documentation generator with the Phosphor Terminal Noir theme. Write Markdown, get a polished dark-mode docs site with search, navigation, and rich components.

[Get Started](getting-started.html#quickstart){.primary}
[Component Gallery](writing-content.html#components){.secondary}
[GitHub](https://github.com/gbasran/phosphor-docs){.secondary}
:::

## Overview

Phosphor is a **system-wide CLI tool** that turns a directory of Markdown files into a complete documentation website. Install it once, then run `phosphor init` in any project directory to scaffold a docs site. No frameworks, no bundlers, no configuration fatigue.

### What You Get

:::cards
::card{icon="file-text" color="teal" title="Markdown-First Content"}
Write documentation in standard Markdown with optional rich components. No proprietary format, no lock-in. Your content stays portable.
::

::card{icon="search" color="blue" title="Instant Search"}
Every heading and paragraph is automatically indexed at build time. Users get fuzzy search with autocomplete, keyboard navigation, and zero JavaScript frameworks.
::

::card{icon="moon" color="purple" title="Terminal Noir Theme"}
A dark theme designed for developer documentation. Monospace accents, syntax-colored terminals, dot-grid backgrounds, and smooth scroll spy.
::

::card{icon="smartphone" color="amber" title="Responsive Design"}
Sidebar navigation collapses into a mobile drawer. Table of contents appears on wide screens. Everything adapts from phone to ultrawide.
::

::card{icon="puzzle" color="teal" title="Rich Components"}
Callouts, cards, terminal blocks, pipelines, decision grids, command references, and accordions. All via simple Markdown syntax.
::

::card{icon="rocket" color="red" title="Zero Dependencies"}
Python 3 + PyYAML. No Node.js, no bundler, no build chain. One install, works everywhere.
::
:::

### How It Works

:::pipeline
Write Markdown -> Configure YAML -> Build Site -> Deploy Anywhere
:::

### Quick Look

```terminal
# Install once (system-wide)
$ git clone https://github.com/gbasran/phosphor-docs ~/phosphor-docs
$ cd ~/phosphor-docs && ./install.sh

# Use from any project directory
$ cd ~/my-project
$ phosphor init
  Created: docs.yaml
  Created: pages/index.md
  Created: pages/getting-started.md

$ phosphor build
  Built: index.html
  Built: getting-started.html

Site built to _site/
  2 pages, 2 HTML files
```

:::tip Install once, use anywhere
Phosphor is a system-wide CLI. After installing, run `phosphor init` inside any project directory to scaffold a docs site. It auto-detects your project name and GitHub URL from the git remote. The same polished theme works whether you're documenting a CLI tool, a library, or an internal system.
:::

### When To Use Phosphor

:::decision-grid
| I want to... | What to do |
| Document a new project | `phosphor init` in your project, edit pages, `phosphor build` |
| Add docs to an existing repo | Create a `docs/` subdirectory, `phosphor init docs/`, build from there |
| Preview changes locally | `phosphor serve` — auto-builds then starts a local server on port 8000 |
| Deploy to GitHub Pages | Build to `_site/`, push that directory to your `gh-pages` branch |
| Customize the theme | Edit `theme/style.css` in your phosphor-docs installation |
:::

### Project Structure

```terminal
$ tree my-project-docs/
my-project-docs/
  docs.yaml          # Site configuration
  pages/
    index.md          # Homepage (supports hero section)
    getting-started.md
    reference.md
  _site/              # Built output (gitignore this)
    index.html
    getting-started.html
    reference.html
    assets/
      style.css
      script.js
      search.js
      favicon.svg
```

### AI Agent Authoring

AI coding agents (Claude Code, Codex, Gemini CLI) can write phosphor documentation for any project. Point an agent at your codebase and tell it to create phosphor docs — it reads the project, understands the structure, and writes all the `.md` pages and `docs.yaml` config.

```terminal
# Example: have an agent write docs for your project
$ cd ~/my-project
$ claude "Create phosphor documentation for this project. Read ~/phosphor-docs/CLAUDE.md for the syntax reference."
$ phosphor build
```

The phosphor-docs repo includes agent instruction files that teach any AI tool the full syntax:

:::decision-grid
| File | Tool | Purpose |
| --- | --- | --- |
| `CLAUDE.md` | Claude Code | Auto-read by Claude when working in the repo |
| `AGENTS.md` | Codex | Auto-read by Codex |
| `GEMINI.md` | Gemini CLI | Auto-read by Gemini |
| `PHOSPHOR_AGENT.md` | Any | Full syntax reference (tool-agnostic) |
:::

The agent reference covers: complete `docs.yaml` config, all `:::` component blocks, page structure rules, build commands, and common page patterns (homepage, reference, FAQ).
