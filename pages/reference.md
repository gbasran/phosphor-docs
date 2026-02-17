## CLI Commands

Phosphor has three commands: `build`, `init`, and `serve`.

### phosphor build

:::command{title="phosphor build" usage="phosphor build [directory]"}
::flag{name="directory" short="dir"}
Path to the project directory containing `docs.yaml` and `pages/`. Defaults to the current directory (`.`).
::
:::

Builds your documentation site. Reads `docs.yaml`, parses all Markdown pages, generates the search index, and writes the complete site to the `_site/` directory.

```terminal
$ phosphor build
Building site from /home/user/my-docs...
  Built: index.html
  Built: getting-started.html
  Built: reference.html

Site built to /home/user/my-docs/_site/
  3 pages, 3 HTML files
```

The build process:

1. Loads and validates `docs.yaml`
2. Reads each `.md` file listed in the `pages` array
3. Parses Markdown into HTML (standard + extended components)
4. Generates the search index from all headings and content
5. Renders each page into the base HTML template
6. Copies theme assets (CSS, JS, favicon) to `_site/assets/`
7. Writes the final HTML files to `_site/`

:::info Clean builds
Every build deletes and recreates the `_site/` directory from scratch. This ensures no stale files remain from previous builds. The `_site/` directory should be in your `.gitignore`.
:::

### phosphor init

:::command{title="phosphor init" usage="phosphor init [directory]"}
::flag{name="directory" short="dir"}
Target directory for the new docs project. Defaults to the current directory (`.`). Created if it doesn't exist.
::
:::

Scaffolds a new documentation project. Creates a `docs.yaml` config file and example Markdown pages to get you started immediately.

```terminal
$ phosphor init my-new-docs
  Created: docs.yaml
  Created: pages/index.md
  Created: pages/getting-started.md

Docs project initialized in /home/user/my-new-docs/
Next steps:
  1. Edit docs.yaml to configure your site
  2. Edit pages/*.md to write your content
  3. Run: phosphor build
```

:::tip Auto-detects your GitHub repo
If you run `phosphor init` inside a Git repository with a remote origin, it automatically detects the GitHub URL and populates `docs.yaml` with sensible defaults:
- **title**: Repository name, title-cased (e.g., `my-cli-tool` becomes `My CLI Tool`)
- **tagline**: `~/repo-name`
- **logo_text**: First two characters of the repo name, uppercase
- **github**: Full GitHub URL

You can always edit these afterward.
:::

Key behaviors:

- **Won't overwrite**: Existing files are never overwritten. If `docs.yaml` or a page file already exists, it's skipped with a message
- **Creates directories**: The target directory and `pages/` subdirectory are created if they don't exist
- **Example content**: The scaffolded pages include working examples of various components so you can see the syntax in action

### phosphor serve

:::command{title="phosphor serve" usage="phosphor serve [directory] [-p PORT]"}
::flag{name="directory" short="dir"}
Path to the project directory containing `docs.yaml`. Defaults to the current directory.
::
::flag{name="--port" short="-p"}
Port number for the local HTTP server. Defaults to 8000.
::
:::

Builds the site and starts a local HTTP server for previewing. This is a convenience command that combines `phosphor build` with Python's built-in HTTP server.

```terminal
$ phosphor serve
Building site from /home/user/my-docs...
  Built: index.html
  Built: getting-started.html

Serving at http://localhost:8000
Press Ctrl+C to stop.
```

```terminal
$ phosphor serve -p 3000
Building site from /home/user/my-docs...
  Built: index.html

Serving at http://localhost:3000
Press Ctrl+C to stop.
```

:::warn Not for production
The serve command uses Python's `http.server` module, which is designed for development only. For production, build with `phosphor build` and deploy the `_site/` directory to a proper web server or static hosting service.
:::

## Architecture

### How Phosphor Works

Phosphor is a build-time static site generator. There's no runtime server, no client-side rendering, and no JavaScript framework. The build process transforms Markdown files into complete HTML pages.

:::pipeline
Config -> Parse -> Render -> Search -> Output
:::

### Build Pipeline

:::cards
::card{icon="settings" color="teal" title="1. Config Loader"}
Reads `docs.yaml`, merges with defaults. Validates that all required fields exist and all referenced page files are present.
::

::card{icon="file-text" color="blue" title="2. Markdown Parser"}
Processes each `.md` file in two passes: first extracts `:::` component blocks and converts them to HTML, then processes standard Markdown (headings, paragraphs, lists, code, tables).
::

