#!/usr/bin/env python3
"""
Cricket Potsdam Auction - Demo Console Version
A simple console-based demonstration of the auction system
"""

import random
import json
from datetime import datetime

class Player:
    """Represents a cricket player in the auction"""
    
    def __init__(self, name: str, base_price: int, category: str):
        self.name = name
        self.base_price = base_price
        self.category = category
        self.sold_price = 0
        self.sold_to = None
        self.is_sold = False
    
    def __repr__(self):
        return f"Player({self.name}, €{self.base_price}, {self.category})"

class Manager:
    """Represents a team manager"""
    
    def __init__(self, name: str, team_name: str, budget: int = 2000):
        self.name = name
        self.team_name = team_name
        self.budget = budget
        self.players = []
        self.tiger_count = 0
        self.lion_count = 0
    
    def can_bid(self, amount: int, category: str) -> bool:
        """Check if manager can place this bid"""
        if amount > self.budget:
            return False
        
        if category == "TIGER" and self.tiger_count >= 4:
            return False
        
        if category == "LION" and self.lion_count >= 3:
            return False
        
        return True
    
    def add_player(self, player: Player):
        """Add a player to the manager's team"""
        self.players.append(player)
        self.budget -= player.sold_price
        
        if player.category == "TIGER":
            self.tiger_count += 1
        else:
            self.lion_count += 1

class ConsoleAuction:
    """Console-based auction demonstration"""
    
    def __init__(self):
        self.setup_data()
        self.sold_players = []
    
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
        
        # Track category rotation (start with Tiger)
        self.next_category = "TIGER"
    
    def print_banner(self):
        """Print the auction banner"""
        print("=" * 60)
        print("🏏 CRICKET POTSDAM - PLAYER AUCTION DEMO 🏏")
        print("=" * 60)
        print()
    
    def print_teams_status(self):
        """Print current team status"""
        print("\n" + "=" * 60)
        print("CURRENT TEAM STATUS")
        print("=" * 60)
        
        for manager in self.managers:
            print(f"\n🏏 {manager.team_name}")
            print(f"   Manager: {manager.name}")
            print(f"   Budget: €{manager.budget}")
            print(f"   Tigers: {manager.tiger_count}/4 | Lions: {manager.lion_count}/3")
            
            if manager.players:
                print("   Players:")
                for player in manager.players:
                    print(f"     • {player.name} ({player.category}) - €{player.sold_price}")
            else:
                print("   Players: None yet")
    
    def simulate_auction(self, num_rounds=5):
        """Simulate a few auction rounds"""
        
        self.print_banner()
        print("Starting auction simulation...")
        print(f"Simulating {num_rounds} player auctions")
        
        for round_num in range(1, num_rounds + 1):
            print(f"\n{'=' * 40}")
            print(f"AUCTION ROUND {round_num}")
            print(f"{'=' * 40}")
            
            # Select next player
            if self.next_category == "TIGER" and self.tiger_pool:
                current_player = self.tiger_pool.pop(0)
                self.next_category = "LION"
            elif self.next_category == "LION" and self.lion_pool:
                current_player = self.lion_pool.pop(0)
                self.next_category = "TIGER"
            elif self.tiger_pool:
                current_player = self.tiger_pool.pop(0)
            elif self.lion_pool:
                current_player = self.lion_pool.pop(0)
            else:
                print("No more players available!")
                break
            
            print(f"\n🎯 Player: {current_player.name}")
            print(f"   Category: {current_player.category}")
            print(f"   Base Price: €{current_player.base_price}")
            
            # Simulate bidding
            eligible_managers = [
                m for m in self.managers 
                if m.can_bid(current_player.base_price + 50, current_player.category)
            ]
            
            if not eligible_managers:
                print(f"   ❌ No one can bid on {current_player.name}")
                continue
            
            # Random bidding simulation
            current_bid = current_player.base_price
            highest_bidder = None
            bid_count = 0
            
            while eligible_managers and bid_count < 5:  # Max 5 bid rounds
                bidder = random.choice(eligible_managers)
                current_bid += 50
                
                if bidder.can_bid(current_bid, current_player.category):
                    highest_bidder = bidder
                    print(f"   💰 {bidder.name} bids €{current_bid}")
                    bid_count += 1
                    
                    # Remove managers who can't bid higher
                    eligible_managers = [
                        m for m in eligible_managers 
                        if m.can_bid(current_bid + 50, current_player.category)
                    ]
                    
                    # Random chance to stop bidding
                    if random.random() < 0.4:  # 40% chance to stop
                        break
                else:
                    eligible_managers.remove(bidder)
            
            # Finalize sale
            if highest_bidder:
                current_player.sold_price = current_bid
                current_player.sold_to = highest_bidder.name
                current_player.is_sold = True
                
                highest_bidder.add_player(current_player)
                self.sold_players.append(current_player)
                
                print(f"   🎉 SOLD to {highest_bidder.name} for €{current_bid}!")
            else:
                print(f"   ❌ No valid bids for {current_player.name}")
        
        # Final status
        self.print_teams_status()
        self.print_auction_summary()
    
    def print_auction_summary(self):
        """Print auction summary"""
        print(f"\n{'=' * 60}")
        print("AUCTION SUMMARY")
        print(f"{'=' * 60}")
        
        print(f"Players sold: {len(self.sold_players)}")
        print(f"Tigers remaining: {len(self.tiger_pool)}")
        print(f"Lions remaining: {len(self.lion_pool)}")
        
        total_spent = sum(player.sold_price for player in self.sold_players)
        print(f"Total money spent: €{total_spent}")
        
        print(f"\nBudgets remaining:")
        for manager in self.managers:
            print(f"  {manager.name}: €{manager.budget}")
    
    def export_demo_data(self):
        """Export demo data to JSON"""
        data = {
            "auction_date": datetime.now().isoformat(),
            "teams": [],
            "sold_players": []
        }
        
        for manager in self.managers:
            team_data = {
                "team_name": manager.team_name,
                "manager": manager.name,
                "budget_left": manager.budget,
                "tigers": manager.tiger_count,
                "lions": manager.lion_count,
                "players": [
                    {
                        "name": player.name,
                        "category": player.category,
                        "price": player.sold_price
                    }
                    for player in manager.players
                ]
            }
            data["teams"].append(team_data)
        
        for player in self.sold_players:
            data["sold_players"].append({
                "name": player.name,
                "category": player.category,
                "base_price": player.base_price,
                "sold_price": player.sold_price,
                "sold_to": player.sold_to
            })
        
        filename = f"auction_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Demo data exported to: {filename}")

def main():
    """Main function"""
    print("🏏 Cricket Potsdam Auction - Console Demo")
    print("This demonstrates the auction system functionality")
    print()
    
    auction = ConsoleAuction()
    auction.simulate_auction(8)  # Simulate 8 rounds
    
    print(f"\n{'=' * 60}")
    print("DEMO COMPLETE!")
    print("This shows how the auction system works.")
    print("The full GUI version will have interactive bidding buttons.")
    print(f"{'=' * 60}")
    
    auction.export_demo_data()
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
