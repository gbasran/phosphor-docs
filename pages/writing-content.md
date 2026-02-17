## Standard Markdown

Phosphor supports all standard Markdown syntax you already know. Every page is a `.md` file in your `pages/` directory.

### Headings

Use `##` for sections and `###` for subsections. Phosphor uses these to generate the sidebar table of contents and the search index.

- `## Section` — creates a styled section with accent rule, auto-generates an ID for anchor links
- `### Subsection` — creates a subsection heading with auto-generated ID
- `#### Minor heading` — smaller heading for subdivisions within a subsection

:::warn h1 headings are reserved
Don't use `# Heading` (single `#`) in your pages. The h1 is reserved for the hero section title. Start your content with `##` headings.
:::

### Text Formatting

Standard inline formatting works as expected:

- `**bold text**` renders as **bold text**
- `*italic text*` renders as *italic text*
- `` `inline code` `` renders as `inline code`

### Links

Standard Markdown links work for both internal and external targets:

- `[Link Text](https://example.com)` — external link
- `[Other Page](other-page.html#section)` — internal link (use `.html` extension, not `.md`)

:::tip Internal links use .html
When linking between your docs pages, use the `.html` extension since that's what the built output uses. For example: `[Getting Started](getting-started.html#quickstart)`.
:::

### Images

```
![Alt text](path/to/image.png)
```

Place images in your `pages/` directory or reference external URLs.

### Lists

Unordered lists use `-` or `*`:

- First item
- Second item
- Third item with `inline code`

Ordered lists use numbers:

1. Step one
2. Step two
3. Step three

### Code Blocks

Standard fenced code blocks render with the Phosphor monospace styling:

```
function hello() {
  console.log("Hello from Phosphor");
}
```

### Tables

Standard Markdown tables render with the Phosphor table styling:

| Feature | Status | Notes |
| --- | --- | --- |
| Sidebar navigation | Complete | Auto-generated from docs.yaml |
| Search | Complete | Fuzzy search with autocomplete |
| Table of contents | Complete | Scroll spy on wide screens |
| Mobile layout | Complete | Responsive sidebar drawer |

### Horizontal Rules

Use `---` on its own line to create a horizontal divider:

---

The divider above was created with three dashes.

## Components

Phosphor extends Markdown with rich components using the `:::` fenced block syntax. These render as styled HTML elements that match the Terminal Noir theme.

### Callouts

Callouts highlight important information. Three types are available:

:::tip Tip callout
Use `:::tip` for helpful suggestions, best practices, and recommendations. The title text goes on the same line as the opening `:::tip`.
:::

:::info Informational callout
Use `:::info` for neutral supplementary information, context, or explanations.
:::

:::warn Warning callout
Use `:::warn` for warnings, caveats, breaking changes, or anything the reader should be careful about.
:::

#### Callout Syntax

```
:::tip Your Title Here
The body text goes on subsequent lines.
You can use **bold**, *italic*, and `code` in the body.
:::
```

The type can be `tip` (teal), `info` (blue), or `warn` (amber). The first word after `:::` is the type, everything after it on that line is the title.

### Terminal Blocks

Terminal blocks render as realistic terminal windows with colored dots, a title bar, and syntax-colored output. Lines starting with `$` are commands, lines starting with `#` are comments, and everything else is output.

```terminal
$ cd ~/my-project
$ phosphor build
  Built: index.html
  Built: getting-started.html

Site built to _site/
  2 pages, 2 HTML files
# Build complete!
```

#### Terminal Syntax

Use a fenced code block with the `terminal` language identifier:

````
```terminal
$ command-here
Output appears as dimmed text
# This is a comment
$ another-command --with-flags
```
````

Line types:

| Prefix | Rendering |
| --- | --- |
| `$ ` | Green prompt + bright command text |
| `# ` | Dimmed italic comment |
| (anything else) | Dimmed output text |

### Cards

Cards display features, concepts, or options in a responsive grid. Each card has an icon, color accent, title, and description.

:::cards
::card{icon="code" color="teal" title="Code Blocks"}
Standard fenced code blocks with monospace font and dark background.
::

::card{icon="terminal" color="amber" title="Terminal Blocks"}
Realistic terminal windows with prompt coloring and output styling.
::

::card{icon="message-square" color="blue" title="Callouts"}
Tip, info, and warning boxes for highlighting important content.
::

::card{icon="git-branch" color="purple" title="Pipeline Diagrams"}
Visual stage-by-stage flow diagrams with numbered nodes and arrows.
::
:::

#### Card Syntax

```
:::cards
::card{icon="icon-name" color="teal" title="Card Title"}
Description text. Supports **bold** and `code`.
::

::card{icon="another-icon" color="amber" title="Another Card"}
Another description.
::
:::
```

#### Available Colors

