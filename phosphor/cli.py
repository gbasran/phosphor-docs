#!/usr/bin/env python3
"""CLI entry point for phosphor-docs.

Commands:
    phosphor build [dir]   — Build the documentation site
    phosphor init [dir]    — Scaffold a new docs project
    phosphor serve [dir]   — Preview with local HTTP server
"""

import argparse
import http.server
import os
import re
import shutil
import subprocess
import sys


def _detect_git_info(directory):
    """Detect GitHub repo info from git remote origin.

    Returns dict with title, tagline, logo_text, github URL,
    or empty dict if not a git repo or no remote found.
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return {}

        url = result.stdout.strip()
        if not url:
            return {}

        # Parse repo name from various URL formats:
        #   https://github.com/user/repo-name.git
        #   git@github.com:user/repo-name.git
        #   https://github.com/user/repo-name
        m = re.search(r"[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
        if not m:
            return {}

        owner = m.group(1)
        repo = m.group(2)

        # Build the HTTPS GitHub URL
        github_url = f"https://github.com/{owner}/{repo}"

        # Title: repo name with hyphens replaced and title-cased
        title = repo.replace("-", " ").replace("_", " ").title()

        # Tagline: ~/repo-name
        tagline = f"~/{repo}"

        # Logo text: first two chars of repo name, uppercase
        logo_text = repo.replace("-", "").replace("_", "")[:2].upper()

        return {
            "title": title,
            "tagline": tagline,
            "logo_text": logo_text,
            "github": github_url,
        }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {}


def cmd_build(args):
    """Build the documentation site."""
    from . import build as build_mod

    project_dir = args.dir or "."
    print(f"Building site from {os.path.abspath(project_dir)}...")
    try:
        build_mod.build(project_dir)
    except Exception as e:
        print(f"Error: Build failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_init(args):
    """Scaffold a new docs project."""
    target_dir = args.dir or "."
    target_dir = os.path.abspath(target_dir)

    phosphor_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    examples_dir = os.path.join(phosphor_root, "examples")

    if not os.path.isdir(examples_dir):
        print(f"Error: examples/ directory not found at {examples_dir}", file=sys.stderr)
        print("Phosphor installation may be incomplete.", file=sys.stderr)
        sys.exit(1)

    # Create pages directory
    pages_dir = os.path.join(target_dir, "pages")
    try:
        os.makedirs(pages_dir, exist_ok=True)
    except OSError as e:
        print(f"Error: cannot create pages directory: {e}", file=sys.stderr)
        sys.exit(1)

    # Detect git info for auto-populating config
    # Walk up from target_dir to find a git repo
    git_info = _detect_git_info(target_dir)
    if not git_info:
        # Try parent directories (target might be docs/ inside a repo)
        parent = os.path.dirname(target_dir)
        if parent != target_dir:
            git_info = _detect_git_info(parent)

    # Copy and customize config
    config_src = os.path.join(examples_dir, "docs.yaml")
    dest = os.path.join(target_dir, "docs.yaml")
    if not os.path.exists(dest):
        if os.path.exists(config_src):
            if git_info:
                # Read template and substitute with detected values
                with open(config_src, "r") as f:
                    config_content = f.read()
                config_content = config_content.replace(
                    'title: "My Project Docs"',
                    f'title: "{git_info["title"]}"',
                )
                config_content = config_content.replace(
                    'tagline: "~/my-project"',
                    f'tagline: "{git_info["tagline"]}"',
                )
                config_content = config_content.replace(
                    'logo_text: "MP"',
                    f'logo_text: "{git_info["logo_text"]}"',
                )
                config_content = config_content.replace(
                    'github: "https://github.com/user/my-project"',
                    f'github: "{git_info["github"]}"',
                )
                with open(dest, "w") as f:
                    f.write(config_content)
                print(f"  Created: docs.yaml (auto-detected from git: {git_info['title']})")
            else:
                shutil.copy2(config_src, dest)
                print(f"  Created: docs.yaml")
    else:
        print(f"  Skipped: docs.yaml (already exists)")

    example_pages = os.path.join(examples_dir, "pages")
    if os.path.exists(example_pages):
        for fname in os.listdir(example_pages):
            src = os.path.join(example_pages, fname)
            dest = os.path.join(pages_dir, fname)
            if not os.path.exists(dest):
                shutil.copy2(src, dest)
                print(f"  Created: pages/{fname}")
            else:
                print(f"  Skipped: pages/{fname} (already exists)")

    print(f"\nDocs project initialized in {target_dir}/")
    print("Next steps:")
    print("  1. Edit docs.yaml to configure your site")
    print("  2. Edit pages/*.md to write your content")
    print("  3. Run: phosphor build")


def cmd_serve(args):
    """Start a local HTTP server for preview."""
    from . import build as build_mod

    project_dir = args.dir or "."
    site_dir = os.path.join(os.path.abspath(project_dir), "_site")

    port = args.port or 8000
    if not (1 <= port <= 65535):
        print(f"Error: port must be between 1 and 65535, got {port}", file=sys.stderr)
        sys.exit(1)

    # Build first
    print(f"Building site from {os.path.abspath(project_dir)}...")
    try:
        build_mod.build(project_dir)
    except Exception as e:
        print(f"Error: Build failed: {e}", file=sys.stderr)
        sys.exit(1)
    print()

    if not os.path.exists(site_dir):
        print("Error: _site/ directory not found. Build failed?", file=sys.stderr)
        sys.exit(1)

    print(f"Serving at http://localhost:{port}")
    print("Press Ctrl+C to stop.\n")

    os.chdir(site_dir)

    class _Handler(http.server.SimpleHTTPRequestHandler):
        # Add SVG MIME type
        extensions_map = {
            **http.server.SimpleHTTPRequestHandler.extensions_map,
            ".svg": "image/svg+xml",
        }

        def log_message(self, fmt, *a):
            print(f"  {a[0]} {a[1]}")

    try:
        server = http.server.HTTPServer(("", port), _Handler)
    except OSError as e:
        if "Address already in use" in str(e) or "address already in use" in str(e):
            print(f"Error: port {port} is already in use. Try a different port with -p.", file=sys.stderr)
        else:
            print(f"Error: cannot start server: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


def main():
    parser = argparse.ArgumentParser(
        prog="phosphor",
        description="Phosphor — Static documentation site generator",
    )
    subparsers = parser.add_subparsers(dest="command")

    # build
    build_parser = subparsers.add_parser("build", help="Build the documentation site")
    build_parser.add_argument("dir", nargs="?", default=".", help="Project directory (default: .)")

    # init
    init_parser = subparsers.add_parser("init", help="Scaffold a new docs project")
    init_parser.add_argument("dir", nargs="?", default=".", help="Target directory (default: .)")

    # serve
    serve_parser = subparsers.add_parser("serve", help="Preview with local HTTP server")
    serve_parser.add_argument("dir", nargs="?", default=".", help="Project directory (default: .)")
    serve_parser.add_argument("-p", "--port", type=int, default=8000, help="Port number (default: 8000)")

    args = parser.parse_args()

    if args.command == "build":
        cmd_build(args)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "serve":
        cmd_serve(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
