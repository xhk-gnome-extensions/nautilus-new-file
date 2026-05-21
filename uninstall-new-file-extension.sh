#!/bin/bash
set -e

echo "Uninstalling Nautilus New File Extension..."

EXTENSION_FILE="$HOME/.local/share/nautilus-python/extensions/nautilus_new_file_ext.py"

if [ -f "$EXTENSION_FILE" ]; then
    rm "$EXTENSION_FILE"
    echo "Extension removed: $EXTENSION_FILE"
else
    echo "Extension not found: $EXTENSION_FILE"
fi

# Restart Nautilus
echo ""
echo "Restarting Nautilus..."
nautilus -q 2>/dev/null || true

echo ""
echo "✅ Uninstallation complete!"
