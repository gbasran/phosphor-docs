## Changelog

Release history for Phosphor Docs. Each entry documents what changed and why.

## v0.2.0 — Security Hardening & Robustness

Released 2026-02-18.

A comprehensive security and stability audit uncovered 40+ issues across the parser, build system, config loader, CLI, and renderer. All have been fixed in this release.

### Security Fixes

:::warn Critical — update recommended
These fixes address real security vulnerabilities. If you accept user-contributed content (Markdown files, config values), update immediately.
:::

- **XSS in URLs**: All links, images, and hero buttons now escape URLs and reject `javascript:` URIs
- **Path traversal in build**: Custom favicon paths and page file paths are validated to stay within the project directory. Paths containing `../` that escape the project are rejected
- **SVG injection in favicon**: Theme color values injected into auto-generated favicons are now validated against safe patterns (`#hex` or `rgba()`)

### Parser Fixes

- **Code fences inside `:::` blocks**: A `:::` delimiter inside a code fence (` ``` `) is no longer treated as a component close. You can now safely show `:::` syntax in code examples within callouts, accordions, and other components
- **Unclosed `:::` blocks**: If a `:::tip` or other component block is never closed, the parser now warns to stderr and renders the content instead of silently consuming the rest of the file
- **Hyphenated component types**: The depth tracking regex now matches types like `decision-grid` (previously only matched `\w+` which excludes hyphens)
- **Heading regex performance**: Limited a repeating group in heading extraction to prevent potential catastrophic backtracking on malformed HTML
- **Table column padding**: Short table rows are now padded with empty cells to match the header column count, preventing misaligned tables
- **`data-` attribute support**: Component attribute parsing now accepts hyphenated names like `data-x="value"`

### Config & Build Robustness

- **Config type validation**: The config loader now validates that `pages` and `nav` are lists, `site` and `theme` are mappings. Wrong types produce clear error messages instead of downstream crashes
- **Template existence checks**: Missing `base.html` or `search.js` templates produce a clear error instead of an unhandled exception
- **Output directory permissions**: Permission denied errors when cleaning `_site/` are caught and reported clearly
- **Pages directory validation**: The build now checks that `pages/` exists before attempting to read files
- **Non-string theme values**: Integer or null values in the theme config are silently skipped instead of producing invalid CSS

### CLI Improvements

- **Port validation**: `phosphor serve -p` rejects port numbers outside the valid range (1-65535)
- **Port-in-use handling**: If the port is already in use, a friendly error message is shown instead of an unhandled exception
- **Build failure handling**: Build errors during `phosphor serve` and `phosphor build` are caught with a clean error message
- **Init guard**: `phosphor init` checks that the examples directory exists and handles directory creation failures
- **SVG MIME type**: The serve command now serves `.svg` files with the correct `image/svg+xml` content type

### Other

- **PyYAML version pin**: Changed from `>=6.0` to `>=6.0,<7.0` to prevent breaking changes from a future major version
- **install.sh**: Added `$HOME` environment check and chmod error handling

---

## v0.1.0 — Initial Release

Released 2026-02-17.

First public release of Phosphor Docs.

- Extended Markdown parser with 8 component types (callouts, cards, terminal blocks, command blocks, decision grids, accordions, pipelines, hero sections)
- Dark Terminal Noir theme with full CSS variable theming
- Client-side fuzzy search with keyboard navigation
- Auto-themed gradient favicon from accent colors
- `phosphor build`, `phosphor init`, `phosphor serve` CLI commands
- Git auto-detection for `phosphor init`
- GitHub Pages deployment workflow
- Zero dependencies beyond Python 3 and PyYAML
