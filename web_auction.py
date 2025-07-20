#!/usr/bin/env python3
"""
Cricket Potsdam - Web-based Player Auction
A simple web interface for the auction system using Flask
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import random
from datetime import datetime
import os

# Import our auction classes
from demo_auction import Player, Manager

app = Flask(__name__)

class WebAuction:
    """Web-based auction system"""
    
    def __init__(self):
        self.setup_data()
        self.current_player = None
        self.current_bid = 0
        self.highest_bidder = None
        self.bidding_active = False
        self.sold_players = []
        self.next_category = "TIGER"
    
    def setup_data(self):
        """Initialize players and managers"""
        
        # Create player pool
        tiger_players = [
            Player("Shanto", 150, "TIGER"),
            Player("Tanzim", 150, "TIGER"),
            Player("Pranto", 150, "TIGER"),
            Player("Oni", 120, "TIGER"),
            Player("Rifat", 120, "TIGER"),
            Player("Naim", 120, "TIGER"),
            Player("Nahid", 120, "TIGER"),
            Player("Sony", 100, "TIGER"),
            Player("Sufiyan", 100, "TIGER"),
            Player("Samit", 100, "TIGER"),
            Player("Shanto Berlin", 100, "TIGER")
        ]
        
        lion_players = [
            Player("Akash", 80, "LION"),
            Player("Amamul", 80, "LION"),
            Player("Tanveer", 80, "LION"),
            Player("Raisul", 80, "LION"),
            Player("Ankon", 80, "LION"),
            Player("Shahriar", 80, "LION"),
            Player("Dip", 80, "LION"),
            Player("Ejaz", 80, "LION")
        ]
        
        # Shuffle players for random selection
        random.shuffle(tiger_players)
        random.shuffle(lion_players)
        
        self.tiger_pool = tiger_players
        self.lion_pool = lion_players
        
        # Create managers
        self.managers = [
            Manager("Imtiaz", "Patronus Voyagers"),
            Manager("Ifthekhar", "Alpha Knight"),
            Manager("Mahfuz", "X-Mafias Return")
        ]
    
    def get_state(self):
        """Get current auction state"""
        return {
            "current_player": {
                "name": self.current_player.name if self.current_player else None,
                "category": self.current_player.category if self.current_player else None,
                "base_price": self.current_player.base_price if self.current_player else None
            } if self.current_player else None,
            "current_bid": self.current_bid,
            "highest_bidder": self.highest_bidder.name if self.highest_bidder else None,
            "bidding_active": self.bidding_active,
            "managers": [
                {
                    "name": m.name,
                    "team_name": m.team_name,
                    "budget": m.budget,
                    "tiger_count": m.tiger_count,
                    "lion_count": m.lion_count,
                    "players": [
                        {
                            "name": p.name,
                            "category": p.category,
                            "price": p.sold_price
                        } for p in m.players
                    ]
                } for m in self.managers
            ],
            "remaining_players": {
                "tigers": len(self.tiger_pool),
                "lions": len(self.lion_pool)
            }
        }
    
    def next_player(self):
        """Select the next player for auction"""
        
        # Determine which category to pick from
        if self.next_category == "TIGER" and self.tiger_pool:
            self.current_player = self.tiger_pool.pop(0)
            self.next_category = "LION"
        elif self.next_category == "LION" and self.lion_pool:
            self.current_player = self.lion_pool.pop(0)
            self.next_category = "TIGER"
        elif self.tiger_pool:
            self.current_player = self.tiger_pool.pop(0)
        elif self.lion_pool:
            self.current_player = self.lion_pool.pop(0)
        else:
            return False  # No more players
        
        # Reset bidding state
        self.current_bid = self.current_player.base_price
        self.highest_bidder = None
        self.bidding_active = True
        
        return True
    
    def place_bid(self, manager_name):
        """Place a bid for a manager"""
        
        if not self.bidding_active or not self.current_player:
            return False
        
        manager = next((m for m in self.managers if m.name == manager_name), None)
        if not manager:
            return False
        
        new_bid = self.current_bid + 50
        
        if manager.can_bid(new_bid, self.current_player.category):
            self.current_bid = new_bid
            self.highest_bidder = manager
            return True
        
        return False
    
    def sell_player(self):
        """Sell the current player to highest bidder"""
        
        if not self.current_player or not self.highest_bidder:
            return False
        
        # Finalize the sale
        self.current_player.sold_price = self.current_bid
        self.current_player.sold_to = self.highest_bidder.name
        self.current_player.is_sold = True
        
        self.highest_bidder.add_player(self.current_player)
        self.sold_players.append(self.current_player)
        
        # Reset auction state
        self.bidding_active = False
        self.current_player = None
        
        return True

# Global auction instance
auction = WebAuction()

@app.route('/')
def index():
    """Main auction page"""
    return render_template('auction.html')

@app.route('/api/state')
def get_state():
    """Get current auction state"""
    return jsonify(auction.get_state())

@app.route('/api/next_player', methods=['POST'])
def next_player():
    """Select next player"""
    success = auction.next_player()
    return jsonify({"success": success, "state": auction.get_state()})

@app.route('/api/bid', methods=['POST'])
def place_bid():
    """Place a bid"""
    data = request.json
    manager_name = data.get('manager')
    success = auction.place_bid(manager_name)
    return jsonify({"success": success, "state": auction.get_state()})

@app.route('/api/sell', methods=['POST'])
def sell_player():
    """Sell current player"""
    success = auction.sell_player()
    return jsonify({"success": success, "state": auction.get_state()})

@app.route('/api/reset', methods=['POST'])
def reset_auction():
    """Reset the auction"""
    global auction
    auction = WebAuction()
    return jsonify({"success": True, "state": auction.get_state()})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🏏 Cricket Potsdam Web Auction")
    print("=" * 40)
    print("Starting web server...")
    print("Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
