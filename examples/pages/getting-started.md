## Getting Started

Get up and running with Phosphor in under 5 minutes.

### Prerequisites

- Python 3.8+
- PyYAML (`pip install pyyaml`)

### Installation

```terminal
$ git clone https://github.com/user/phosphor-docs
$ cd phosphor-docs
$ ./install.sh
```

### Create Your First Site

```terminal
$ mkdir my-docs && cd my-docs
$ phosphor init
  Created: docs.yaml
  Created: pages/index.md
  Created: pages/getting-started.md
$ phosphor build
  Built: index.html
  Built: getting-started.html
```

:::info Project structure
After running `phosphor init`, your directory will contain:
- `docs.yaml` — Site configuration
- `pages/` — Markdown content files
:::

### Configuration

Edit `docs.yaml` to configure your site:

```terminal
$ cat docs.yaml
```

The config file has three sections:

1. **site** — Title, tagline, logo, GitHub link
2. **nav** — Sidebar navigation groups and items
3. **pages** — Build order for your Markdown files

### Writing Content

Phosphor extends standard Markdown with custom components:

:::accordion{title="Callouts (tip, info, warn)"}
Use `:::tip`, `:::info`, or `:::warn` to create callout boxes:

```
:::tip Title
Your content here.
:::
```
:::

:::accordion{title="Cards"}
Use `:::cards` with `::card` children:

```
:::cards
::card{icon="star" color="teal" title="Feature"}
Description here.
::
:::
```
:::

:::accordion{title="Terminal Blocks"}
Use triple backticks with `terminal` language:

````
```terminal
$ your-command here
Output appears here
```
````
:::

:::warn Important
Always run `phosphor build` after making changes to see updates in `_site/`.
:::

## Commands

### phosphor init

:::command{title="phosphor init" usage="phosphor init [directory]"}
::flag{name="directory" short="dir"}
Target directory for the new docs project. Defaults to current directory.
::
:::

### phosphor build

:::command{title="phosphor build" usage="phosphor build [directory]"}
::flag{name="directory" short="dir"}
Project directory containing docs.yaml. Defaults to current directory.
::
:::

### phosphor serve

:::command{title="phosphor serve" usage="phosphor serve [directory] [-p PORT]"}
::flag{name="directory" short="dir"}
Project directory containing docs.yaml. Defaults to current directory.
::
::flag{name="--port" short="-p"}
Port number for the local server. Defaults to 8000.
::
:::
