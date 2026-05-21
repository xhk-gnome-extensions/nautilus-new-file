# Nautilus/Files New File Extension

Extension cho Nautilus (GNOME Files) để tạo file mới nhanh chóng với UI đẹp và các template sẵn.

> **Lưu ý:** Nautilus được đổi tên thành "Files" từ Ubuntu 24.04+, nhưng package name vẫn là `nautilus`

![New File Dialog](https://img.shields.io/badge/GTK-3.0%2F4.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%2B-orange)

## ✨ Tính năng

Khi chuột phải vào khoảng trống trong Nautilus/Files, sẽ có menu **"📄 New File"** với các tùy chọn:

- **📝 Text File** - File text trống
- **🔧 JSON File** - File JSON với template `{}`
- **📋 Markdown File** - File Markdown với header `# New Document`
- **⚙️ Shell Script** - Shell script với shebang và `set -e`
- **🐍 Python Script** - Python script với shebang
- **🌐 HTML File** - HTML5 template đầy đủ
- **🎨 CSS File** - CSS file với comment header
- **⚡ JavaScript File** - JavaScript với comment
- **📋 XML File** - XML với declaration
- **📝 YAML File** - YAML với comment
- **📄 Custom File...** - Tự nhập tên và extension bất kỳ

### UI Dialog

Khi chọn loại file, một dialog đẹp sẽ hiện ra với:
- **Header bar** với nút Cancel và Create
- **Input field lớn** để nhập tên file
- **Extension dropdown** để chọn hoặc đổi extension
- **Auto-focus** và text được select sẵn
- **Enter** để tạo file nhanh

## 📦 Cài đặt

```bash
cd <folder>
chmod +x install-new-file-extension.sh
./install-new-file-extension.sh
```

Script sẽ tự động:
- Tạo thư mục extension nếu chưa có
- Copy extension vào `~/.local/share/nautilus-python/extensions/`
- Kiểm tra và cài đặt dependencies (nếu thiếu)
- Restart Nautilus

## 🚀 Sử dụng

### Cách 1: Từ menu
1. Mở **Files** (Nautilus) - File manager mặc định
2. Vào thư mục bất kỳ
3. Chuột phải vào khoảng trống
4. Chọn **"📄 New File"** → Chọn loại file
5. Dialog hiện ra → Nhập tên file
6. Click **"Create"** hoặc nhấn **Enter**
7. File được tạo và tự động mở bằng gedit

### Cách 2: Custom file
1. Chọn **"📄 New File"** → **"📄 Custom File..."**
2. Extension dropdown tự động chọn **"All Files"**
3. Nhập tên file với extension tùy ý (vd: `config.ini`, `README`, `.gitignore`)
4. Click Create

### Ví dụ

**Tạo file Python:**
- Chọn "🐍 Python Script"
- Nhập: `hello` → Tạo `hello.py` với shebang
- Nhập: `hello.py` → Tạo `hello.py` (extension tự động)

**Tạo file custom:**
- Chọn "📄 Custom File..."
- Nhập: `config.ini` → Tạo `config.ini`
- Nhập: `.gitignore` → Tạo `.gitignore`
- Nhập: `README` → Tạo `README`

## 🗑️ Gỡ cài đặt

```bash
cd <folder>
chmod +x uninstall-new-file-extension.sh
./uninstall-new-file-extension.sh
```

Hoặc thủ công:

```bash
rm ~/.local/share/nautilus-python/extensions/nautilus_new_file_ext.py
nautilus -q
```

## 🎨 Tùy chỉnh

### Thêm loại file mới

Chỉnh sửa `nautilus_new_file_ext.py`, tìm phần `file_types` và thêm:

```python
file_types = [
    # ... existing types ...
    {
        "name": "NewFileExtension::NewYourType",
        "label": "🎨 Your File",
        "extension": ".ext",
        "icon": "text-x-generic",
        "template": "Your template content here\n"
    },
]
```

Thêm template tương ứng trong `self.templates`:

```python
self.templates = {
    # ... existing templates ...
    ".ext": "Your template content\n",
}
```

Sau đó restart Nautilus:

```bash
nautilus -q
```

### Thay đổi editor mặc định

Chỉnh sửa dòng này trong `create_file()`:

```python
editors = ["gedit", "gnome-text-editor", "xdg-open"]
```

Thay bằng editor bạn muốn (vd: `["code", "vim", "nano"]`)

## 📋 Yêu cầu

### Bắt buộc:
- **Nautilus/Files** - File manager mặc định của GNOME (Ubuntu 22.04+)
- **python3-nautilus** - Python bindings cho Nautilus
- **gir1.2-nautilus-3.0** (Ubuntu 22.04, 23.04) hoặc **gir1.2-nautilus-4.0** (Ubuntu 24.04+) - GObject introspection
- **GTK 3.0** - GUI toolkit

### Tùy chọn:
- **gedit** hoặc **gnome-text-editor** - Để mở file (fallback: xdg-open)

### Cài đặt dependencies:

**Ubuntu 22.04 / 23.04:**
```bash
sudo apt install python3-nautilus gir1.2-nautilus-3.0 gedit
```

**Ubuntu 24.04+ / 25.04+:**
```bash
sudo apt install python3-nautilus gir1.2-nautilus-4.0 gnome-text-editor
# Hoặc nếu dùng gedit:
sudo apt install python3-nautilus gir1.2-nautilus-4.0 gedit
```

**Fedora:**
```bash
sudo dnf install nautilus-python gedit
```

> **Lưu ý:** Script cài đặt sẽ tự động detect và cài đúng version

## 🔧 Troubleshooting

### Extension không hiện trong menu

**Lưu ý:** Trên Ubuntu 24.04+, file manager có tên "Files" nhưng vẫn dùng Nautilus backend.

1. **Kiểm tra extension đã được cài:**
```bash
ls -la ~/.local/share/nautilus-python/extensions/
# Phải thấy: nautilus_new_file_ext.py
```

2. **Kiểm tra nautilus-python (thử cả 2 version):**
```bash
# Ubuntu 22.04/23.04
python3 -c "import gi; gi.require_version('Nautilus', '3.0'); print('Nautilus 3.0 OK')"

# Ubuntu 24.04+
python3 -c "import gi; gi.require_version('Nautilus', '4.0'); print('Nautilus 4.0 OK')"
```

3. **Restart Files/Nautilus:**
```bash
nautilus -q
sleep 2
nautilus &
# Hoặc: killall nautilus && nautilus &
```

4. **Kiểm tra quyền file:**
```bash
chmod +x ~/.local/share/nautilus-python/extensions/nautilus_new_file_ext.py
```

5. **Kiểm tra Nautilus version:**
```bash
nautilus --version
# Nautilus 3.x → Dùng gir1.2-nautilus-3.0
# Nautilus 4.x+ → Dùng gir1.2-nautilus-4.0
```

### Xem log lỗi

**Cách 1: journalctl**
```bash
journalctl -f | grep nautilus
```

**Cách 2: Chạy Nautilus từ terminal**
```bash
nautilus -q
nautilus
# Chuột phải và xem output trong terminal
```

### Extension bị lỗi sau khi update

```bash
# Gỡ và cài lại
./uninstall-new-file-extension.sh
./install-new-file-extension.sh
```

### File không mở sau khi tạo

Kiểm tra editor có cài không:
```bash
which gedit
which gnome-text-editor
```

Nếu không có, cài:
```bash
sudo apt install gedit
```

## 🔗 Tích hợp với PackageManager

Extension này độc lập với PackageManager nhưng có thể cài chung:

```bash
cd <folder>

# Cài PackageManager extension (chuột phải .deb/.AppImage để install)
./install.sh

# Cài New File extension (chuột phải khoảng trống để tạo file)
./install-new-file-extension.sh
```

## 🌟 Tính năng nổi bật

- ✅ **UI đẹp** - Dialog hiện đại với GTK header bar
- ✅ **Nhanh chóng** - Enter để tạo file ngay
- ✅ **Thông minh** - Tự động thêm extension
- ✅ **Linh hoạt** - Hỗ trợ custom extension
- ✅ **Templates** - Nhiều template có sẵn
- ✅ **Tương thích** - Hoạt động với Nautilus 3.0 và 4.0
- ✅ **Nhẹ** - Không ảnh hưởng hiệu năng

## 📝 Templates có sẵn

| Extension | Template |
|-----------|----------|
| `.txt` | File trống |
| `.json` | `{ }` |
| `.md` | `# New Document` |
| `.sh` | `#!/bin/bash` + `set -e` |
| `.py` | `#!/usr/bin/env python3` |
| `.html` | HTML5 boilerplate |
| `.css` | CSS comment |
| `.js` | JavaScript comment |
| `.xml` | XML declaration |
| `.yaml` | YAML comment |

## 🤝 Đóng góp

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Add more file templates

## 📄 License

MIT License - Free to use and modify

## 👨‍💻 Author

Created for easier file management in Nautilus

---

**Tip:** Nhấn `Ctrl+Shift+N` trong Files/Nautilus để tạo folder mới, và dùng extension này để tạo file mới! 🚀

## 🔍 Compatibility

| Ubuntu Version | Nautilus Version | Package Name | Extension Works |
|----------------|------------------|--------------|-----------------|
| 22.04 LTS | Nautilus 3.x | `gir1.2-nautilus-3.0` | ✅ |
| 23.04 | Nautilus 3.x | `gir1.2-nautilus-3.0` | ✅ |
| 24.04 LTS | Files (Nautilus 4.x) | `gir1.2-nautilus-4.0` | ✅ |
| 25.04+ | Files (Nautilus 4.x+) | `gir1.2-nautilus-4.0` | ✅ |

Extension tự động detect và tương thích với cả 2 version!
