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

### How Theming Works

Add a `theme:` section to your project's `docs.yaml` to override any color variable. Phosphor injects your overrides as a `<style>` block after the base stylesheet, so they take precedence without modifying the Phosphor installation. Each project can have its own color scheme.

```
theme:
  accent: "#f97316"        # Your primary color
  accent_dim: "#ea580c"    # Hover/darker variant
  bg_deep: "#09080c"       # Page background
  # ... any other keys you want to change
```

All keys are optional. Any variable you don't override uses the Terminal Noir default.

### The Color System

Phosphor's theme is built on **five layers of color**. Understanding these layers is the key to building a cohesive palette.

#### 1. Backgrounds (depth)

Four shades that create visual depth through layering. Each level is slightly lighter than the one below it.

| Key | Default | Used For |
| --- | --- | --- |
| `bg_deep` | `#080c14` | Page body, deepest layer |
| `bg_surface` | `#0e1320` | Sidebar, cards, panels |
| `bg_raised` | `#151c2c` | Buttons, table headers, code bar |
| `bg_hover` | `#1a2338` | Hover states on raised elements |
| `code_bg` | `#0a1018` | Code block interiors |

:::tip Picking backgrounds
Start with your deepest color (`bg_deep`), then create each layer by adding 5-8% lightness. Add a subtle hue tint to match your accent — pure grays look flat. For a purple theme, tint toward `#0e0822`. For amber, tint toward `#12101a`.
:::

#### 2. Accent Colors (identity)

The primary accent defines your site's visual identity. It's used for links, active nav items, buttons, hero highlights, the logo icon, and the scrollbar.

| Key | Default | Used For |
| --- | --- | --- |
| `accent` | `#22d3a7` | Primary links, active states, highlights |
| `accent_dim` | `#1a9e7e` | Hover state (slightly darker) |
| `accent_glow` | `rgba(34,211,167,0.08)` | Subtle overlay on hover backgrounds |
| `accent_glow_strong` | `rgba(34,211,167,0.18)` | Stronger overlay on active states |

:::info The glow values
`accent_glow` and `accent_glow_strong` should use the same RGB as your `accent` but with low alpha (0.08–0.10 for glow, 0.18–0.22 for strong). These create the subtle background tinting on hover and active states.
:::

#### 3. Semantic Colors (meaning)

These give specific meaning to UI elements — callouts, warnings, errors, code syntax.

| Key | Default | Used For |
| --- | --- | --- |
| `accent_warm` | `#f0a500` | `:::tip` and `:::warn` callouts, flag markers |
| `accent_warm_dim` | `rgba(240,165,0,0.08)` | Warm callout backgrounds |
| `accent_red` | `#f47067` | Error states, `:::warn` borders |
| `accent_blue` | `#58a6ff` | `:::info` callouts, inline code |
| `accent_purple` | `#bc8cff` | Code syntax strings |

#### 4. Text (readability)

Three tiers of text contrast. Keep sufficient contrast against your backgrounds for readability.

| Key | Default | Used For |
| --- | --- | --- |
| `text` | `#aab4c5` | Body paragraphs, table cells |
| `text_bright` | `#e2e8f2` | Headings, emphasis, bold |
| `text_dim` | `#6b7a8f` | Labels, captions, timestamps |

#### 5. Borders (structure)

Two levels of border visibility for separating content areas.

| Key | Default | Used For |
| --- | --- | --- |
| `border` | `#1a2236` | Subtle dividers, card borders |
| `border_bright` | `#253048` | Table borders, prominent separators |

### Typography

Phosphor uses three font families loaded from Google Fonts:

| Font | Use |
| --- | --- |
| **Chakra Petch** | Headings, labels, navigation |
| **Nunito Sans** | Body text |
| **JetBrains Mono** | Code, terminal, monospace elements |

### Building a Custom Palette

Here's a step-by-step walkthrough for creating a theme from scratch. We'll use the **Avengers: Endgame** palette as the example — deep space purples with violet accents.

#### Step 1: Choose Your Accent Color

Pick one dominant color. This is the personality of your site. Everything else derives from it.

For Endgame, the Power Stone violet: **`#8b5cf6`**

```
theme:
  accent: "#8b5cf6"
```

#### Step 2: Create Accent Variants

Derive the dim, glow, and glow-strong values from your accent:

- **Dim**: Drop the lightness ~15%. `#8b5cf6` → `#7c3aed`
- **Glow**: Same RGB, alpha 0.10. `rgba(139, 92, 246, 0.10)`
- **Glow strong**: Same RGB, alpha 0.20-0.22. `rgba(139, 92, 246, 0.22)`

```
theme:
  accent: "#8b5cf6"
  accent_dim: "#7c3aed"
  accent_glow: "rgba(139, 92, 246, 0.10)"
  accent_glow_strong: "rgba(139, 92, 246, 0.22)"
```

#### Step 3: Set Semantic Colors

Choose colors that complement your accent without clashing. For a purple theme, shift the warm accent toward lavender and the red toward pink:

```
  accent_warm: "#c084fc"
  accent_warm_dim: "rgba(192, 132, 252, 0.10)"
  accent_red: "#f472b6"
  accent_blue: "#818cf8"
  accent_purple: "#c084fc"
```

:::tip Color harmony
Keep semantic colors in the same temperature family as your accent. A purple accent pairs well with pink reds and indigo blues. An orange accent pairs better with warm yellows and coral reds.
:::

#### Step 4: Build Your Background Stack

