# Cricket Potsdam - Project File Guide

## 🎯 Main Application Files

### **Web Version (Recommended)**
- **`index.html`** - Landing page for GitHub Pages
- **`auction_web.html`** - Main web auction application
- **`standalone_auction.html`** - Self-contained web version

### **Desktop Version**
- **`cricket_auction.py`** - Python GUI application (Tkinter)

## 📋 Project Documentation
- **`README.md`** - Main project documentation
- **`PROJECT_SUMMARY.md`** - Detailed project summary
- **`requirements.txt`** - Python dependencies

## 📁 Organized Directories

### **`demos/`** - Demo and Example Files
- **`demo_auction.py`** - Console-based demo version
- Shows basic auction logic without GUI

### **`scripts/`** - Utility Scripts
- **`test_auction.py`** - Testing and validation script
- **`run_auction.bat`** - Windows batch file to run Python app

### **`archive/`** - Legacy and Backup Files
- **`web_auction.py`** - Flask web server (superseded by HTML version)
- **`auction_demo_*.json`** - Old auction save files
- **`test.html`** - Old test files

### **`templates/`** - Web Templates
- **`auction.html`** - Template file for web version

## 🚀 Quick Start Guide

### For Web Auction (Easiest):
1. Open `auction_web.html` in any browser
2. Start bidding immediately

### For Desktop Auction:
1. Install Python 3.7+
2. Run: `pip install -r requirements.txt`
3. Run: `python cricket_auction.py`

### For GitHub Pages:
Visit: https://ataullahkhanrifat.github.io/cricket_potsdam/

## 🎯 Which Files to Use?

### **Live Auction Events:**
- **Primary**: `auction_web.html` (web version)
- **Backup**: `cricket_auction.py` (desktop version)

### **Testing and Development:**
- `demos/demo_auction.py` - Test auction logic
- `scripts/test_auction.py` - Validate setup

### **Documentation:**
- `README.md` - For users and contributors
- This file - For understanding project structure

## 🔄 File Dependencies

```
Web Version:
├── index.html (landing page)
├── auction_web.html (main app)
└── standalone_auction.html (backup)

Desktop Version:
├── cricket_auction.py (main app)
└── requirements.txt (dependencies)

Development:
├── demos/demo_auction.py
├── scripts/test_auction.py
└── archive/ (old files)
```

## 📝 Notes for Contributors

- **Main development**: Focus on `auction_web.html` and `cricket_auction.py`
- **Testing**: Use files in `demos/` and `scripts/`
- **Archive**: Don't delete `archive/` files (version history)
- **Templates**: Keep `templates/` for future web development

---
*This structure keeps all files organized while maintaining project history*
