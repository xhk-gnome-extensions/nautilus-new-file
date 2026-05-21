#!/bin/bash
set -e

echo "Installing Nautilus New File Extension..."

# Create extension directory if not exists
EXTENSION_DIR="$HOME/.local/share/nautilus-python/extensions"
mkdir -p "$EXTENSION_DIR"

# Copy extension
cp nautilus_new_file_ext.py "$EXTENSION_DIR/"
chmod +x "$EXTENSION_DIR/nautilus_new_file_ext.py"

echo "Extension installed to: $EXTENSION_DIR/nautilus_new_file_ext.py"

# Check if nautilus-python is installed (try both version 3 and 4)
NAUTILUS_OK=false

if python3 -c "import gi; gi.require_version('Nautilus', '3.0')" &> /dev/null; then
    echo "✓ Nautilus 3.0 bindings found"
    NAUTILUS_OK=true
elif python3 -c "import gi; gi.require_version('Nautilus', '4.0')" &> /dev/null; then
    echo "✓ Nautilus 4.0 bindings found"
    NAUTILUS_OK=true
fi

if [ "$NAUTILUS_OK" = false ]; then
    echo ""
    echo "⚠️  Warning: nautilus-python not found!"
    echo "Installing required packages..."
    
    # Try to install for Nautilus 3.0 first (more common)
    if sudo apt install -y python3-nautilus gir1.2-nautilus-3.0; then
        echo "✓ Installed Nautilus 3.0 packages"
    else
        echo "Trying Nautilus 4.0 packages..."
        sudo apt install -y python3-nautilus gir1.2-nautilus-4.0 || true
    fi
fi

# Restart Nautilus
echo ""
echo "Restarting Nautilus..."
nautilus -q 2>/dev/null || true
sleep 1

echo ""
echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  1. Open Nautilus (Files)"
echo "  2. Right-click on empty space in any folder"
echo "  3. Select '📄 New File' → Choose file type"
echo ""
echo "To uninstall:"
echo "  rm $EXTENSION_DIR/nautilus_new_file_ext.py"
echo "  nautilus -q"
