#!/usr/bin/env bash
# Phosphor Docs — Install Script
# Creates a `phosphor` command in ~/bin or /usr/local/bin

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_PATH="$SCRIPT_DIR/phosphor/cli.py"

# Make CLI executable
chmod +x "$CLI_PATH"

# Create wrapper script
WRAPPER='#!/usr/bin/env bash
PHOSPHOR_ROOT="'"$SCRIPT_DIR"'"
exec python3 -m phosphor.cli "$@"
'

# Determine install location
if [ -d "$HOME/bin" ]; then
    INSTALL_DIR="$HOME/bin"
elif [ -d "$HOME/.local/bin" ]; then
    INSTALL_DIR="$HOME/.local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

# Write wrapper
WRAPPER_PATH="$INSTALL_DIR/phosphor"
cat > "$WRAPPER_PATH" << WRAPPER_EOF
#!/usr/bin/env bash
cd "$SCRIPT_DIR" 2>/dev/null
exec python3 -m phosphor.cli "\$@"
WRAPPER_EOF

chmod +x "$WRAPPER_PATH"

echo "Phosphor installed to $WRAPPER_PATH"

# Check PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "Warning: $INSTALL_DIR is not in your PATH."
    echo "Add this to your ~/.bashrc or ~/.zshrc:"
    echo ""
    echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
    echo ""
fi

echo "Run 'phosphor --help' to get started."
