# Universal Sports Auction Platform

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Live Demo](https://img.shields.io/badge/demo-live-green.svg)](https://ataullahkhanrifat.github.io/cricket_potsdam/)

A modern, configurable sports auction application that can be adapted for any sport or event. Originally developed for Cricket Potsdam, now evolved into a universal platform with professional UI/UX design.

## 🌐 Live Demo
**Try it now**: https://ataullahkhanrifat.github.io/cricket_potsdam/

## 🚀 Quick Start

### Web Version (Recommended)
```bash
# Method 1: Open directly in browser
open src/web/auction_web.html

# Method 2: Use local server
python scripts/server.py
# Then visit: http://localhost:8080/src/web/auction_web.html
```

### Python Versions
```bash
# GUI Version (tkinter)
python src/python/cricket_auction.py
```

## � Project Structure

```
cricket_potsdam/
├── 📄 README.md                 # Main documentation
├── 📄 LICENSE                   # MIT License
├── 📄 requirements.txt          # Python dependencies
├── 📄 .gitignore               # Git ignore rules
├── 📁 src/                     # Source code
│   ├── 📁 web/                 # Web application
│   │   ├── auction_web.html    # Main auction app
│   │   └── index.html          # Landing page
│   └── 📁 python/              # Python applications
│       └── cricket_auction.py  # GUI version
├── 📁 scripts/                 # Utility scripts
│   ├── server.py              # Local web server
│   └── run_auction.bat        # Windows launcher
├── 📁 tests/                   # Test files
│   ├── test_auction.py        # Main tests
│   └── simple_test.py         # Basic tests
├── 📁 docs/                    # Documentation
│   └── PROJECT_SUMMARY.md     # Technical details
├── 📁 examples/                # Example configurations
└── 📁 data/                    # Sample and demo data
    └── auction_demo_*.json     # Demo auction results
```

## 🔧 Technical Details

### Web Application (Primary)
- **Technology**: Pure HTML/CSS/JavaScript
- **Dependencies**: None - runs in any modern browser
- **Storage**: Browser Local Storage for data persistence
- **Compatibility**: Chrome, Firefox, Safari, Edge
- **Mobile Support**: Responsive design for all screen sizes

### Design System
- **CSS Custom Properties**: Consistent theming
- **Modern Layout**: CSS Grid and Flexbox
- **Typography**: Inter font family from Google Fonts
- **Color Palette**: Professional gradients and accent colors
- **Animations**: Smooth transitions and micro-interactions

### Browser Requirements
- **Modern Browser**: Any browser from the last 3 years
- **JavaScript**: ES6+ support (standard since 2015)
- **Local Storage**: For saving auction progress
- **No Plugins**: Works without additional software

## 🎯 Example Configurations

### 🏏 Cricket Tournament
- **Teams**: 4 teams, €2000 budget
- **Categories**: Batsman (max 4), Bowler (max 3), All-rounder (max 2)
- **Players**: 50+ players with base prices €50-€200

### ⚽ Football Draft  
- **Teams**: 6 teams, €5000 budget
- **Categories**: Striker (max 2), Midfielder (max 4), Defender (max 4), Goalkeeper (max 1)
- **Players**: 100+ players with base prices €100-€500

### 🎮 Gaming Tournament
- **Teams**: 8 teams, €1000 budget
- **Categories**: DPS (max 2), Tank (max 1), Support (max 2)
- **Players**: Custom roster with skill-based pricing

## 🛡️ Data & Privacy

### Local Storage Only
- **No Server**: All data stays in your browser
- **No Registration**: No accounts or personal data required
- **Privacy First**: Complete control over your auction data
- **Offline Capable**: Works without internet after loading

### Export Options
- **Text Format**: Professional auction summaries
- **Copy-Paste**: Easy sharing of results
- **Browser Download**: Automatic file generation
- **JSON Backup**: Technical data preservation

## 🐛 Troubleshooting

### Common Solutions
- **Not Loading**: Try refreshing or different browser
- **Data Lost**: Check browser Local Storage permissions
- **Mobile Issues**: Use landscape mode for better experience
- **Export Problems**: Ensure pop-ups are allowed

### Browser Support
- ✅ **Chrome/Edge**: Full support, recommended
- ✅ **Firefox**: Full support
- ✅ **Safari**: Full support
- ⚠️ **Mobile**: Basic support, tablet recommended

## 🔄 Legacy Versions

### Python GUI Version
```bash
pip install -r requirements.txt
python cricket_auction.py
```

### Flask Web Version
```bash
pip install flask
python web_auction.py
# Access: http://localhost:5000
```

### Console Demo
```bash
python demo_auction.py
```

## 📈 Future Enhancements

- **Real-time Sync**: Multi-device synchronization
- **Advanced Stats**: Player performance analytics  
- **Database Backend**: Cloud storage options
- **Mobile Apps**: Native iOS/Android versions
- **API Integration**: Sports data connectivity

## 🤝 Contributing

This is an open-source project perfect for:
- **Web developers** learning modern CSS/JavaScript
- **Sports enthusiasts** customizing for their leagues
- **UI/UX designers** improving the interface
- **Students** studying auction algorithms

## 📄 License

**Proprietary License** - All rights reserved. This software is protected by copyright law. 
Unauthorized copying, distribution, or modification is strictly prohibited. 
See [LICENSE](LICENSE) file for detailed terms and conditions.

---

**🏆 From Cricket Potsdam to Universal Sports Auction Platform**  
*Professional auction management with modern design and universal flexibility*

**Live Demo**: https://ataullahkhanrifat.github.io/cricket_potsdam/  
**Version**: 3.0 | **Last Updated**: July 2025