| Color | CSS Variable | Use For |
| --- | --- | --- |
| `teal` | `--accent` (#22d3a7) | Primary features, positive items |
| `amber` | `--accent-warm` (#f0a500) | Warnings, important items |
| `blue` | `--accent-blue` (#58a6ff) | Informational, neutral items |
| `purple` | `--accent-purple` (#bc8cff) | Special features, unique items |
| `red` | `--accent-red` (#f47067) | Critical items, errors |

#### Available Icons

Phosphor uses the Lucide icon library. Any Lucide icon name works in the `icon` attribute. Common ones for docs:

| Icon Name | Use For |
| --- | --- |
| `file-text` | Documentation, files |
| `terminal` | CLI, commands |
| `code` | Source code, programming |
| `settings` | Configuration |
| `search` | Search features |
| `zap` | Quick start, performance |
| `rocket` | Deployment, launch |
| `shield` | Security |
| `puzzle` | Components, plugins |
| `git-branch` | Version control |
| `database` | Data, storage |
| `globe` | Web, network |
| `bot` | AI, automation |
| `sparkles` | Features, highlights |

Full list at [lucide.dev/icons](https://lucide.dev/icons).

### Decision Grids

Decision grids help users pick the right option based on their situation. They render as styled tables with hover highlighting.

:::decision-grid
| I have... | I want to... | Use |
| A new project | Generate docs from scratch | `phosphor init` then edit pages |
| An existing repo | Add docs to it | `phosphor init docs/` in the repo |
| Built docs locally | Deploy them | Copy `_site/` to your web server |
| Broken build output | Debug the issue | Check `docs.yaml` syntax and page filenames |
:::

#### Decision Grid Syntax

```
:::decision-grid
| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Row 1 cell | Row 1 cell | Row 1 cell |
| Row 2 cell | Row 2 cell | Row 2 cell |
:::
```

The content inside is a standard Markdown table. The `:::decision-grid` wrapper applies the styled grid layout instead of a regular table.

### Command Blocks

Command blocks document CLI commands with a styled header, usage line, and flag reference table. Ideal for tool documentation.

:::command{title="phosphor build" usage="phosphor build [directory]"}
::flag{name="directory" short="dir"}
Path to the project directory containing `docs.yaml`. Defaults to the current directory.
::
:::

:::command{title="phosphor serve" usage="phosphor serve [directory] [-p PORT]"}
::flag{name="directory" short="dir"}
Path to the project directory. Defaults to the current directory.
::
::flag{name="--port" short="-p"}
Port number for the local HTTP server. Defaults to 8000.
::
:::

#### Command Block Syntax

```
:::command{title="command-name" usage="command-name [args] [flags]"}
::flag{name="--flag-name" short="-f"}
Description of what this flag does.
::

::flag{name="--another" short="-a"}
Another flag description.
::
:::
```

The `title` attribute sets the command name in the header. The `usage` attribute sets the usage line. Each `::flag` child has a `name` (long flag) and optional `short` (short flag).

### Accordions

Accordions hide content behind a clickable summary. Useful for FAQs, optional details, or long reference sections that would clutter the page.

:::accordion{title="What Markdown syntax does Phosphor support?"}
All standard Markdown: headings, paragraphs, bold, italic, inline code, links, images, lists (ordered and unordered), code blocks, tables, and horizontal rules. Plus the extended component syntax documented on this page.
:::

:::accordion{title="Can I nest components inside accordions?"}
Yes. Accordion bodies support all standard Markdown formatting including code blocks, lists, bold, italic, and inline code. The body content is processed as regular Markdown.
:::

:::accordion{title="How do accordions render?"}
Accordions use the HTML `<details>` and `<summary>` elements with Phosphor styling. They're accessible, work without JavaScript, and animate smoothly.
:::

#### Accordion Syntax

```
:::accordion{title="Visible summary text"}
Hidden content that appears when the user clicks.
Supports **Markdown** formatting and `code`.
:::
```

### Pipeline Diagrams

Pipelines visualize multi-step processes as numbered stage nodes connected by arrows.

:::pipeline
Plan -> Write -> Build -> Test -> Deploy
:::

#### Pipeline Syntax

```
:::pipeline
Stage 1 -> Stage 2 -> Stage 3 -> Stage 4
:::
```

Stages are separated by `->`. Each stage gets a numbered node (01, 02, 03...) and they're connected with arrow icons. The pipeline scrolls horizontally if it overflows on narrow screens.

### Hero Sections

The hero section is typically used on the homepage (`index.md`) to create a prominent landing area with a title, description, and action buttons.

#### Hero Syntax

```
:::hero{badge="Badge Text"}
# Main Title With **Accent Words**
Description paragraph below the title.

[Primary Button](url){.primary}
[Secondary Button](url){.secondary}
:::
```

Key details:

- The `badge` attribute creates a small pill label above the title
- The `# heading` becomes the hero title (h1)
- Words wrapped in `**double asterisks**` get the teal accent color
- Lines starting with `[` become action buttons
- `{.primary}` makes a teal filled button, `{.secondary}` makes an outlined button
- Regular text lines become description paragraphs

## Page Structure

### Recommended Page Layout

Every page should start with either a `:::hero` block (for the homepage) or a `## Section` heading. Here's the recommended structure:

```
## First Section

Introductory paragraph for this section.

### Subsection

More detailed content here.

## Second Section

Another section with its own content.

### Another Subsection

And so on.
```

### Section IDs

Phosphor automatically generates URL-friendly IDs from your headings:

| Heading | Generated ID |
| --- | --- |
| `## Getting Started` | `getting-started` |
| `### CLI Commands` | `cli-commands` |
| `## FAQ & Troubleshooting` | `faq--troubleshooting` |

These IDs are used for:

- Sidebar navigation anchor links
- Table of contents links
- Direct URL linking (`page.html#section-id`)
- Search result navigation

### Table of Contents

The table of contents (TOC) appears automatically on wide screens (1200px+) as a sticky sidebar on the left side of the content area. It lists all `##` and `###` headings on the current page with scroll spy highlighting.

You don't need to do anything to enable it — Phosphor generates it automatically from your headings.

### Search

Search is also fully automatic. When you build your site, Phosphor extracts every heading and the surrounding paragraph content, generates a search index, and injects it into the search JavaScript. Users can:

- Click the search box in the sidebar
- Press `/` anywhere on the page to focus search
- Type to see instant results with fuzzy matching
- Navigate results with arrow keys
- Press Enter to jump to the result

### Multi-Page Sites

For sites with multiple pages, structure your content across separate `.md` files. Each page becomes its own HTML file. Use the `nav` section in `docs.yaml` to define the sidebar navigation, and link between pages using `.html` extensions:

```
[See the reference](reference.html#commands)
```
