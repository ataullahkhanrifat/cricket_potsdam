# Cricket Potsdam - Player Auction App

A Python GUI application for conducting live fantasy cricket player auctions, designed for Zoom presentations.

## Features

### 🎯 Core Functionality
- **Live Bidding System**: Real-time auction interface for 3 team managers
- **Player Pool Management**: 21 players divided into Tiger (11) and Lion (9) categories
- **Budget Tracking**: Each team starts with €1300 budget
- **Team Limits**: Maximum 4 Tigers and 3 Lions per team
- **Random Player Selection**: Lottery-style player drawing with category rotation

### 🧍‍♂️ Teams & Managers
1. **Imtiaz** → "Patronus Voyagers"
2. **Ifthekhar** → "Alpha Knight" 
3. **Mahfuz** → "X-Mafias Return"

### 🏏 Player Categories

**TIGER Category (11 players):**
- Shanto (€150), Tanzim (€150), Pranto (€150)
- Oni (€120), Rifat (€120), Naim (€120), Nahid (€120)
- Sony (€100), Sufiyan (€100), Samit (€100), Shanto Berlin (€100)

**LION Category (9 players):**
- Akash (€80), Amamul (€80), Tanveer (€80), Raisul (€80)
- Ankon (€80), Shahriar (€80), Dip (€80), Ejaz (€80)

## Installation

1. **Install Python** (3.7 or higher)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python cricket_auction.py
```

## How to Use

### Starting an Auction
1. Launch the application
2. Click **"Next Player"** to begin
3. A random player will be selected for bidding

### Bidding Process
1. Current player details are displayed at the top
2. Each manager has **"Bid +€50"** and **"Pass"** buttons
3. Bids increase in €50 increments
4. 30-second timer for each round
5. Click **"SOLD!"** to finalize the sale

### Features During Auction
- **Real-time Budget Updates**: See remaining budget for each team
- **Category Limits**: Buttons automatically disable when team limits are reached
- **Timer System**: 30-second countdown with auto-sell on timeout
- **Team Display**: Live view of acquired players and spending

### Export & Reset
- **Export Teams**: Save final team rosters to CSV
- **Reset Auction**: Clear all data and start fresh

## GUI Layout

### Top Section
- **Title**: "Cricket Potsdam" 
- **Current Player**: Name, category, base price
- **Bidding Controls**: Manager buttons and timer

### Team Columns (3 columns)
Each team shows:
- Team name and manager
- Budget remaining
- Tiger/Lion count
- List of purchased players with prices

### Control Panel
- Next Player button
- Sold button
- Export and Reset options

## Technical Details

### File Structure
```
cricket_potsdam/
├── cricket_auction.py    # Main application
├── requirements.txt      # Dependencies
└── README.md            # This file
```

### Key Classes
- **Player**: Represents individual cricket players
- **Manager**: Handles team data and budget
- **AuctionApp**: Main tkinter GUI application

### Features
- **Fullscreen Mode**: Optimized for Zoom screen sharing
- **Dark Theme**: Black background for professional presentation
- **Sound Effects**: Optional audio feedback (requires pygame)
- **CSV Export**: Team data export functionality
- **Input Validation**: Prevents overspending and category limit violations

## Troubleshooting

### Common Issues
1. **Pygame not working**: Sound effects will be disabled automatically
2. **Screen too small**: Application automatically goes fullscreen
3. **Timer not showing**: Check if bidding is active

### Requirements
- Python 3.7+
- tkinter (usually included with Python)
- pygame (for sound effects, optional)

## Customization

### Modifying Players
Edit the `setup_data()` method in `cricket_auction.py` to change:
- Player names and prices
- Team budgets
- Category limits

### Changing Bid Increments
Modify the bid increment in the `place_bid()` method (currently €50).

### Timer Duration
Adjust `self.timer_seconds = 30` in the `start_timer()` method.

## Live Streaming Tips

### For Zoom Presentations
1. Run application in fullscreen mode
2. Share entire screen for best visibility
3. Use a second monitor for controls if available
4. Test audio settings before live auction

### Best Practices
- Have a backup moderator to handle technical issues
- Pre-test all functionality before the live event
- Keep the CSV export ready for final team announcements

## Support

For issues or customizations, check the code comments or modify the application as needed for your specific auction requirements.

---

**Developed for Cricket Potsdam Fantasy League**
*Designed for live Zoom auctions with real-time bidding*