Start from near-black with a hue tint matching your accent. For purple: push backgrounds toward blue-violet.

```
  bg_deep: "#070312"
  bg_surface: "#0e0822"
  bg_raised: "#160f2e"
  bg_hover: "#1e1438"
  code_bg: "#080418"
```

Each step adds roughly 5-8% lightness while keeping the purple undertone.

#### Step 5: Match Text and Borders

Tint your text and borders to match the background hue so nothing looks out of place:

```
  text: "#b4b0c8"
  text_bright: "#e8e4f0"
  text_dim: "#6e6890"
  border: "#1c1535"
  border_bright: "#2a2048"
```

#### Complete Endgame Theme

Putting it all together:

```
theme:
  accent: "#8b5cf6"
  accent_dim: "#7c3aed"
  accent_glow: "rgba(139, 92, 246, 0.10)"
  accent_glow_strong: "rgba(139, 92, 246, 0.22)"
  accent_warm: "#c084fc"
  accent_warm_dim: "rgba(192, 132, 252, 0.10)"
  accent_red: "#f472b6"
  accent_blue: "#818cf8"
  accent_purple: "#c084fc"
  bg_deep: "#070312"
  bg_surface: "#0e0822"
  bg_raised: "#160f2e"
  bg_hover: "#1e1438"
  code_bg: "#080418"
  text: "#b4b0c8"
  text_bright: "#e8e4f0"
  text_dim: "#6e6890"
  border: "#1c1535"
  border_bright: "#2a2048"
```

This theme is used in production by the [AI Agents HQ docs](https://gbasran.github.io/ai-agents-hq).

### More Example Palettes

#### Ember (orange accent, purple-tinted backgrounds)

A warm, energetic palette. Orange is uncommon in developer docs, which makes it stand out. This is the theme used by the Phosphor docs site itself.

```
theme:
  accent: "#f97316"
  accent_dim: "#ea580c"
  accent_glow: "rgba(249, 115, 22, 0.10)"
  accent_glow_strong: "rgba(249, 115, 22, 0.22)"
  accent_warm: "#facc15"
  accent_warm_dim: "rgba(250, 204, 21, 0.10)"
  accent_red: "#f43f5e"
  accent_blue: "#38bdf8"
  accent_purple: "#c084fc"
  bg_deep: "#09080c"
  bg_surface: "#12101a"
  bg_raised: "#1c1828"
  bg_hover: "#252034"
  code_bg: "#0c0a12"
  text: "#b8b2c8"
  text_bright: "#ede9f5"
  text_dim: "#7a7290"
  border: "#1e1a2e"
  border_bright: "#2e2842"
```

#### Ocean (blue accent, cool backgrounds)

Clean and professional. Good for corporate or technical documentation.

```
theme:
  accent: "#3b82f6"
  accent_dim: "#2563eb"
  accent_glow: "rgba(59, 130, 246, 0.10)"
  accent_glow_strong: "rgba(59, 130, 246, 0.20)"
  accent_warm: "#f59e0b"
  accent_warm_dim: "rgba(245, 158, 11, 0.10)"
  accent_red: "#ef4444"
  accent_blue: "#06b6d4"
  accent_purple: "#8b5cf6"
```

#### Crimson (red accent, warm backgrounds)

Bold and high-energy. Works well for gaming or creative project docs.

```
theme:
  accent: "#ef4444"
  accent_dim: "#dc2626"
  accent_glow: "rgba(239, 68, 68, 0.10)"
  accent_glow_strong: "rgba(239, 68, 68, 0.20)"
  accent_warm: "#f59e0b"
  accent_warm_dim: "rgba(245, 158, 11, 0.10)"
  accent_blue: "#38bdf8"
  accent_purple: "#a78bfa"
  bg_deep: "#0c0606"
  bg_surface: "#160e0e"
  bg_raised: "#201616"
  bg_hover: "#2c1e1e"
  code_bg: "#0e0808"
  text: "#c8b8b8"
  text_bright: "#f0e8e8"
  text_dim: "#8a7070"
  border: "#261a1a"
  border_bright: "#382828"
```

#### Minimal Override

You don't need to override everything. To just change the accent from teal to blue and keep all other defaults:

```
theme:
  accent: "#3b82f6"
  accent_dim: "#2563eb"
  accent_glow: "rgba(59, 130, 246, 0.08)"
  accent_glow_strong: "rgba(59, 130, 246, 0.18)"
```

:::tip Per-project theming
The `theme:` config is per-project — each site can have its own color scheme without modifying the Phosphor installation. The base Terminal Noir theme is used for any variable you don't override.
:::

### Favicon

The default favicon is **automatically themed** — it uses your `accent` and `accent_dim` colors for the gradient background, `bg_deep` for the text color, and `logo_text` for the letters. No configuration needed; just set your theme colors and the favicon matches.

To use a completely custom favicon instead, set the `favicon` field in `docs.yaml`:

```
site:
  favicon: "my-favicon.svg"
```

Place the favicon file in your project directory (next to `docs.yaml`). SVG format is recommended. Custom favicons are copied as-is and not themed.

### Layout Breakpoints

| Width | Layout |
| --- | --- |
| 1440px+ | Full layout: sidebar + content + wide sticky TOC |
| 1200px - 1439px | Sidebar + content + compact sticky TOC |
| 901px - 1199px | Sidebar + content (TOC hidden) |
| 900px and below | Mobile layout: hamburger menu + full-width content |
| 480px and below | Compact mobile: stacked hero buttons, smaller grids |
