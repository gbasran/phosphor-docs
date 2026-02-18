#!/usr/bin/env bash
# Phosphor Docs — Install Script
# Creates a `phosphor` command in ~/.local/bin (or ~/bin)

set -e

if [ -z "$HOME" ]; then
    echo "Error: \$HOME is not set" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_PATH="$SCRIPT_DIR/phosphor/cli.py"

# Make CLI executable
chmod +x "$CLI_PATH" || { echo "Error: failed to chmod $CLI_PATH" >&2; exit 1; }

# Determine install location
if [ -d "$HOME/bin" ]; then
    INSTALL_DIR="$HOME/bin"
elif [ -d "$HOME/.local/bin" ]; then
    INSTALL_DIR="$HOME/.local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

# Write wrapper — uses PYTHONPATH so the user's current directory is preserved
# (previously used cd which broke `phosphor serve .` and relative paths)
WRAPPER_PATH="$INSTALL_DIR/phosphor"
cat > "$WRAPPER_PATH" << WRAPPER_EOF
#!/usr/bin/env bash
PHOSPHOR_ROOT="$SCRIPT_DIR"
PYTHONPATH="\$PHOSPHOR_ROOT" exec python3 -m phosphor.cli "\$@"
WRAPPER_EOF

chmod +x "$WRAPPER_PATH"

echo "Phosphor installed to $WRAPPER_PATH"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    # Detect shell config file
    SHELL_RC=""
    if [ -f "$HOME/.zshrc" ] && [ "$(basename "$SHELL")" = "zsh" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        SHELL_RC="$HOME/.bash_profile"
    fi

    if [ -n "$SHELL_RC" ]; then
        # Only add if not already present in the file
        if ! grep -q "$INSTALL_DIR" "$SHELL_RC" 2>/dev/null; then
            echo "" >> "$SHELL_RC"
            echo "# Phosphor docs CLI" >> "$SHELL_RC"
            echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$SHELL_RC"
            echo "Added $INSTALL_DIR to PATH in $SHELL_RC"
            echo "Run 'source $SHELL_RC' or restart your terminal for it to take effect."
        else
            echo "$INSTALL_DIR is already in $SHELL_RC"
        fi
    else
        echo ""
        echo "Warning: Could not find shell config file."
        echo "Add this to your shell profile manually:"
        echo ""
        echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
        echo ""
    fi
fi

echo "Run 'phosphor --help' to get started."
