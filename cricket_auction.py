#!/usr/bin/env python3
"""
Cricket Potsdam - Live Player Bidding App
A tkinter-based auction system for fantasy cricket player drafts
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import csv
from datetime import datetime
from typing import List, Dict, Optional

# Optional pygame import for sound effects
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


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
        return f"Player({self.name}, {self.base_price}, {self.category})"


class Manager:
    """Represents a team manager"""
    
    def __init__(self, name: str, team_name: str, budget: int = 2000):
        self.name = name
        self.team_name = team_name
        self.budget = budget
        self.players: List[Player] = []
        self.tiger_count = 0
        self.lion_count = 0
    
    def can_bid(self, amount: int, category: str) -> bool:
        """Check if manager can place this bid"""
        if amount > self.budget:
            return False
        
        # Each team needs 7 players total (including manager-player)
        total_players = len(self.players)
        if total_players >= 7:
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
        elif player.category == "LION":
            self.lion_count += 1
        # MANAGER category doesn't count toward Tiger/Lion limits
    
    def get_budget_left(self) -> int:
        return self.budget
    
    def get_team_summary(self) -> str:
        """Get formatted team summary"""
        summary = f"{self.team_name}\nManager: {self.name}\n€{self.budget} left\n"
        summary += f"Tigers: {self.tiger_count}/4, Lions: {self.lion_count}/3\n\n"
        
        for player in self.players:
            summary += f"{player.name} ({player.category}) - €{player.sold_price}\n"
        
        return summary


class AuctionApp:
    """Main auction application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Potsdam - Player Auction")
        self.root.configure(bg='black')
        self.root.state('zoomed')  # Fullscreen on Windows
        
        # Initialize pygame for sound effects (optional)
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.sound_enabled = True
            except:
                self.sound_enabled = False
        else:
            self.sound_enabled = False
        
        self.setup_data()
        self.setup_gui()
        self.current_player = None
        self.current_bid = 0
        self.highest_bidder = None
        self.bidding_active = False
        
        # Removed timer - no timer needed
        self.unsold_players = []  # Players that no one bid on
    
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
        self.sold_players = []
        
        # Create managers with manager-players
        self.managers = [
            Manager("Imtiaz", "Patronus Voyagers"),
            Manager("Ifthekhar", "Alpha Knight"),
            Manager("Mahfuz", "X-Mafias Return")
        ]
        
        # Add manager-players to their teams immediately
        imtiaz_player = Player("Imtiaz", 0, "MANAGER")  # Manager as player with 0 cost
        imtiaz_player.sold_price = 0
        imtiaz_player.sold_to = "Imtiaz"
        imtiaz_player.is_sold = True
        self.managers[0].add_player(imtiaz_player)
        
        ifthekhar_player = Player("Ifthekhar", 0, "MANAGER")  # Manager as player with 0 cost
        ifthekhar_player.sold_price = 0
        ifthekhar_player.sold_to = "Ifthekhar"
        ifthekhar_player.is_sold = True
        self.managers[1].add_player(ifthekhar_player)
        
        # Track category rotation (start with Tiger)
        self.next_category = "TIGER"
    
    def setup_gui(self):
        """Create the main GUI layout"""
        
        # Title
        title_frame = tk.Frame(self.root, bg='black')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🏏 CRICKET POTSDAM 🏏",
            font=("Arial", 28, "bold"),
            fg='gold',
            bg='black'
        )
        title_label.pack()
        
        # Current auction section
        self.auction_frame = tk.Frame(self.root, bg='black', relief=tk.RAISED, bd=2)
        self.auction_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.setup_auction_section()
        
        # Teams section
        teams_frame = tk.Frame(self.root, bg='black')
        teams_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.setup_teams_section(teams_frame)
        
        # Control buttons
        self.setup_control_buttons()
    
    def setup_auction_section(self):
        """Create the current auction display"""
        
        # Player info
        player_info_frame = tk.Frame(self.auction_frame, bg='black')
        player_info_frame.pack(pady=10)
        
        self.player_name_label = tk.Label(
            player_info_frame,
            text="Click 'Next Player' to start auction",
            font=("Arial", 24, "bold"),
            fg='white',
            bg='black'
        )
        self.player_name_label.pack()
        
        self.player_details_label = tk.Label(
            player_info_frame,
            text="",
            font=("Arial", 16),
            fg='yellow',
            bg='black'
        )
        self.player_details_label.pack()
        
        # Current bid info
        bid_info_frame = tk.Frame(self.auction_frame, bg='black')
        bid_info_frame.pack(pady=10)
        
        self.current_bid_label = tk.Label(
            bid_info_frame,
            text="",
            font=("Arial", 18, "bold"),
            fg='lime',
            bg='black'
        )
        self.current_bid_label.pack()
        
        # Timer - removed as requested
        # self.timer_label was removed
        
        # Bidding buttons
        bidding_frame = tk.Frame(self.auction_frame, bg='black')
        bidding_frame.pack(pady=15)
        
        self.bid_buttons = []
        for i, manager in enumerate(self.managers):
            btn_frame = tk.Frame(bidding_frame, bg='black')
            btn_frame.pack(side=tk.LEFT, padx=20)
            
            # Manager name
            name_label = tk.Label(
                btn_frame,
                text=manager.name,
                font=("Arial", 12, "bold"),
                fg='lightgreen',
                bg='black'
            )
            name_label.pack()
            
            # Bid button (€10 increments)
            bid_btn = tk.Button(
                btn_frame,
                text="Bid +€10",
                font=("Arial", 14, "bold"),
                bg='darkblue',
                fg='white',
                width=12,
                height=2,
                command=lambda idx=i: self.place_bid(idx)
            )
            bid_btn.pack(pady=5)
            
            # Pass button
            pass_btn = tk.Button(
                btn_frame,
                text="Pass",
                font=("Arial", 12),
                bg='darkred',
                fg='white',
                width=12,
                command=lambda idx=i: self.pass_bid(idx)
            )
            pass_btn.pack()
            
            self.bid_buttons.append((bid_btn, pass_btn))
    
    def setup_teams_section(self, parent):
        """Create the teams display"""
        
        self.team_frames = []
        
        for i, manager in enumerate(self.managers):
            # Team frame
            team_frame = tk.Frame(parent, bg='darkgray', relief=tk.RAISED, bd=2)
            team_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            
            # Team header
            header_frame = tk.Frame(team_frame, bg='navy')
            header_frame.pack(fill=tk.X, pady=2)
            
            team_name_label = tk.Label(
                header_frame,
                text=manager.team_name,
                font=("Arial", 14, "bold"),
                fg='white',
                bg='navy'
            )
            team_name_label.pack(pady=5)
            
            manager_label = tk.Label(
                header_frame,
                text=f"Manager: {manager.name}",
                font=("Arial", 10),
                fg='lightgreen',
                bg='navy'
            )
            manager_label.pack()
            
            # Budget and stats
            stats_frame = tk.Frame(team_frame, bg='darkgray')
            stats_frame.pack(fill=tk.X, pady=5)
            
            budget_label = tk.Label(
                stats_frame,
                text=f"€{manager.budget} left",
                font=("Arial", 12, "bold"),
                fg='gold',
                bg='darkgray'
            )
            budget_label.pack()
            
            category_label = tk.Label(
                stats_frame,
                text=f"Players: {len(manager.players)}/7 | Tigers: {manager.tiger_count}/4 | Lions: {manager.lion_count}/3",
                font=("Arial", 10),
                fg='white',
                bg='darkgray'
            )
            category_label.pack()
            
            # Players list
            players_frame = tk.Frame(team_frame, bg='darkgray')
            players_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            players_listbox = tk.Listbox(
                players_frame,
                font=("Arial", 10),
                bg='white',
                fg='black',
                height=15
            )
            players_listbox.pack(fill=tk.BOTH, expand=True)
            
            self.team_frames.append({
                'frame': team_frame,
                'budget_label': budget_label,
                'category_label': category_label,
                'players_listbox': players_listbox
            })
    
    def setup_control_buttons(self):
        """Create control buttons"""
        
        control_frame = tk.Frame(self.root, bg='black')
        control_frame.pack(pady=20)
        
        # Next player button
        self.next_player_btn = tk.Button(
            control_frame,
            text="Next Player",
            font=("Arial", 16, "bold"),
            bg='green',
            fg='white',
            width=15,
            height=2,
            command=self.next_player
        )
        self.next_player_btn.pack(side=tk.LEFT, padx=10)
        
        # Sold button
        self.sold_btn = tk.Button(
            control_frame,
            text="SOLD!",
            font=("Arial", 16, "bold"),
            bg='orange',
            fg='white',
            width=15,
            height=2,
            command=self.sell_player,
            state=tk.DISABLED
        )
        self.sold_btn.pack(side=tk.LEFT, padx=10)
        
        # Unsold button
        self.unsold_btn = tk.Button(
            control_frame,
            text="UNSOLD",
            font=("Arial", 16, "bold"),
            bg='red',
            fg='white',
            width=15,
            height=2,
            command=self.mark_unsold,
            state=tk.DISABLED
        )
        self.unsold_btn.pack(side=tk.LEFT, padx=10)
        
        # Export button
        export_btn = tk.Button(
            control_frame,
            text="Export Teams",
            font=("Arial", 14),
            bg='purple',
            fg='white',
            width=15,
            height=2,
            command=self.export_teams
        )
        export_btn.pack(side=tk.LEFT, padx=10)
        
        # Reset button
        reset_btn = tk.Button(
            control_frame,
            text="Reset Auction",
            font=("Arial", 14),
            bg='darkred',
            fg='white',
            width=15,
            height=2,
            command=self.reset_auction
        )
        reset_btn.pack(side=tk.LEFT, padx=10)
    
    def next_player(self):
        """Select the next player for auction"""
        
        # First check if we have unsold players to retry
        if self.unsold_players:
            self.current_player = self.unsold_players.pop(0)
        else:
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
                # Check if all teams have 7 players
                all_teams_full = all(len(manager.players) >= 7 for manager in self.managers)
                if all_teams_full:
                    messagebox.showinfo("Auction Complete", "All teams have 7 players! Auction complete!")
                else:
                    messagebox.showinfo("Players Needed", "Some teams still need players, but no more players available!")
                return
        
        # Reset bidding state - start with base price
        self.current_bid = self.current_player.base_price
        self.highest_bidder = None
        self.bidding_active = True
        
        # Update display
        self.update_auction_display()
        self.update_bid_buttons()
        
        # Enable sold and unsold buttons
        self.sold_btn.config(state=tk.NORMAL)
        self.unsold_btn.config(state=tk.NORMAL)
    
    def update_auction_display(self):
        """Update the current auction display"""
        
        if self.current_player:
            self.player_name_label.config(
                text=f"{self.current_player.name}",
                fg='white'
            )
            
            category_color = 'orange' if self.current_player.category == 'TIGER' else 'cyan'
            self.player_details_label.config(
                text=f"Category: {self.current_player.category} | Base Price: €{self.current_player.base_price}",
                fg=category_color
            )
            
            bidder_text = f" - {self.highest_bidder.name}" if self.highest_bidder else ""
            self.current_bid_label.config(
                text=f"Current Bid: €{self.current_bid}{bidder_text}"
            )
    
    def update_bid_buttons(self):
        """Update bid button states"""
        
        if not self.current_player or not self.bidding_active:
            for bid_btn, pass_btn in self.bid_buttons:
                bid_btn.config(state=tk.DISABLED)
                pass_btn.config(state=tk.DISABLED)
            return
        
        next_bid = self.current_bid + 10  # €10 increments
        
        for i, (bid_btn, pass_btn) in enumerate(self.bid_buttons):
            manager = self.managers[i]
            
            if manager.can_bid(next_bid, self.current_player.category):
                bid_btn.config(state=tk.NORMAL, text=f"Bid €{next_bid}")
                pass_btn.config(state=tk.NORMAL)
            else:
                bid_btn.config(state=tk.DISABLED, text="Cannot Bid")
                pass_btn.config(state=tk.DISABLED)
    
    def place_bid(self, manager_idx):
        """Place a bid for a manager"""
        
        if not self.bidding_active or not self.current_player:
            return
        
        manager = self.managers[manager_idx]
        new_bid = self.current_bid + 10  # €10 increments
        
        if manager.can_bid(new_bid, self.current_player.category):
            self.current_bid = new_bid
            self.highest_bidder = manager
            
            self.update_auction_display()
            self.update_bid_buttons()
            
            # Play sound effect
            if self.sound_enabled:
                try:
                    # You can add a sound file here
                    pass
                except:
                    pass
    
    def pass_bid(self, manager_idx):
        """Manager passes on current bid"""
        pass  # For now, just let the timer run out
    
    def sell_player(self):
        """Sell the current player to highest bidder or at base price"""
        
        if not self.current_player:
            return
        
        # If no one has bid yet, allow base price purchase by any eligible manager
        if self.highest_bidder is None:
            # Check if any manager can buy at base price
            eligible_managers = []
            for manager in self.managers:
                if manager.can_bid(self.current_player.base_price, self.current_player.category):
                    eligible_managers.append(manager)
            
            if len(eligible_managers) == 0:
                messagebox.showwarning("No Eligible Managers", "No manager can afford this player!")
                return
            elif len(eligible_managers) == 1:
                # Only one manager can afford - sell at base price
                self.highest_bidder = eligible_managers[0]
                self.current_bid = self.current_player.base_price
                messagebox.showinfo("Base Price Sale", f"{self.current_player.name} sold to {self.highest_bidder.name} at base price €{self.current_bid}!")
            else:
                # Multiple managers can afford - they need to bid
                messagebox.showwarning("Multiple Bidders Possible", "Multiple managers can afford this player. Please have them bid!")
                return
        
        # Finalize the sale
        self.current_player.sold_price = self.current_bid
        self.current_player.sold_to = self.highest_bidder.name
        self.current_player.is_sold = True
        
        self.highest_bidder.add_player(self.current_player)
        self.sold_players.append(self.current_player)
        
        # Update displays
        self.update_teams_display()
        
        # Reset auction state
        self.bidding_active = False
        sold_player_name = self.current_player.name
        sold_to = self.highest_bidder.name
        sold_price = self.current_bid
        self.current_player = None
        self.sold_btn.config(state=tk.DISABLED)
        self.unsold_btn.config(state=tk.DISABLED)
        self.update_bid_buttons()
        
        # Clear auction display
        self.player_name_label.config(text="Click 'Next Player' for next auction")
        self.player_details_label.config(text="")
        self.current_bid_label.config(text="")
        
        messagebox.showinfo("Player Sold!", f"{sold_player_name} sold to {sold_to} for €{sold_price}!")
    
    def update_teams_display(self):
        """Update all team displays"""
        
        for i, manager in enumerate(self.managers):
            # Update budget and stats
            self.team_frames[i]['budget_label'].config(text=f"€{manager.budget} left")
            self.team_frames[i]['category_label'].config(
                text=f"Players: {len(manager.players)}/7 | Tigers: {manager.tiger_count}/4 | Lions: {manager.lion_count}/3"
            )
            
            # Update players list
            listbox = self.team_frames[i]['players_listbox']
            listbox.delete(0, tk.END)
            
            for player in manager.players:
                listbox.insert(tk.END, f"{player.name} ({player.category}) - €{player.sold_price}")
    
    def export_teams(self):
        """Export team data to CSV"""
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Teams"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(["Team", "Manager", "Budget Left", "Player", "Category", "Price"])
                
                # Write team data
                for manager in self.managers:
                    if manager.players:
                        for player in manager.players:
                            writer.writerow([
                                manager.team_name,
                                manager.name,
                                manager.budget,
                                player.name,
                                player.category,
                                player.sold_price
                            ])
                    else:
                        writer.writerow([
                            manager.team_name,
                            manager.name,
                            manager.budget,
                            "No players",
                            "",
                            ""
                        ])
                
                # Write summary
                writer.writerow([])
                writer.writerow(["AUCTION SUMMARY"])
                writer.writerow(["Total Players Sold", len(self.sold_players)])
                writer.writerow(["Tigers Remaining", len(self.tiger_pool)])
                writer.writerow(["Lions Remaining", len(self.lion_pool)])
            
            messagebox.showinfo("Export Complete", f"Teams exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def reset_auction(self):
        """Reset the entire auction"""
        
        result = messagebox.askyesno(
            "Reset Auction",
            "Are you sure you want to reset the entire auction? This will clear all bids and teams."
        )
        
        if result:
            # Reset all data
            self.setup_data()
            
            # Clear displays
            self.current_player = None
            self.current_bid = 0
            self.highest_bidder = None
            self.bidding_active = False
            
            # Update UI
            self.player_name_label.config(text="Click 'Next Player' to start auction")
            self.player_details_label.config(text="")
            self.current_bid_label.config(text="")
            
            self.update_teams_display()
            self.update_bid_buttons()
            self.sold_btn.config(state=tk.DISABLED)
            self.unsold_btn.config(state=tk.DISABLED)
    
    def mark_unsold(self):
        """Mark current player as unsold and add to unsold players list"""
        
        if not self.current_player:
            return
        
        # Add player back to unsold list for re-auction
        self.unsold_players.append(self.current_player)
        
        # Reset auction state
        self.bidding_active = False
        current_player_name = self.current_player.name
        self.current_player = None
        self.sold_btn.config(state=tk.DISABLED)
        self.unsold_btn.config(state=tk.DISABLED)
        self.update_bid_buttons()
        
        # Clear auction display
        self.player_name_label.config(text="Click 'Next Player' for next auction")
        self.player_details_label.config(text="")
        self.current_bid_label.config(text="")
        
        messagebox.showinfo("Player Unsold", f"{current_player_name} will be re-auctioned later!")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = AuctionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
