# Cricket Potsdam - Fantasy Cricket Auction System

A comprehensive fantasy cricket auction application with both **Python GUI** and **Web-based** interfaces, featuring custom auction rules designed specifically for Cricket Potsdam league.

## 🚀 Quick Start

### Web Version (Recommended)
Simply open `auction_web.html` in your browser - no installation required!

### Python GUI Version
```bash
pip install -r requirements.txt
python cricket_auction.py
```

## ✨ Key Features

### 🎯 Custom Auction Rules
- **€10 Bid Increments**: Small, manageable bid steps
- **No Timer**: Relaxed bidding environment
- **Base Price Purchase**: Players can be bought instantly at base price
- **Unsold Player Re-auction**: Failed auctions get second chances
- **Manager-Player Logic**: Special pricing for team managers

### 🏏 Player & Team Management
- **21 Players**: 11 Tigers (premium) + 9 Lions (standard) + 1 Manager per team
- **Dynamic Team Limits**: Configurable max players, Tigers, and Lions per team
- **Custom Player Addition**: Add new players during auction
- **Player Removal**: Remove players and restore budgets
- **€2000 Starting Budget** per team

### 🧍‍♂️ Teams & Managers
1. **Imtiaz** → "Patronus Voyagers"
2. **Ifthekhar** → "Alpha Knight" 
3. **Mahfuz** → "X-Mafias Return"

### 💾 Export & Data Management
- **Formatted Text Export**: PDF-style team summaries
- **JSON Backup**: Complete auction state preservation
- **Real-time Saving**: Automatic progress tracking

## 🖥️ Application Versions

### Web Version (`auction_web.html`)
- **Browser-based**: Works on any device with a web browser
- **Mobile Friendly**: Responsive design for tablets and phones
- **Real-time Updates**: Live bidding and team status
- **Modern UI**: Clean, professional interface
- **Local Storage**: Automatic save/restore functionality

### Python GUI Version (`cricket_auction.py`)
- **Desktop Application**: Full-screen tkinter interface
- **Keyboard Shortcuts**: Fast navigation and bidding
- **Cross-platform**: Windows, macOS, Linux support
- **Offline Operation**: No internet connection required

## 📋 Player Categories

### TIGER Category (Premium Players)
- **Shanto** (€150), **Tanzim** (€150), **Pranto** (€150)
- **Oni** (€120), **Rifat** (€120), **Naim** (€120), **Nahid** (€120)
- **Sony** (€100), **Sufiyan** (€100), **Samit** (€100), **Shanto Berlin** (€100)

### LION Category (Standard Players)
- **Akash** (€80), **Amamul** (€80), **Tanveer** (€80), **Raisul** (€80)
- **Ankon** (€80), **Shahriar** (€80), **Dip** (€80), **Ejaz** (€80)

### MANAGER Category (Special Pricing)
- **Team Managers**: €50 each (reduced price for team captains)

## 🎮 How to Conduct an Auction

### Setup Phase
1. Open the application (web or desktop)
2. Configure team rules if needed (max players, categories)
3. Review player list and prices

### Auction Process
1. **Next Player**: Click to randomly select next player for auction
2. **Bidding**: 
   - Use **Bid +€10** buttons for incremental bidding
   - Click **Buy at Base Price** for instant purchase
   - **Pass** to skip bidding
3. **Sold**: Finalize the sale to highest bidder
4. **Unsold Handling**: Failed auctions automatically re-enter the pool

### Advanced Features
- **Remove Players**: Undo purchases and restore budgets
- **Add Custom Players**: Create new players during auction
- **Team Configuration**: Adjust limits mid-auction if needed
- **Export Results**: Generate final team reports

## 📁 Project Structure

```
cricket_potsdam/
├── index.html                    # GitHub Pages landing page
├── auction_web.html              # Main web application
├── standalone_auction.html       # Self-contained web version
├── cricket_auction.py            # Python GUI application
├── requirements.txt              # Python dependencies
├── README.md                     # This documentation
├── PROJECT_SUMMARY.md            # Detailed project summary
├── FILE_GUIDE.md                 # Project file organization guide
├── demos/
│   └── demo_auction.py           # Console-based demo
├── scripts/
│   ├── test_auction.py           # Testing script
│   └── run_auction.bat           # Windows launcher
├── archive/
│   ├── web_auction.py            # Legacy Flask server
│   ├── auction_demo_*.json       # Old save files
│   └── test.html                 # Legacy test files
└── templates/
    └── auction.html              # Web template
```

## 🔧 Technical Details

### Web Version Technology
- **Pure HTML/CSS/JavaScript**: No frameworks or dependencies
- **Local Storage API**: Browser-based data persistence
- **Responsive Design**: Mobile and desktop compatible
- **Modern ES6+**: Clean, maintainable code

### Python Version Technology
- **Tkinter GUI**: Cross-platform desktop interface
- **JSON Data**: Lightweight data storage
- **Object-Oriented**: Clean class structure
- **Error Handling**: Robust exception management

### Requirements
- **Web**: Any modern browser (Chrome, Firefox, Safari, Edge)
- **Python**: 3.7+ with tkinter (usually included)
- **Optional**: pygame for sound effects (Python version)

## 🎯 Live Auction Tips

### For Web-based Auctions
- Share your screen during video calls
- Use full-screen mode for better visibility
- Test on the same browser/device before going live
- Have backup JSON files ready

### For Desktop Auctions
- Use dual monitor setup for better control
- Enable full-screen mode for presentations
- Keep export functionality easily accessible
- Test all features before live event

## 🛠️ Customization

### Modifying Players and Prices
Edit the player arrays in either:
- `auction_web.html` (lines ~30-80)
- `cricket_auction.py` (setup_data method)

### Changing Team Rules
Adjust the configuration variables:
- `MAX_PLAYERS_PER_TEAM`
- `MAX_TIGERS_PER_TEAM` 
- `MAX_LIONS_PER_TEAM`
- `STARTING_BUDGET`

### Bid Increment
Change the bid step from €10 to any value in the bidding functions.

## 🐛 Troubleshooting

### Common Issues
- **Web version not saving**: Check browser local storage permissions
- **Python dependencies**: Install requirements.txt packages
- **Display issues**: Try different screen resolutions
- **Data loss**: Use JSON export/import for backup

### Browser Compatibility
- Chrome/Edge: Full support
- Firefox: Full support  
- Safari: Full support
- Mobile browsers: Basic support

## 📈 Future Enhancements

- Real-time multiplayer synchronization
- Advanced statistics and analytics
- Player performance integration
- Mobile app versions
- Database backend support

---

**🏏 Developed for Cricket Potsdam Fantasy League**  
*Professional auction management with custom rules and dual interfaces*

**Version**: 2.0 | **Last Updated**: July 2025
