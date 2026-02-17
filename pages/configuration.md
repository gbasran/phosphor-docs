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

theme:                          # Override any CSS color variable (all optional)
  accent: "#8b5cf6"
  accent_dim: "#7c3aed"
  bg_deep: "#070312"
  # ... see Theming section for all available keys

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

Add a `theme:` section to your project's `docs.yaml` to override any color variable. Overrides are injected as a `<style>` block after the base stylesheet, so they take precedence without modifying the Phosphor installation.

#### Available Theme Keys

| Key | CSS Variable | Default | Description |
| --- | --- | --- | --- |
| `accent` | `--accent` | `#22d3a7` | Primary accent color |
| `accent_dim` | `--accent-dim` | `#1a9e7e` | Accent hover / darker variant |
| `accent_glow` | `--accent-glow` | `rgba(34,211,167,0.08)` | Subtle accent overlay |
| `accent_glow_strong` | `--accent-glow-strong` | `rgba(34,211,167,0.18)` | Stronger accent overlay |
| `accent_warm` | `--accent-warm` | `#f0a500` | Warm accent (warnings, tips) |
| `accent_warm_dim` | `--accent-warm-dim` | `rgba(240,165,0,0.08)` | Subtle warm overlay |
| `accent_red` | `--accent-red` | `#f47067` | Red accent (errors) |
| `accent_blue` | `--accent-blue` | `#58a6ff` | Blue accent (info callouts) |
| `accent_purple` | `--accent-purple` | `#bc8cff` | Purple accent (code syntax) |
| `bg_deep` | `--bg-deep` | `#080c14` | Deepest background (body) |
| `bg_surface` | `--bg-surface` | `#0e1320` | Sidebar, cards, surfaces |
| `bg_raised` | `--bg-raised` | `#151c2c` | Elevated elements |
| `bg_hover` | `--bg-hover` | `#1a2338` | Hover states |
| `code_bg` | `--code-bg` | `#0a1018` | Code block backgrounds |
| `text` | `--text` | `#aab4c5` | Body text |
| `text_bright` | `--text-bright` | `#e2e8f2` | Headings, emphasis |
| `text_dim` | `--text-dim` | `#6b7a8f` | Labels, captions |
| `border` | `--border` | `#1a2236` | Subtle borders |
| `border_bright` | `--border-bright` | `#253048` | Prominent borders |

All keys are optional — only override the ones you want to change.

#### Example: Endgame Theme

A purple-dominant color scheme inspired by Avengers: Endgame. Deep space purples with violet accents.

```
theme:
  bg_deep: "#070312"
  bg_surface: "#0e0822"
  bg_raised: "#160f2e"
  bg_hover: "#1e1438"
  code_bg: "#080418"
  accent: "#8b5cf6"
  accent_dim: "#7c3aed"
  accent_glow: "rgba(139, 92, 246, 0.10)"
  accent_glow_strong: "rgba(139, 92, 246, 0.22)"
  accent_warm: "#c084fc"
  accent_warm_dim: "rgba(192, 132, 252, 0.10)"
  accent_red: "#f472b6"
  accent_blue: "#818cf8"
  accent_purple: "#c084fc"
  text: "#b4b0c8"
  text_bright: "#e8e4f0"
  text_dim: "#6e6890"
  border: "#1c1535"
  border_bright: "#2a2048"
```

#### Example: Minimal Override

You don't need to override everything. To just change the accent from teal to blue:

```
theme:
  accent: "#58a6ff"
  accent_dim: "#4488cc"
  accent_glow: "rgba(88, 166, 255, 0.08)"
  accent_glow_strong: "rgba(88, 166, 255, 0.18)"
```

:::tip Per-project theming
The `theme:` config is per-project — each site can have its own color scheme without modifying the Phosphor installation. The base Terminal Noir theme is used for any variable you don't override.
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
