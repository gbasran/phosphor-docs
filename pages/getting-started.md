## Quickstart

Phosphor is a **system-wide CLI tool**. You install it once, then the `phosphor` command works from any directory on your machine. Point it at any project, and it scaffolds and builds a complete docs site.

### How Phosphor Works

:::pipeline
Install Once -> phosphor init -> Write Markdown -> phosphor build -> Deploy _site/
:::

:::cards
::card{icon="download" color="teal" title="Install Once"}
Clone the repo and run `install.sh`. The `phosphor` command is now available system-wide — you never need to install it again.
::

::card{icon="folder-plus" color="blue" title="phosphor init"}
Run `phosphor init` in any project directory. It creates `docs.yaml`, `pages/`, and example content. If you're in a git repo, it auto-detects your project name and GitHub URL.
::

::card{icon="file-text" color="purple" title="Write Markdown"}
Edit the generated `.md` files in `pages/`. Use standard Markdown plus Phosphor's rich components — callouts, terminal blocks, cards, and more.
::

::card{icon="rocket" color="amber" title="Build & Deploy"}
`phosphor build` generates a complete static site in `_site/`. Copy it to any web server, push to GitHub Pages, or use any static host.
::
:::

### 30-Second Start

```terminal
# One-time setup (only do this once)
$ git clone https://github.com/gbasran/phosphor-docs ~/phosphor-docs
$ cd ~/phosphor-docs && ./install.sh
Phosphor installed to /home/user/.local/bin/phosphor

# Now use it from any project directory
$ cd ~/my-project
$ phosphor init
  Created: docs.yaml
  Created: pages/index.md
  Created: pages/getting-started.md

$ phosphor serve
Building site from /home/user/my-project...
  Built: index.html
  Built: getting-started.html

Serving at http://localhost:8000
```

Open `http://localhost:8000` — you'll see a fully-styled documentation site with sidebar navigation, search, and the Terminal Noir theme.

### What Just Happened

1. **`phosphor init`** scaffolded a docs project with a config file and example pages inside your project directory
2. **`phosphor serve`** built the Markdown into HTML and started a local preview server
3. The output lives in **`_site/`** — static HTML you can deploy anywhere

:::info Three commands, that's it
`phosphor init` (scaffold everything) → `phosphor build` (generate site) → `phosphor serve` (preview locally). That's the entire workflow.
:::

## Installation

### Prerequisites

- **Python 3.8+** — any modern Python installation
- **PyYAML** — `pip install pyyaml` (the only dependency)

:::info No Node.js required
Phosphor is pure Python. No npm, no bundlers, no JavaScript toolchain needed. The theme assets are static files served as-is.
:::

### Install Steps

```terminal
$ git clone https://github.com/gbasran/phosphor-docs ~/phosphor-docs
$ cd ~/phosphor-docs
$ pip install pyyaml
$ chmod +x install.sh
$ ./install.sh
Phosphor installed to /home/user/.local/bin/phosphor
```

The installer creates a `phosphor` wrapper script in `~/.local/bin/` (or `~/bin/` if it exists) that points to the phosphor Python module.

### Verify Installation

```terminal
$ phosphor --help
usage: phosphor [-h] {build,init,serve} ...

Phosphor — Static documentation site generator
```

:::accordion{title="PATH troubleshooting"}
If you get `command not found` after installing:

```terminal
$ export PATH="$HOME/.local/bin:$PATH"
```

Add that line to your `~/.bashrc` or `~/.zshrc` to make it permanent:

```terminal
$ echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
$ source ~/.bashrc
```
:::

:::accordion{title="Linux"}
Works out of the box. No special requirements beyond Python 3.8+ and pip.
:::

:::accordion{title="macOS"}
Works with the system Python 3 or any Python installed via Homebrew. If using zsh (default on modern macOS), add the PATH export to `~/.zshrc` instead of `~/.bashrc`.
:::

:::accordion{title="WSL2 (Windows)"}
Works perfectly under WSL2. For best performance, keep your docs project inside the Linux filesystem (e.g., `~/my-docs/`) rather than under `/mnt/c/`. The `/mnt/c/` path crosses a filesystem boundary and will be slower for file operations.
:::

:::tip Alternative: run without installing
You can skip `install.sh` and run Phosphor directly with Python:

`python3 -m phosphor.cli build .`

This works from the phosphor-docs directory, or from anywhere if you set `PYTHONPATH` to include the phosphor-docs directory.
:::

## Your First Docs Site

Let's build documentation for a project called `deploy-cli`.

### Step 1: Initialize

```terminal
$ cd ~/deploy-cli
$ phosphor init
  Created: docs.yaml
  Created: pages/index.md
  Created: pages/getting-started.md
```

`phosphor init` creates everything you need. If you're inside a git repo with a remote origin, it auto-populates the title, tagline, logo, and GitHub link from your repository name.

### Step 2: Edit

Customize `docs.yaml` to match your project:

```
site:
  title: "Deploy CLI"
  tagline: "~/deploy-cli"
  logo_text: "DC"
  github: "https://github.com/you/deploy-cli"

nav:
  - group: "Getting Started"
    items:
      - label: "Overview"
        icon: "home"
        page: "index.md"
        anchor: "overview"
      - label: "Installation"
        icon: "download"
        page: "index.md"
        anchor: "installation"

  - group: "Reference"
    items:
      - label: "Commands"
        icon: "terminal"
        page: "commands.md"
        anchor: "commands"

pages:
  - index.md
  - commands.md
```

Replace the example content in `pages/index.md` with your actual documentation. Add new `.md` files for additional pages — just list them in the `pages:` array.

### Step 3: Build & Preview

```terminal
$ phosphor build
  Built: index.html
  Built: commands.html

Site built to _site/
  2 pages, 2 HTML files

$ phosphor serve
Serving at http://localhost:8000
```

### Step 4: Deploy

The `_site/` directory contains pure static HTML. Copy it to any web server, push to GitHub Pages, or use any static hosting service:

```terminal
$ cp -r _site/ /var/www/deploy-cli-docs/
```

:::tip Let an AI agent write your docs
Point an AI coding agent (Claude Code, Codex, Gemini CLI) at your project with instructions to create phosphor documentation. The agent can read your codebase, understand the structure, and write all the `.md` pages and `docs.yaml` config for you. Then just run `phosphor build` to generate the site. See the `CLAUDE.md` (or `AGENTS.md` / `GEMINI.md`) in the phosphor-docs repo for the full syntax reference agents need.
:::

:::tip Iterative workflow
The typical workflow is: edit Markdown, run `phosphor build`, refresh browser. The `phosphor serve` command also builds before serving, so you can just restart it to see changes.
:::
