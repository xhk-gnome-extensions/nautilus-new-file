#!/usr/bin/env python3
"""
Nautilus Extension: Create New File
Adds a context menu to create new files with different extensions
Compatible with Nautilus 3.0 and 4.0
"""

import os
from gi.repository import GObject, Gio
import subprocess

# Try to import Nautilus (support both version 3 and 4)
try:
    import gi
    try:
        gi.require_version('Nautilus', '4.0')
        NAUTILUS_VERSION = 4
    except ValueError:
        gi.require_version('Nautilus', '3.0')
        NAUTILUS_VERSION = 3
    from gi.repository import Nautilus
    
    # Import GTK for dialog
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except Exception as e:
    print(f"Error importing libraries: {e}")
    raise

class NewFileDialog(Gtk.Dialog):
    """Dialog to input filename and select extension"""
    
    def __init__(self, parent, folder_path, default_extension=".txt", default_template=""):
        super().__init__(
            title="New File",
            parent=parent,
            flags=0
        )
        
        self.folder_path = folder_path
        self.default_template = default_template
        self.result_filename = None
        
        # Set dialog size
        self.set_default_size(500, 180)
        self.set_resizable(False)
        
        # Remove default action area
        action_area = self.get_action_area()
        action_area.set_visible(False)
        
        # Create custom header bar
        header = Gtk.HeaderBar()
        header.set_show_close_button(False)
        header.set_title("New File")
        
        # Cancel button (left side)
        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.connect("clicked", lambda b: self.response(Gtk.ResponseType.CANCEL))
        header.pack_start(cancel_btn)
        
        # Create button (right side)
        create_btn = Gtk.Button(label="Create")
        create_btn.get_style_context().add_class("suggested-action")
        create_btn.connect("clicked", lambda b: self.response(Gtk.ResponseType.OK))
        header.pack_end(create_btn)
        
        self.set_titlebar(header)
        
        # Content area
        box = self.get_content_area()
        box.set_border_width(20)
        box.set_spacing(15)
        
        # Filename label
        filename_label = Gtk.Label(label="File name")
        filename_label.set_halign(Gtk.Align.START)
        box.pack_start(filename_label, False, False, 0)
        
        # Filename input (large)
        self.filename_entry = Gtk.Entry()
        self.filename_entry.set_text("new_file")
        self.filename_entry.set_activates_default(True)
        self.filename_entry.connect("changed", self.on_filename_changed)
        self.filename_entry.connect("activate", lambda e: self.response(Gtk.ResponseType.OK))
        # Make entry taller
        self.filename_entry.set_size_request(-1, 40)
        box.pack_start(self.filename_entry, False, False, 0)
        
        # Extension dropdown
        extension_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        extension_label = Gtk.Label(label="Extension:")
        extension_label.set_halign(Gtk.Align.START)
        
        self.extension_combo = Gtk.ComboBoxText()
        self.extensions = [
            (".txt", "Text File"),
            (".json", "JSON File"),
            (".md", "Markdown"),
            (".sh", "Shell Script"),
            (".py", "Python"),
            (".html", "HTML"),
            (".css", "CSS"),
            (".js", "JavaScript"),
            (".xml", "XML"),
            (".yaml", "YAML"),
            ("", "All Files"),
        ]
        
        self.templates = {
            ".txt": "",
            ".json": "{\n  \n}\n",
            ".md": "# New Document\n\n",
            ".sh": "#!/bin/bash\nset -e\n\n",
            ".py": "#!/usr/bin/env python3\n\n",
            ".html": "<!DOCTYPE html>\n<html>\n<head>\n  <title>New Page</title>\n</head>\n<body>\n  \n</body>\n</html>\n",
            ".css": "/* Styles */\n\n",
            ".js": "// JavaScript\n\n",
            ".xml": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\n",
            ".yaml": "# YAML\n\n",
            "": "",
        }
        
        for i, (ext, desc) in enumerate(self.extensions):
            if ext:
                self.extension_combo.append_text(f"{desc} ({ext})")
            else:
                self.extension_combo.append_text(desc)
            
            if ext == default_extension:
                self.extension_combo.set_active(i)
        
        if self.extension_combo.get_active() == -1:
            self.extension_combo.set_active(0)
        
        self.extension_combo.connect("changed", self.on_extension_changed)
        
        extension_box.pack_start(extension_label, False, False, 0)
        extension_box.pack_start(self.extension_combo, True, True, 0)
        box.pack_start(extension_box, False, False, 0)
        
        # Focus on filename entry
        self.filename_entry.grab_focus()
        self.filename_entry.select_region(0, -1)
        
        self.show_all()
    
    def on_filename_changed(self, entry):
        """Update when filename changes"""
        pass
    
    def on_extension_changed(self, combo):
        """Update when extension changes"""
        pass
    
    def get_result(self):
        """Get the filename and template"""
        filename = self.filename_entry.get_text().strip()
        active_idx = self.extension_combo.get_active()
        
        if not filename:
            return None, "", ""
        
        if active_idx >= 0 and active_idx < len(self.extensions):
            ext, _ = self.extensions[active_idx]
            template = self.templates.get(ext, "")
            
            if ext:  # Not "All Files"
                # Remove existing extension if any
                if '.' in filename:
                    base = filename.rsplit('.', 1)[0]
                else:
                    base = filename
                full_name = f"{base}{ext}"
            else:  # All Files - use filename as-is
                full_name = filename
            
            return full_name, template, ext
        
        return None, "", ""