::card{icon="layout-grid" color="amber" title="3. Template Renderer"}
Substitutes variables (`{{TITLE}}`, `{{NAV}}`, `{{CONTENT}}`) in the base HTML template. Builds sidebar navigation HTML from the config.
::

::card{icon="search" color="purple" title="4. Search Indexer"}
Walks all parsed pages, extracts every heading and surrounding text, generates a JSON search index, and injects it into the search JavaScript file.
::

::card{icon="folder-output" color="red" title="5. Output Writer"}
Copies theme assets to `_site/assets/`, writes each rendered HTML page to `_site/`, and produces the final search.js with the embedded index.
::
:::

### File Structure

```terminal
$ tree ~/phosphor-docs/
phosphor-docs/
  phosphor/
    __init__.py       # Package marker
    __main__.py       # python3 -m phosphor entry point
    cli.py            # CLI argument parsing and commands
    build.py          # Build orchestrator
    config.py         # YAML config loader with defaults
    parser.py         # Extended Markdown-to-HTML parser
    renderer.py       # Template variable substitution
    search.py         # Search index generator
  templates/
    base.html         # HTML page shell with {{VAR}} placeholders
  theme/
    style.css         # Phosphor Terminal Noir CSS
    script.js         # TOC generation, scroll spy, mobile toggle
    search.js         # Search engine with {{SEARCH_INDEX}} placeholder
    favicon.svg       # Default gradient favicon
  examples/
    docs.yaml         # Example config for scaffolding
    pages/            # Example Markdown pages for scaffolding
  install.sh          # Symlink installer
  requirements.txt    # Python dependencies (pyyaml)
```

### The Parser

The Markdown parser works in two passes:

1. **Fenced block pass**: Scans for `:::type` blocks and converts them into HTML. Supports nesting (e.g., cards inside a section). This pass runs first so component HTML doesn't get processed as Markdown.

2. **Standard Markdown pass**: Processes the remaining text for headings, paragraphs, lists, code blocks, tables, bold, italic, links, and images. HTML blocks from the first pass are passed through untouched.

### The Template

The base HTML template at `templates/base.html` defines the page shell:

| Placeholder | Content |
| --- | --- |
| `{{TITLE}}` | Site title (from `site.title`) |
| `{{SITE_TITLE}}` | Same as TITLE (sidebar header) |
| `{{TAGLINE}}` | Subtitle (from `site.tagline`) |
| `{{LOGO_TEXT}}` | 1-2 char logo text |
| `{{FAVICON}}` | Favicon path |
| `{{NAV}}` | Generated sidebar navigation HTML |
| `{{GITHUB_LINK}}` | GitHub link HTML (or empty) |
| `{{CONTENT}}` | Parsed page content HTML |

### Dependencies

| Dependency | Version | Purpose |
| --- | --- | --- |
| Python 3 | 3.8+ | Runtime |
| PyYAML | 6.0+ | `docs.yaml` parsing |
| Lucide Icons | CDN (latest) | Icon library (loaded at runtime from CDN) |
| Google Fonts | CDN | Chakra Petch, Nunito Sans, JetBrains Mono |

No Node.js, no npm, no build tools. The JavaScript and CSS are hand-written static files.

## Deployment

### Static Hosting

The `_site/` directory contains pure static HTML, CSS, and JavaScript. It can be served by any web server or static hosting service.

### GitHub Pages

```terminal
$ phosphor build
$ cd _site
$ git init
$ git add -A
$ git commit -m "Deploy docs"
$ git remote add origin https://github.com/user/repo.git
$ git push -f origin main:gh-pages
```

Or with an existing repo, push the `_site/` contents to a `gh-pages` branch.

### Netlify / Vercel / Cloudflare Pages

Point the hosting service to your repo and set:

- **Build command**: `cd path/to/docs && phosphor build` (or just copy `_site/`)
- **Publish directory**: `_site/`

### Nginx

