## docs.yaml

Every Phosphor project has a `docs.yaml` file at its root. This is the single configuration file that controls your site's metadata, navigation, and build order.

### Full Reference

Here's a complete `docs.yaml` with every available option:

```
site:
  title: "Project Name"         # Site title (shown in sidebar header, browser tab)
  tagline: "~/project-name"     # Subtitle below the logo (typically a path or version)
  logo_text: "PN"               # 1-2 character text shown in the logo icon
  github: "https://github.com/user/repo"  # GitHub link (shown in sidebar footer)
  favicon: ""                   # Custom favicon path (relative to project dir, optional)

nav:
  - group: "Group Label"        # Sidebar section label (uppercase, small text)
    items:
      - label: "Page Title"     # Link text shown in sidebar
        icon: "home"            # Lucide icon name
        page: "page.md"         # Markdown file (auto-converted to .html in links)
        anchor: "section-id"    # Section anchor (appended as #section-id)

pages:                          # Build order — list every .md file to include
  - index.md
  - getting-started.md
  - reference.md
```

### Site Section

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `title` | string | `"Documentation"` | Site title displayed in the sidebar and browser tab |
| `tagline` | string | `""` | Subtitle below the logo — typically a path or version string |
| `logo_text` | string | `"PD"` | 1-2 characters shown in the gradient logo icon |
| `github` | string | `""` | GitHub repository URL. If set, a GitHub link appears at the sidebar bottom |
| `favicon` | string | `""` | Path to a custom favicon (relative to project directory). If empty, uses the default Phosphor favicon |

:::tip Auto-detection from Git
When you run `phosphor init` inside a Git repository with a remote origin, Phosphor automatically detects your GitHub URL and populates the `title`, `tagline`, `logo_text`, and `github` fields from the repository name. You can always override these afterward.
:::

### Nav Section

The `nav` array defines the sidebar navigation. Items are organized into groups.

#### Group Structure

```
nav:
  - group: "Getting Started"
    items:
      - label: "Overview"
        icon: "home"
        page: "index.md"
        anchor: "overview"
```

| Field | Description |
| --- | --- |
| `group` | Section heading text (rendered as uppercase small text) |
| `items` | Array of navigation links |

#### Item Structure

| Field | Required | Description |
| --- | --- | --- |
| `label` | Yes | Link text displayed in the sidebar |
| `icon` | Yes | Lucide icon name (e.g., `"home"`, `"terminal"`, `"settings"`) |
| `page` | Yes | The `.md` filename — automatically converted to `.html` in the built link |
| `anchor` | No | Section ID to link to. Produces `page.html#anchor` |

:::info Anchor IDs match heading slugs
The `anchor` value should match the auto-generated ID from your `## Heading`. For example, `## CLI Commands` generates the ID `cli-commands`, so use `anchor: "cli-commands"`.
:::

#### Multiple Groups

You can have as many groups as you need:

```
nav:
  - group: "Getting Started"
    items:
      - label: "Overview"
        icon: "home"
        page: "index.md"
        anchor: "overview"

  - group: "Guides"
    items:
      - label: "Writing Content"
        icon: "file-text"
        page: "guides.md"
        anchor: "writing"

  - group: "Reference"
    items:
      - label: "Commands"
        icon: "terminal"
        page: "reference.md"
        anchor: "commands"
      - label: "FAQ"
        icon: "circle-help"
        page: "reference.md"
        anchor: "faq"
```

### Pages Section

The `pages` array lists every Markdown file to build, in order:

```
pages:
  - index.md
  - getting-started.md
  - writing-content.md
  - configuration.md
  - reference.md
```

- Each entry is a filename relative to the `pages/` directory
- Files are processed in the listed order
- The `.md` extension is replaced with `.html` in the output
- Files not listed here are **not built** — this lets you keep drafts in `pages/` without publishing them

:::warn Every page must be listed
If a Markdown file exists in `pages/` but isn't listed in the `pages` array, it won't be included in the build. This is intentional — it gives you control over what gets published.
:::

## Navigation