class NewFileExtension(GObject.GObject, Nautilus.MenuProvider):
    
    def get_background_items(self, *args):
        """
        Called when right-clicking on empty space in Nautilus
        """
        # Nautilus 4.0: (self, current_folder)
        # Nautilus 3.0: (self, window, current_folder)
        if NAUTILUS_VERSION >= 4:
            current_folder = args[0] if args else None
        else:
            current_folder = args[1] if len(args) > 1 else None
        
        if not current_folder:
            return []
        
        # Get current directory path
        folder_path = current_folder.get_location().get_path()
        if not folder_path:
            return []
        
        # Create main menu item
        main_item = Nautilus.MenuItem(
            name="NewFileExtension::NewFile",
            label="📄 New File",
            tip="Create a new file",
            icon="document-new"
        )
        
        # Create submenu
        submenu = Nautilus.Menu()
        main_item.set_submenu(submenu)
        
        # Define file types
        file_types = [
            {
                "name": "NewFileExtension::NewText",
                "label": "📝 Text File",
                "extension": ".txt",
                "icon": "text-x-generic",
                "template": ""
            },
            {
                "name": "NewFileExtension::NewJson",
                "label": "🔧 JSON File",
                "extension": ".json",
                "icon": "text-x-script",
                "template": "{\n  \n}\n"
            },
            {
                "name": "NewFileExtension::NewMarkdown",
                "label": "📋 Markdown File",
                "extension": ".md",
                "icon": "text-x-generic",
                "template": "# New Document\n\n"
            },
            {
                "name": "NewFileExtension::NewShell",
                "label": "⚙️ Shell Script",
                "extension": ".sh",
                "icon": "text-x-script",
                "template": "#!/bin/bash\nset -e\n\n"
            },
            {
                "name": "NewFileExtension::NewPython",
                "label": "🐍 Python Script",
                "extension": ".py",
                "icon": "text-x-python",
                "template": "#!/usr/bin/env python3\n\n"
            },
            {
                "name": "NewFileExtension::NewCustom",
                "label": "📄 Custom File...",
                "extension": "",  # Empty = All Files
                "icon": "document-new",
                "template": ""
            },
        ]
        
        # Add menu items for each file type
        for file_type in file_types:
            item = Nautilus.MenuItem(
                name=file_type["name"],
                label=file_type["label"],
                tip=f"Create a new file",
                icon=file_type["icon"]
            )
            item.connect("activate", self.show_dialog_cb, folder_path, file_type)
            submenu.append_item(item)
        
        return [main_item]
    
    def show_dialog_cb(self, menu, folder_path, file_type):
        """Show dialog to input filename"""
        dialog = NewFileDialog(
            parent=None,
            folder_path=folder_path,
            default_extension=file_type["extension"],  # Không fallback, giữ nguyên "" nếu custom
            default_template=file_type["template"]
        )
        
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            filename, template, ext = dialog.get_result()
            
            if filename:
                file_path = os.path.join(folder_path, filename)
                self.create_file(file_path, template, ext)
        
        dialog.destroy()
    
    def create_file(self, file_path, template, extension):
        """Create the file and open it"""
        try:
            # Create the file with template content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(template)
            
            # Make shell scripts executable
            if extension == ".sh":
                os.chmod(file_path, 0o755)
            
            # Open with default text editor
            editors = ["gedit", "gnome-text-editor", "xdg-open"]
            for editor in editors:
                try:
                    subprocess.Popen([editor, file_path])
                    break
                except FileNotFoundError:
                    continue
            
        except Exception as e:
            print(f"Error creating file: {e}")