```
server {
    listen 80;
    server_name docs.example.com;
    root /var/www/docs;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Apache

```
DocumentRoot "/var/www/docs"
DirectoryIndex index.html
```

### Rsync

For simple deployment to any server:

```terminal
$ phosphor build
$ rsync -avz _site/ user@server:/var/www/docs/
```

## Troubleshooting

:::accordion{title="command not found: phosphor"}
The `phosphor` command isn't in your PATH. Either:
1. Run the installer: `./install.sh`
2. Add `~/.local/bin` to your PATH: `export PATH="$HOME/.local/bin:$PATH"`
3. Run directly: `python3 -m phosphor.cli build`
:::

:::accordion{title="Config not found: docs.yaml"}
You're running `phosphor build` from a directory that doesn't contain `docs.yaml`. Either:
1. `cd` to your docs project directory first
2. Pass the directory as an argument: `phosphor build path/to/docs/`
3. Run `phosphor init` to create a new docs project
:::

:::accordion{title="Warning: Page not found"}
A file listed in the `pages` array of `docs.yaml` doesn't exist in the `pages/` directory. Check:
1. The filename spelling matches exactly (case-sensitive)
2. The file is in the `pages/` subdirectory, not the project root
3. The file has the `.md` extension
:::

:::accordion{title="ModuleNotFoundError: No module named 'yaml'"}
PyYAML isn't installed. Fix with: `pip install pyyaml`

If you have multiple Python versions, make sure you're installing for the right one: `python3 -m pip install pyyaml`
:::

:::accordion{title="Build output looks broken (no styling)"}
The CSS isn't loading. Check:
1. The `_site/assets/` directory contains `style.css`, `script.js`, and `search.js`
2. You're opening the HTML files through a web server (use `phosphor serve`), not directly as `file://` URLs. Some browsers block local file loading.
3. The `theme/` directory in your Phosphor installation has all the asset files
:::

:::accordion{title="Search returns no results"}
The search index might be empty. Verify:
1. Your pages have `##` headings (h2) — these are the primary units for search indexing
2. The pages are listed in the `pages` array in `docs.yaml`
3. Rebuild with `phosphor build` after adding new content
:::

:::accordion{title="Slow build on WSL2"}
If your docs project is on the Windows filesystem (`/mnt/c/...`), file operations are slow due to the WSL2 filesystem bridge. Move your project to the Linux filesystem (`~/my-docs/`) for faster builds.
:::

:::accordion{title="Lucide icons not rendering"}
Icons appear as empty squares or text. This means the Lucide CDN script isn't loading. Check:
1. You have internet connectivity (Lucide loads from `unpkg.com`)
2. Your browser isn't blocking CDN scripts
3. The generated HTML includes the Lucide script tag near the bottom
:::

## FAQ

:::accordion{title="What's the minimum I need to get started?"}
Python 3.8+, PyYAML, and the Phosphor repo. Run `phosphor init`, edit the generated files, run `phosphor build`. That's it.
:::

:::accordion{title="Can I use this for any project?"}
Yes. Phosphor is project-agnostic. The theme and components work for CLI tools, libraries, APIs, internal tools, or any technical documentation. Just change the config and write your content.
:::

:::accordion{title="How many pages can Phosphor handle?"}
As many as you need. Phosphor processes pages sequentially and the build is fast (sub-second for typical doc sites). Each page is an independent HTML file.
:::

:::accordion{title="Can I have multiple docs sites?"}
Yes. Each docs site is an independent directory with its own `docs.yaml` and `pages/`. They all share the same Phosphor installation (theme, templates, CLI). You can have dozens of sites.
:::

:::accordion{title="Does it support syntax highlighting?"}
Code blocks use the Phosphor monospace styling but don't include language-specific syntax highlighting. For terminal blocks specifically, Phosphor colors commands, output, and comments differently. General-purpose syntax highlighting could be added via a post-processing step.
:::

:::accordion{title="Can I customize the HTML template?"}
Yes. Edit `templates/base.html` in the Phosphor installation to change the page structure, add analytics scripts, modify the footer, or add custom meta tags. The template uses `{{VAR}}` placeholders.
:::

:::accordion{title="Is JavaScript required?"}
The site works without JavaScript for basic reading. JavaScript enhances the experience with: search, table of contents generation, scroll spy navigation highlighting, and Lucide icon rendering. All content is readable without JS.
:::

:::accordion{title="How do I update Phosphor?"}
Pull the latest changes from the repository. Your project files (`docs.yaml`, `pages/`) are separate from the Phosphor installation, so updates won't affect your content.
:::

:::accordion{title="Can I contribute or fork?"}
Yes. Phosphor is open source. Fork the repo, modify the theme, add components, or adapt it for your needs. The codebase is intentionally small and readable.
:::