### How Navigation Works

The sidebar navigation is generated from the `nav` section of `docs.yaml`. Each page shares the same sidebar. When you click a nav link, it navigates to the page and section specified by the `page` and `anchor` fields.

### Scroll Spy

Phosphor includes scroll spy that automatically highlights the active navigation item as you scroll through the page. This works by tracking which `## Section` heading is currently in view and matching it against the nav item anchors.

### Table of Contents

On wide screens (1200px and above), a sticky table of contents appears to the left of the content area. It's automatically generated from all `##` and `###` headings on the current page and includes its own scroll spy highlighting.

### Linking Between Pages

When creating links between pages in your Markdown content, always use the `.html` extension:

```
[See the commands](reference.html#commands)
[Back to home](index.html)
```

The `#section-id` anchor is optional but recommended for linking to specific sections.

### Search Integration

Every heading and its surrounding content is automatically indexed for search. The search box in the sidebar supports:

- Fuzzy matching across titles, sections, and content keywords
- Keyboard navigation (arrow keys to move, Enter to select, Escape to close)
- The `/` key as a global shortcut to focus the search box
- Up to 8 results shown at a time, sorted by relevance

## Theming

### The Phosphor Theme

Phosphor ships with the Terminal Noir theme — a dark color scheme designed for developer documentation. The theme is defined in CSS variables in `theme/style.css`.

### Color Palette

| Variable | Value | Use |
| --- | --- | --- |
| `--bg-deep` | `#080c14` | Page background |
| `--bg-surface` | `#0e1320` | Sidebar, card backgrounds |
| `--bg-raised` | `#151c2c` | Elevated elements, code headers |
| `--bg-hover` | `#1a2338` | Hover states |
| `--accent` | `#22d3a7` | Primary teal accent |
| `--accent-warm` | `#f0a500` | Amber accent (warnings) |
| `--accent-red` | `#f47067` | Red accent (errors) |
| `--accent-blue` | `#58a6ff` | Blue accent (info) |
| `--accent-purple` | `#bc8cff` | Purple accent |
| `--text` | `#aab4c5` | Body text |
| `--text-bright` | `#e2e8f2` | Headings, emphasis |
| `--text-dim` | `#6b7a8f` | Labels, captions |
| `--border` | `#1a2236` | Subtle borders |
| `--border-bright` | `#253048` | Prominent borders |
| `--code-bg` | `#0a1018` | Code block backgrounds |

### Typography

Phosphor uses three font families loaded from Google Fonts:

| Font | Use |
| --- | --- |
| **Chakra Petch** | Headings, labels, navigation |
| **Nunito Sans** | Body text |
| **JetBrains Mono** | Code, terminal, monospace elements |

### Customizing Colors

To customize the theme, edit the CSS variables in `theme/style.css` at your Phosphor installation. For example, to change the accent color from teal to blue:

```
:root {
  --accent: #58a6ff;
  --accent-dim: #4488cc;
  --accent-glow: rgba(88, 166, 255, 0.08);
  --accent-glow-strong: rgba(88, 166, 255, 0.18);
}
```

:::warn Theme changes are global
Editing `theme/style.css` in the Phosphor installation affects all sites built with that installation. If you need different themes per project, consider maintaining separate Phosphor installations or copying the theme files into your project.
:::

### Custom Favicon

You can use a custom favicon by setting the `favicon` field in `docs.yaml`:

```
site:
  favicon: "my-favicon.svg"
```

Place the favicon file in your project directory (next to `docs.yaml`). SVG format is recommended. If no custom favicon is specified, Phosphor uses its default gradient favicon.

### Layout Breakpoints

| Width | Layout |
| --- | --- |
| 1440px+ | Full layout: sidebar + content + wide sticky TOC |
| 1200px - 1439px | Sidebar + content + compact sticky TOC |
| 901px - 1199px | Sidebar + content (TOC hidden) |
| 900px and below | Mobile layout: hamburger menu + full-width content |
| 480px and below | Compact mobile: stacked hero buttons, smaller grids |
