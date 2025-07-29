#!/usr/bin/env python3
"""
Universal Sports Auction - Live Player Bidding App
A tkinter-based auction system for fantasy sports player drafts
Supports customizable teams, categories, and player configurations
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import random
import csv
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

# Optional pygame import for sound effects
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class Player:
    """Represents a player in the auction"""
    
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
    
    def __init__(self, name: str, team_name: str, budget: int, max_players: int, category_limits: Dict[str, int]):
        self.name = name
        self.team_name = team_name
        self.budget = budget
        self.initial_budget = budget
        self.max_players = max_players
        self.category_limits = category_limits.copy()
        self.players: List[Player] = []
        self.category_counts: Dict[str, int] = {cat: 0 for cat in category_limits.keys()}
    
    def can_bid(self, amount: int, category: str) -> bool:
        """Check if manager can place this bid"""
        if amount > self.budget:
            return False
        
        # Check player limit
        if len(self.players) >= self.max_players:
            return False
        
        # Check category limit
        if category in self.category_limits:
            if self.category_counts[category] >= self.category_limits[category]:
                return False
        
        return True
    
    def add_player(self, player: Player):
        """Add a player to the manager's team"""
        self.players.append(player)
        self.budget -= player.sold_price
        
        if player.category in self.category_counts:
            self.category_counts[player.category] += 1
    
    def remove_player(self, player: Player):
        """Remove a player from the manager's team"""
        if player in self.players:
            self.players.remove(player)
            self.budget += player.sold_price
            
            if player.category in self.category_counts:
                self.category_counts[player.category] -= 1
    
    def get_budget_left(self) -> int:
        return self.budget
    
    def get_total_spent(self) -> int:
        return self.initial_budget - self.budget
    
    def get_team_summary(self) -> str:
        """Get formatted team summary"""
        summary = f"{self.team_name}\nManager: {self.name}\n€{self.budget} left\n"
        
        # Category counts
        for category, count in self.category_counts.items():
            limit = self.category_limits.get(category, 0)
            summary += f"{category}: {count}/{limit}, "
        summary = summary.rstrip(", ") + "\n\n"
        
        for player in self.players:
            summary += f"{player.name} ({player.category}) - €{player.sold_price}\n"
        
        return summary


class AuctionConfig:
    """Configuration for the auction"""
    
    def __init__(self):
        self.title = "Sports Auction"
        self.total_budget = 2000
        self.bid_increment = 10
        self.max_players = 7
        self.teams: List[Dict[str, str]] = []
        self.categories: List[Dict[str, Any]] = []
        self.players: List[Dict[str, Any]] = []
        self.is_configured = False


class SetupWindow:
    """Setup configuration window for the auction"""
    
    def __init__(self, parent):
        self.parent = parent
        self.config = AuctionConfig()
        
        # Create setup window
        self.window = tk.Toplevel(parent.root)
        self.window.title("Auction Setup")
        self.window.configure(bg='#1a1a3a')
        self.window.geometry('900x700')
        self.window.grab_set()  # Make modal
        
        # Center the window on screen
        self.center_window()
        
        self.setup_gui()
        
        # Make window transient and wait
        self.window.transient(parent.root)
        self.window.wait_window()
    
    def center_window(self):
        """Center the window on the screen"""
        self.window.update_idletasks()  # Ensure window dimensions are calculated
        
        # Get window dimensions
        window_width = 900
        window_height = 700
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate position for center
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window position
        self.window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Make window resizable but set minimum size
        self.window.minsize(800, 600)
        self.window.maxsize(1200, 900)
    
    def setup_gui(self):
        """Create the setup interface"""
        
        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TNotebook', background='#1a1a3a')
        style.configure('Custom.TNotebook.Tab', background='#2d1b69', foreground='white', padding=[20, 10])
        
        notebook = ttk.Notebook(self.window, style='Custom.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Basic Configuration Tab
        basic_frame = tk.Frame(notebook, bg='#1a1a3a')
        notebook.add(basic_frame, text="Basic Config")
        self.setup_basic_config(basic_frame)
        
        # Teams Tab
        teams_frame = tk.Frame(notebook, bg='#1a1a3a')
        notebook.add(teams_frame, text="Teams")
        self.setup_teams_config(teams_frame)
        
        # Categories Tab
        categories_frame = tk.Frame(notebook, bg='#1a1a3a')
        notebook.add(categories_frame, text="Categories")
        self.setup_categories_config(categories_frame)
        
        # Players Tab
        players_frame = tk.Frame(notebook, bg='#1a1a3a')
        notebook.add(players_frame, text="Players")
        self.setup_players_config(players_frame)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#1a1a3a')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            button_frame,
            text="Load Configuration",
            font=("Arial", 12),
            bg='#6366f1',
            fg='white',
            command=self.load_config
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Save Configuration",
            font=("Arial", 12),
            bg='#8b5cf6',
            fg='white',
            command=self.save_config
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Start Auction",
            font=("Arial", 14, "bold"),
            bg='#10b981',
            fg='white',
            command=self.start_auction
        ).pack(side=tk.RIGHT, padx=5)
    
    def setup_basic_config(self, parent):
        """Setup basic configuration tab"""
        
        title_frame = tk.Frame(parent, bg='#1a1a3a')
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            title_frame,
            text="⚙️ Basic Configuration",
            font=("Arial", 16, "bold"),
            fg='#ffd700',
            bg='#1a1a3a'
        ).pack()
        
        # Configuration fields
        config_frame = tk.Frame(parent, bg='#1a1a3a')
        config_frame.pack(fill=tk.X, padx=40, pady=20)
        
        # Title
        tk.Label(config_frame, text="Auction Title:", font=("Arial", 12), fg='white', bg='#1a1a3a').grid(row=0, column=0, sticky='w', pady=5)
        self.title_entry = tk.Entry(config_frame, font=("Arial", 12), width=30)
        self.title_entry.insert(0, "Sports Championship Auction")
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Budget
        tk.Label(config_frame, text="Budget per Team (€):", font=("Arial", 12), fg='white', bg='#1a1a3a').grid(row=1, column=0, sticky='w', pady=5)
        self.budget_var = tk.IntVar(value=2000)
        budget_spin = tk.Spinbox(config_frame, from_=500, to=10000, increment=100, textvariable=self.budget_var, font=("Arial", 12), width=28)
        budget_spin.grid(row=1, column=1, padx=10, pady=5)
        
        # Bid increment
        tk.Label(config_frame, text="Bid Increment (€):", font=("Arial", 12), fg='white', bg='#1a1a3a').grid(row=2, column=0, sticky='w', pady=5)
        self.increment_var = tk.IntVar(value=10)
        increment_spin = tk.Spinbox(config_frame, from_=5, to=100, increment=5, textvariable=self.increment_var, font=("Arial", 12), width=28)
        increment_spin.grid(row=2, column=1, padx=10, pady=5)
        
        # Max players
        tk.Label(config_frame, text="Max Players per Team:", font=("Arial", 12), fg='white', bg='#1a1a3a').grid(row=3, column=0, sticky='w', pady=5)
        self.max_players_var = tk.IntVar(value=7)
        players_spin = tk.Spinbox(config_frame, from_=5, to=15, textvariable=self.max_players_var, font=("Arial", 12), width=28)
        players_spin.grid(row=3, column=1, padx=10, pady=5)
    
    def setup_teams_config(self, parent):
        """Setup teams configuration tab"""
        
        title_frame = tk.Frame(parent, bg='#1a1a3a')
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            title_frame,
            text="👥 Team Configuration",
            font=("Arial", 16, "bold"),
            fg='#ffd700',
            bg='#1a1a3a'
        ).pack()
        
        # Number of teams
        control_frame = tk.Frame(parent, bg='#1a1a3a')
        control_frame.pack(fill=tk.X, padx=40, pady=10)
        
        tk.Label(control_frame, text="Number of Teams:", font=("Arial", 12), fg='white', bg='#1a1a3a').pack(side=tk.LEFT)
        self.num_teams_var = tk.IntVar(value=3)
        teams_spin = tk.Spinbox(control_frame, from_=2, to=8, textvariable=self.num_teams_var, font=("Arial", 12), width=5)
        teams_spin.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            control_frame,
            text="Generate Team Fields",
            font=("Arial", 12),
            bg='#4f46e5',
            fg='white',
            command=self.generate_team_fields
        ).pack(side=tk.LEFT, padx=20)
        
        # Teams frame
        self.teams_canvas_frame = tk.Frame(parent, bg='#1a1a3a')
        self.teams_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        self.generate_team_fields()
    
    def setup_categories_config(self, parent):
        """Setup categories configuration tab"""
        
        title_frame = tk.Frame(parent, bg='#1a1a3a')
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            title_frame,
            text="📋 Category Configuration",
            font=("Arial", 16, "bold"),
            fg='#ffd700',
            bg='#1a1a3a'
        ).pack()
        
        # Number of categories
        control_frame = tk.Frame(parent, bg='#1a1a3a')
        control_frame.pack(fill=tk.X, padx=40, pady=10)
        
        tk.Label(control_frame, text="Number of Categories:", font=("Arial", 12), fg='white', bg='#1a1a3a').pack(side=tk.LEFT)
        self.num_categories_var = tk.IntVar(value=2)
        categories_spin = tk.Spinbox(control_frame, from_=1, to=5, textvariable=self.num_categories_var, font=("Arial", 12), width=5)
        categories_spin.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            control_frame,
            text="Generate Category Fields",
            font=("Arial", 12),
            bg='#4f46e5',
            fg='white',
            command=self.generate_category_fields
        ).pack(side=tk.LEFT, padx=20)
        
        # Categories frame
        self.categories_canvas_frame = tk.Frame(parent, bg='#1a1a3a')
        self.categories_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        self.generate_category_fields()
    
    def setup_players_config(self, parent):
        """Setup players configuration tab"""
        
        title_frame = tk.Frame(parent, bg='#1a1a3a')
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            title_frame,
            text="🏃‍♂️ Player Management",
            font=("Arial", 16, "bold"),
            fg='#ffd700',
            bg='#1a1a3a'
        ).pack()
        
        # Add player form
        form_frame = tk.Frame(parent, bg='#2d1b69', relief=tk.RAISED, bd=2)
        form_frame.pack(fill=tk.X, padx=40, pady=10)
        
        tk.Label(form_frame, text="Add New Player", font=("Arial", 14, "bold"), fg='#ffd700', bg='#2d1b69').pack(pady=10)
        
        fields_frame = tk.Frame(form_frame, bg='#2d1b69')
        fields_frame.pack(padx=20, pady=10)
        
        # Player name
        tk.Label(fields_frame, text="Name:", font=("Arial", 12), fg='white', bg='#2d1b69').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.player_name_entry = tk.Entry(fields_frame, font=("Arial", 12), width=20)
        self.player_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Base price
        tk.Label(fields_frame, text="Base Price (€):", font=("Arial", 12), fg='white', bg='#2d1b69').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.player_price_entry = tk.Entry(fields_frame, font=("Arial", 12), width=15)
        self.player_price_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Category
        tk.Label(fields_frame, text="Category:", font=("Arial", 12), fg='white', bg='#2d1b69').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.player_category_var = tk.StringVar()
        self.player_category_combo = ttk.Combobox(fields_frame, textvariable=self.player_category_var, font=("Arial", 12), width=17, state="readonly")
        self.player_category_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(
            fields_frame,
            text="Add Player",
            font=("Arial", 12, "bold"),
            bg='#10b981',
            fg='white',
            command=self.add_player
        ).grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
        # Players list
        list_frame = tk.Frame(parent, bg='#1a1a3a')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        tk.Label(list_frame, text="Players List", font=("Arial", 14, "bold"), fg='white', bg='#1a1a3a').pack()
        
        # Create treeview for players
        columns = ('Name', 'Category', 'Base Price')
        self.players_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.players_tree.heading(col, text=col)
            self.players_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.players_tree.yview)
        self.players_tree.configure(yscroll=scrollbar.set)
        
        self.players_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Delete button
        tk.Button(
            list_frame,
            text="Remove Selected Player",
            font=("Arial", 12),
            bg='#ef4444',
            fg='white',
            command=self.remove_selected_player
        ).pack(pady=10)
    
    def generate_team_fields(self):
        """Generate input fields for teams"""
        
        # Clear existing widgets
        for widget in self.teams_canvas_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame for teams
        canvas = tk.Canvas(self.teams_canvas_frame, bg='#1a1a3a', highlightthickness=0, height=300)
        scrollbar = ttk.Scrollbar(self.teams_canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a3a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Generate team entry fields
        self.team_entries = []
        num_teams = self.num_teams_var.get()
        
        for i in range(num_teams):
            team_frame = tk.Frame(scrollable_frame, bg='#2d1b69', relief=tk.RAISED, bd=1)
            team_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(team_frame, text=f"Team {i+1}", font=("Arial", 12, "bold"), fg='#ffd700', bg='#2d1b69').grid(row=0, column=0, columnspan=2, pady=5)
            
            tk.Label(team_frame, text="Team Name:", font=("Arial", 10), fg='white', bg='#2d1b69').grid(row=1, column=0, sticky='w', padx=5, pady=2)
            team_entry = tk.Entry(team_frame, font=("Arial", 10), width=25)
            team_entry.insert(0, f"Team {i+1}")
            team_entry.grid(row=1, column=1, padx=5, pady=2)
            
            tk.Label(team_frame, text="Manager Name:", font=("Arial", 10), fg='white', bg='#2d1b69').grid(row=2, column=0, sticky='w', padx=5, pady=2)
            manager_entry = tk.Entry(team_frame, font=("Arial", 10), width=25)
            manager_entry.insert(0, f"Manager {i+1}")
            manager_entry.grid(row=2, column=1, padx=5, pady=2)
            
            self.team_entries.append((team_entry, manager_entry))
    
    def generate_category_fields(self):
        """Generate input fields for categories"""
        
        # Clear existing widgets
        for widget in self.categories_canvas_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame for categories
        canvas = tk.Canvas(self.categories_canvas_frame, bg='#1a1a3a', highlightthickness=0, height=200)
        scrollbar = ttk.Scrollbar(self.categories_canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a3a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Generate category entry fields
        self.category_entries = []
        num_categories = self.num_categories_var.get()
        
        default_categories = ["Premium", "Standard", "Budget", "Special", "Reserve"]
        
        for i in range(num_categories):
            cat_frame = tk.Frame(scrollable_frame, bg='#2d1b69', relief=tk.RAISED, bd=1)
            cat_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(cat_frame, text=f"Category {i+1}", font=("Arial", 12, "bold"), fg='#ffd700', bg='#2d1b69').grid(row=0, column=0, columnspan=2, pady=5)
            
            tk.Label(cat_frame, text="Category Name:", font=("Arial", 10), fg='white', bg='#2d1b69').grid(row=1, column=0, sticky='w', padx=5, pady=2)
            cat_entry = tk.Entry(cat_frame, font=("Arial", 10), width=20)
            if i < len(default_categories):
                cat_entry.insert(0, default_categories[i])
            else:
                cat_entry.insert(0, f"Category {i+1}")
            cat_entry.grid(row=1, column=1, padx=5, pady=2)
            cat_entry.bind('<KeyRelease>', lambda e: self.update_player_categories())
            
            tk.Label(cat_frame, text="Max per Team:", font=("Arial", 10), fg='white', bg='#2d1b69').grid(row=2, column=0, sticky='w', padx=5, pady=2)
            max_var = tk.IntVar(value=3)
            max_spin = tk.Spinbox(cat_frame, from_=1, to=10, textvariable=max_var, font=("Arial", 10), width=18)
            max_spin.grid(row=2, column=1, padx=5, pady=2)
            
            self.category_entries.append((cat_entry, max_var))
        
        # Update player category dropdown
        self.update_player_categories()
    
    def update_player_categories(self):
        """Update the player category dropdown"""
        if hasattr(self, 'player_category_combo'):
            categories = []
            for cat_entry, _ in self.category_entries:
                cat_name = cat_entry.get().strip()
                if cat_name:
                    categories.append(cat_name)
            
            self.player_category_combo['values'] = categories
            if categories and not self.player_category_var.get():
                self.player_category_var.set(categories[0])
    
    def add_player(self):
        """Add a player to the list"""
        name = self.player_name_entry.get().strip()
        price_str = self.player_price_entry.get().strip()
        category = self.player_category_var.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter a player name.")
            return
        
        try:
            price = int(price_str)
            if price < 10:
                raise ValueError("Price too low")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price (minimum €10).")
            return
        
        if not category:
            messagebox.showerror("Error", "Please select a category.")
            return
        
        # Check if player already exists
        for item in self.players_tree.get_children():
            values = self.players_tree.item(item)['values']
            if values[0].lower() == name.lower():
                messagebox.showerror("Error", "A player with this name already exists.")
                return
        
        # Add to tree
        self.players_tree.insert('', tk.END, values=(name, category, f"€{price}"))
        
        # Clear form
        self.player_name_entry.delete(0, tk.END)
        self.player_price_entry.delete(0, tk.END)
    
    def remove_selected_player(self):
        """Remove selected player from the list"""
        selected = self.players_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a player to remove.")
            return
        
        item = selected[0]
        player_name = self.players_tree.item(item)['values'][0]
        
        if messagebox.askyesno("Confirm", f"Remove {player_name} from the player list?"):
            self.players_tree.delete(item)
    
    def save_config(self):
        """Save current configuration to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Configuration"
        )
        
        if not filename:
            return
        
        try:
            config_data = self.get_current_config()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Configuration saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def load_config(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Configuration"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            self.load_config_data(config_data)
            messagebox.showinfo("Success", f"Configuration loaded from {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
    
    def get_current_config(self):
        """Get current configuration as dictionary"""
        config = {
            'title': self.title_entry.get(),
            'total_budget': self.budget_var.get(),
            'bid_increment': self.increment_var.get(),
            'max_players': self.max_players_var.get(),
            'teams': [],
            'categories': [],
            'players': []
        }
        
        # Teams
        for team_entry, manager_entry in self.team_entries:
            config['teams'].append({
                'team_name': team_entry.get(),
                'manager_name': manager_entry.get()
            })
        
        # Categories
        for cat_entry, max_var in self.category_entries:
            config['categories'].append({
                'name': cat_entry.get(),
                'max_per_team': max_var.get()
            })
        
        # Players
        for item in self.players_tree.get_children():
            values = self.players_tree.item(item)['values']
            price_str = values[2].replace('€', '')
            config['players'].append({
                'name': values[0],
                'category': values[1],
                'price': int(price_str)
            })
        
        return config
    
    def load_config_data(self, config_data):
        """Load configuration data into the interface"""
        
        # Basic config
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, config_data.get('title', 'Sports Auction'))
        self.budget_var.set(config_data.get('total_budget', 2000))
        self.increment_var.set(config_data.get('bid_increment', 10))
        self.max_players_var.set(config_data.get('max_players', 7))
        
        # Teams
        teams_data = config_data.get('teams', [])
        self.num_teams_var.set(len(teams_data))
        self.generate_team_fields()
        
        for i, team_data in enumerate(teams_data):
            if i < len(self.team_entries):
                team_entry, manager_entry = self.team_entries[i]
                team_entry.delete(0, tk.END)
                team_entry.insert(0, team_data.get('team_name', ''))
                manager_entry.delete(0, tk.END)
                manager_entry.insert(0, team_data.get('manager_name', ''))
        
        # Categories
        categories_data = config_data.get('categories', [])
        self.num_categories_var.set(len(categories_data))
        self.generate_category_fields()
        
        for i, cat_data in enumerate(categories_data):
            if i < len(self.category_entries):
                cat_entry, max_var = self.category_entries[i]
                cat_entry.delete(0, tk.END)
                cat_entry.insert(0, cat_data.get('name', ''))
                max_var.set(cat_data.get('max_per_team', 3))
        
        # Players
        self.players_tree.delete(*self.players_tree.get_children())
        for player_data in config_data.get('players', []):
            self.players_tree.insert('', tk.END, values=(
                player_data.get('name', ''),
                player_data.get('category', ''),
                f"€{player_data.get('price', 0)}"
            ))
    
    def start_auction(self):
        """Validate configuration and start auction"""
        
        # Get current configuration
        config_data = self.get_current_config()
        
        # Validate
        if not config_data['title']:
            messagebox.showerror("Error", "Please enter an auction title.")
            return
        
        if not config_data['teams']:
            messagebox.showerror("Error", "Please add at least one team.")
            return
        
        if not config_data['categories']:
            messagebox.showerror("Error", "Please add at least one category.")
            return
        
        if not config_data['players']:
            messagebox.showerror("Error", "Please add at least one player.")
            return
        
        # Validate team names
        for team in config_data['teams']:
            if not team['team_name'].strip() or not team['manager_name'].strip():
                messagebox.showerror("Error", "Please fill in all team and manager names.")
                return
        
        # Validate categories
        for category in config_data['categories']:
            if not category['name'].strip():
                messagebox.showerror("Error", "Please fill in all category names.")
                return
        
        # Set configuration
        self.config.title = config_data['title']
        self.config.total_budget = config_data['total_budget']
        self.config.bid_increment = config_data['bid_increment']
        self.config.max_players = config_data['max_players']
        self.config.teams = config_data['teams']
        self.config.categories = config_data['categories']
        self.config.players = config_data['players']
        self.config.is_configured = True
        
        # Close setup window
        self.window.destroy()


class AuctionApp:
    """Main auction application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Sports Auction")
        self.root.configure(bg='#1a1a3a')
        
        # Set window to be resizable and centered
        self.center_main_window()
        
        # Initialize pygame for sound effects (optional)
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.sound_enabled = True
            except:
                self.sound_enabled = False
        else:
            self.sound_enabled = False
        
        # Initialize auction state
        self.config = None
        self.managers = {}
        self.player_pool = []
        self.current_player = None
        self.current_bid = 0
        self.highest_bidder = None
        self.bidding_active = False
        self.sold_players = []
        self.unsold_players = []
        
        # Show setup window first
        self.show_setup()
    
    def center_main_window(self):
        """Center and size the main auction window"""
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window size (80% of screen but not too small)
        window_width = max(1200, int(screen_width * 0.8))
        window_height = max(800, int(screen_height * 0.8))
        
        # Calculate position for center
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window geometry
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Set minimum and maximum sizes
        self.root.minsize(1000, 700)
        self.root.maxsize(screen_width, screen_height)
        
        # Make window state maximized if screen is large enough
        if screen_width >= 1920 and screen_height >= 1080:
            self.root.state('zoomed')  # Fullscreen on Windows
    
    def show_setup(self):
        """Show setup configuration window"""
        setup_window = SetupWindow(self)
        
        if setup_window.config.is_configured:
            self.config = setup_window.config
            self.initialize_auction()
            self.setup_gui()
        else:
            # User cancelled setup, close application
            self.root.quit()
    
    def initialize_auction(self):
        """Initialize auction with configuration"""
        
        # Create managers
        self.managers = {}
        
        # Calculate category limits
        category_limits = {cat['name']: cat['max_per_team'] for cat in self.config.categories}
        
        for team in self.config.teams:
            manager = Manager(
                name=team['manager_name'],
                team_name=team['team_name'],
                budget=self.config.total_budget,
                max_players=self.config.max_players,
                category_limits=category_limits
            )
            self.managers[team['manager_name']] = manager
        
        # Create player pool with Fisher-Yates shuffle for better randomization
        self.player_pool = []
        for player_data in self.config.players:
            player = Player(
                name=player_data['name'],
                base_price=player_data['price'],
                category=player_data['category']
            )
            self.player_pool.append(player)
        
        # Shuffle with Fisher-Yates algorithm
        for i in range(len(self.player_pool) - 1, 0, -1):
            j = random.randint(0, i)
            self.player_pool[i], self.player_pool[j] = self.player_pool[j], self.player_pool[i]
    
    def setup_gui(self):
        """Create the main GUI layout"""
        
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Update window title
        self.root.title(f"{self.config.title} - Universal Sports Auction")
        
        # Create main frame with scrolling
        main_canvas = tk.Canvas(self.root, bg='#1a1a3a', highlightthickness=0)
        main_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = tk.Frame(main_canvas, bg='#1a1a3a')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Title section
        self.setup_title_section()
        
        # Status section
        self.setup_status_section()
        
        # Current auction section
        self.setup_auction_section()
        
        # Control buttons
        self.setup_control_buttons()
        
        # Teams section
        self.setup_teams_section()
        
        # Initialize display
        self.update_display()
    
    def setup_title_section(self):
        """Create the title section"""
        title_frame = tk.Frame(self.scrollable_frame, bg='#1a1a3a')
        title_frame.pack(pady=30, padx=20, fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text=f"🏆 {self.config.title.upper()} 🏆",
            font=("Arial", 32, "bold"),
            fg='#ffd700',
            bg='#1a1a3a'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Universal Live Bidding System",
            font=("Arial", 16),
            fg='#a0a9c0',
            bg='#1a1a3a'
        )
        subtitle_label.pack(pady=(5, 0))
    
    def setup_status_section(self):
        """Create the status section"""
        self.status_frame = tk.Frame(self.scrollable_frame, bg='#2d1b69', relief=tk.RAISED, bd=2)
        self.status_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Initializing auction...",
            font=("Arial", 14),
            fg='#a0a9c0',
            bg='#2d1b69'
        )
        self.status_label.pack(pady=15)
    
    def setup_auction_section(self):
        """Create the current auction display"""
        
        self.auction_frame = tk.Frame(self.scrollable_frame, bg='#2d1b69', relief=tk.RAISED, bd=2)
        self.auction_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Player info
        player_info_frame = tk.Frame(self.auction_frame, bg='#2d1b69')
        player_info_frame.pack(pady=20)
        
        self.player_name_label = tk.Label(
            player_info_frame,
            text="Click 'Next Player' to start auction",
            font=("Arial", 28, "bold"),
            fg='white',
            bg='#2d1b69'
        )
        self.player_name_label.pack()
        
        self.player_details_label = tk.Label(
            player_info_frame,
            text="",
            font=("Arial", 16),
            fg='#ffd700',
            bg='#2d1b69'
        )
        self.player_details_label.pack()
        
        # Current bid info
        bid_info_frame = tk.Frame(self.auction_frame, bg='#2d1b69')
        bid_info_frame.pack(pady=15)
        
        self.current_bid_label = tk.Label(
            bid_info_frame,
            text="",
            font=("Arial", 20, "bold"),
            fg='#10b981',
            bg='#2d1b69'
        )
        self.current_bid_label.pack()
        
        # Bidding buttons frame
        self.bidding_frame = tk.Frame(self.auction_frame, bg='#2d1b69')
        self.bidding_frame.pack(pady=20)
        
        self.setup_bidding_buttons()
    
    def setup_bidding_buttons(self):
        """Create bidding buttons for each manager"""
        
        # Clear existing buttons
        for widget in self.bidding_frame.winfo_children():
            widget.destroy()
        
        self.bid_buttons = {}
        
        # Calculate grid layout
        num_managers = len(self.managers)
        cols = min(3, num_managers)  # Max 3 columns
        
        for i, (manager_name, manager) in enumerate(self.managers.items()):
            row = i // cols
            col = i % cols
            
            # Manager bid frame
            manager_frame = tk.Frame(self.bidding_frame, bg='#4f46e5', relief=tk.RAISED, bd=2)
            manager_frame.grid(row=row, column=col, padx=15, pady=10, sticky='ew')
            
            # Configure grid weights
            self.bidding_frame.grid_columnconfigure(col, weight=1)
            
            # Manager info
            tk.Label(
                manager_frame,
                text=manager.name,
                font=("Arial", 14, "bold"),
                fg='white',
                bg='#4f46e5'
            ).pack(pady=(10, 5))
            
            tk.Label(
                manager_frame,
                text=manager.team_name,
                font=("Arial", 10),
                fg='#e0e0e0',
                bg='#4f46e5'
            ).pack(pady=(0, 10))
            
            # Bid button
            bid_btn = tk.Button(
                manager_frame,
                text=f"Bid +€{self.config.bid_increment}",
                font=("Arial", 12, "bold"),
                bg='#10b981',
                fg='white',
                width=18,
                height=2,
                command=lambda m=manager_name: self.place_bid(m)
            )
            bid_btn.pack(pady=5)
            
            # Pass button
            pass_btn = tk.Button(
                manager_frame,
                text="Pass",
                font=("Arial", 10),
                bg='#ef4444',
                fg='white',
                width=18,
                command=lambda m=manager_name: self.pass_bid(m)
            )
            pass_btn.pack(pady=(0, 10))
            
            self.bid_buttons[manager_name] = {
                'bid': bid_btn,
                'pass': pass_btn,
                'frame': manager_frame
            }
    
    def setup_control_buttons(self):
        """Create control buttons"""
        
        control_frame = tk.Frame(self.scrollable_frame, bg='#1a1a3a')
        control_frame.pack(pady=30)
        
        # Create button grid
        button_data = [
            ("Next Player", "#10b981", self.next_player),
            ("SOLD!", "#ff8c42", self.sell_player),
            ("Buy at Base Price", "#8b5cf6", self.buy_at_base_price),
            ("UNSOLD", "#ef4444", self.mark_unsold),
            ("Export Results", "#6366f1", self.export_teams),
            ("Back to Setup", "#6b7280", self.back_to_setup)
        ]
        
        # Arrange buttons in 2 rows
        for i, (text, color, command) in enumerate(button_data):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                control_frame,
                text=text,
                font=("Arial", 14, "bold"),
                bg=color,
                fg='white',
                width=18,
                height=2,
                command=command
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
            
            # Store control buttons for state management
            if text == "SOLD!":
                self.sold_btn = btn
            elif text == "Buy at Base Price":
                self.base_price_btn = btn
            elif text == "UNSOLD":
                self.unsold_btn = btn
        
        # Initially disable some buttons
        self.sold_btn.config(state=tk.DISABLED)
        self.base_price_btn.config(state=tk.DISABLED)
        self.unsold_btn.config(state=tk.DISABLED)
    
    def setup_teams_section(self):
        """Create the teams display"""
        
        teams_title_frame = tk.Frame(self.scrollable_frame, bg='#1a1a3a')
        teams_title_frame.pack(pady=(30, 10), padx=20)
        
        tk.Label(
            teams_title_frame,
            text="🏆 TEAMS 🏆",
            font=("Arial", 24, "bold"),
            fg='#ffd700',
            bg='#1a1a3a'
        ).pack()
        
        # Teams container
        teams_container = tk.Frame(self.scrollable_frame, bg='#1a1a3a')
        teams_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.team_frames = {}
        
        # Calculate grid layout for teams
        num_teams = len(self.managers)
        cols = min(3, num_teams)  # Max 3 columns
        
        for i, (manager_name, manager) in enumerate(self.managers.items()):
            row = i // cols
            col = i % cols
            
            # Team frame
            team_frame = tk.Frame(teams_container, bg='#2d1b69', relief=tk.RAISED, bd=2)
            team_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            # Configure grid weights
            teams_container.grid_rowconfigure(row, weight=1)
            teams_container.grid_columnconfigure(col, weight=1)
            
            # Team header
            header_frame = tk.Frame(team_frame, bg='#4f46e5')
            header_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(
                header_frame,
                text=manager.team_name,
                font=("Arial", 16, "bold"),
                fg='white',
                bg='#4f46e5'
            ).pack(pady=10)
            
            tk.Label(
                header_frame,
                text=f"Manager: {manager.name}",
                font=("Arial", 12),
                fg='#e0e0e0',
                bg='#4f46e5'
            ).pack(pady=(0, 10))
            
            # Stats frame
            stats_frame = tk.Frame(team_frame, bg='#2d1b69')
            stats_frame.pack(fill=tk.X, pady=10)
            
            budget_label = tk.Label(
                stats_frame,
                text=f"€{manager.budget} left",
                font=("Arial", 14, "bold"),
                fg='#ffd700',
                bg='#2d1b69'
            )
            budget_label.pack()
            
            # Category stats
            category_text = f"Players: {len(manager.players)}/{manager.max_players}"
            for cat_name, count in manager.category_counts.items():
                limit = manager.category_limits.get(cat_name, 0)
                category_text += f" | {cat_name}: {count}/{limit}"
            
            category_label = tk.Label(
                stats_frame,
                text=category_text,
                font=("Arial", 10),
                fg='white',
                bg='#2d1b69'
            )
            category_label.pack()
            
            # Players list
            players_frame = tk.Frame(team_frame, bg='#2d1b69')
            players_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create scrollable text widget for players
            players_text = tk.Text(
                players_frame,
                font=("Arial", 10),
                bg='white',
                fg='black',
                height=12,
                width=30,
                wrap=tk.WORD
            )
            
            players_scrollbar = ttk.Scrollbar(players_frame, orient=tk.VERTICAL, command=players_text.yview)
            players_text.configure(yscrollcommand=players_scrollbar.set)
            
            players_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            players_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.team_frames[manager_name] = {
                'frame': team_frame,
                'budget_label': budget_label,
                'category_label': category_label,
                'players_text': players_text
            }
    
    def next_player(self):
        """Select the next player for auction"""
        
        try:
            current_player = None
            
            # First prioritize regular players from the main pool
            if self.player_pool:
                # Select random player from main pool
                random_index = random.randint(0, len(self.player_pool) - 1)
                current_player = self.player_pool.pop(random_index)
            elif self.unsold_players:
                # Only after all regular players are done, re-auction unsold players randomly
                random_index = random.randint(0, len(self.unsold_players) - 1)
                current_player = self.unsold_players.pop(random_index)
            else:
                # Check if all teams have enough players
                all_teams_complete = all(
                    len(manager.players) >= manager.max_players 
                    for manager in self.managers.values()
                )
                if all_teams_complete:
                    messagebox.showinfo("Auction Complete", "🎉 All teams are complete! Auction finished!")
                else:
                    messagebox.showinfo("Players Needed", "Some teams still need players, but no more players available!")
                return
            
            # Set current player
            self.current_player = current_player
            self.current_bid = current_player.base_price
            self.highest_bidder = None
            self.bidding_active = True
            
            # Update display
            self.update_display()
            self.update_bid_buttons()
            
            # Enable control buttons
            self.sold_btn.config(state=tk.NORMAL)
            self.base_price_btn.config(state=tk.NORMAL)
            self.unsold_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting next player: {str(e)}")
    
    def place_bid(self, manager_name):
        """Place a bid for a manager"""
        
        if not self.bidding_active or not self.current_player:
            return
        
        manager = self.managers[manager_name]
        new_bid = self.current_bid + self.config.bid_increment
        
        if manager.can_bid(new_bid, self.current_player.category):
            self.current_bid = new_bid
            self.highest_bidder = manager_name
            
            self.update_display()
            self.update_bid_buttons()
            
            # Play sound effect if available
            if self.sound_enabled:
                try:
                    # You can add a sound file here if desired
                    pass
                except:
                    pass
        else:
            # Provide feedback why bid failed
            if new_bid > manager.budget:
                messagebox.showwarning("Cannot Bid", f"{manager_name} doesn't have enough budget!")
            elif len(manager.players) >= manager.max_players:
                messagebox.showwarning("Cannot Bid", f"{manager_name}'s team is full!")
            else:
                category_limit = manager.category_limits.get(self.current_player.category, 0)
                current_count = manager.category_counts.get(self.current_player.category, 0)
                messagebox.showwarning("Cannot Bid", 
                    f"{manager_name} has reached the {self.current_player.category} limit ({current_count}/{category_limit})!")
    
    def pass_bid(self, manager_name):
        """Manager passes on current bid"""
        print(f"{manager_name} passed on {self.current_player.name if self.current_player else 'current player'}")
    
    def sell_player(self):
        """Sell the current player to highest bidder or at base price"""
        
        if not self.current_player:
            messagebox.showwarning("No Player", "No player to sell!")
            return
        
        # If no one has bid yet, check eligible managers for base price
        if self.highest_bidder is None:
            eligible_managers = []
            for manager in self.managers.values():
                if manager.can_bid(self.current_player.base_price, self.current_player.category):
                    eligible_managers.append(manager)
            
            if len(eligible_managers) == 0:
                messagebox.showwarning("No Eligible Managers", "No manager can afford this player!")
                return
            elif len(eligible_managers) == 1:
                # Only one manager can afford - sell at base price
                self.highest_bidder = eligible_managers[0].name
                self.current_bid = self.current_player.base_price
                messagebox.showinfo("Base Price Sale", 
                    f"{self.current_player.name} sold to {self.highest_bidder} at base price €{self.current_bid}!")
            else:
                # Multiple managers can afford - they need to bid
                messagebox.showwarning("Multiple Bidders Possible", 
                    "Multiple managers can afford this player. Please have them bid!")
                return
        
        # Finalize the sale
        self.current_player.sold_price = self.current_bid
        self.current_player.sold_to = self.highest_bidder
        self.current_player.is_sold = True
        
        manager = self.managers[self.highest_bidder]
        manager.add_player(self.current_player)
        self.sold_players.append(self.current_player)
        
        # Store sale info for message
        sold_player_name = self.current_player.name
        sold_to = self.highest_bidder
        sold_price = self.current_bid
        
        # Reset auction state
        self.bidding_active = False
        self.current_player = None
        self.current_bid = 0
        self.highest_bidder = None
        
        # Update displays
        self.update_display()
        self.update_teams_display()
        
        # Disable control buttons
        self.sold_btn.config(state=tk.DISABLED)
        self.base_price_btn.config(state=tk.DISABLED)
        self.unsold_btn.config(state=tk.DISABLED)
        self.update_bid_buttons()
        
        messagebox.showinfo("Player Sold!", f"🎉 {sold_player_name} sold to {sold_to} for €{sold_price}!")
    
    def buy_at_base_price(self):
        """Buy current player at base price"""
        
        if not self.current_player:
            messagebox.showwarning("No Player", "No player to buy!")
            return
        
        eligible_managers = []
        for manager in self.managers.values():
            if manager.can_bid(self.current_player.base_price, self.current_player.category):
                eligible_managers.append(manager)
        
        if len(eligible_managers) == 0:
            messagebox.showwarning("No Eligible Managers", "No manager can afford this player at base price!")
            return
        elif len(eligible_managers) == 1:
            self.highest_bidder = eligible_managers[0].name
            self.current_bid = self.current_player.base_price
            self.sell_player()
        else:
            # Show selection dialog
            manager_names = [m.name for m in eligible_managers]
            
            # Create selection window
            selection_window = tk.Toplevel(self.root)
            selection_window.title("Select Manager")
            selection_window.configure(bg='#1a1a3a')
            selection_window.geometry('400x300')
            selection_window.grab_set()
            
            tk.Label(
                selection_window,
                text=f"Who wants to buy {self.current_player.name}\nat base price €{self.current_player.base_price}?",
                font=("Arial", 14, "bold"),
                fg='white',
                bg='#1a1a3a'
            ).pack(pady=20)
            
            selected_manager = tk.StringVar()
            
            for manager in eligible_managers:
                tk.Radiobutton(
                    selection_window,
                    text=f"{manager.name} ({manager.team_name})",
                    variable=selected_manager,
                    value=manager.name,
                    font=("Arial", 12),
                    fg='white',
                    bg='#1a1a3a',
                    selectcolor='#4f46e5'
                ).pack(pady=5)
            
            def confirm_selection():
                if selected_manager.get():
                    self.highest_bidder = selected_manager.get()
                    self.current_bid = self.current_player.base_price
                    selection_window.destroy()
                    self.sell_player()
                else:
                    messagebox.showwarning("Selection Required", "Please select a manager.")
            
            tk.Button(
                selection_window,
                text="Confirm Purchase",
                font=("Arial", 12, "bold"),
                bg='#10b981',
                fg='white',
                command=confirm_selection
            ).pack(pady=20)
            
            tk.Button(
                selection_window,
                text="Cancel",
                font=("Arial", 12),
                bg='#ef4444',
                fg='white',
                command=selection_window.destroy
            ).pack()
    
    def mark_unsold(self):
        """Mark current player as unsold and add to unsold players list"""
        
        if not self.current_player:
            messagebox.showwarning("No Player", "No player to mark as unsold!")
            return
        
        # Add player back to unsold list for re-auction
        self.unsold_players.append(self.current_player)
        player_name = self.current_player.name
        
        # Reset auction state
        self.bidding_active = False
        self.current_player = None
        self.current_bid = 0
        self.highest_bidder = None
        
        # Update display
        self.update_display()
        
        # Disable control buttons
        self.sold_btn.config(state=tk.DISABLED)
        self.base_price_btn.config(state=tk.DISABLED)
        self.unsold_btn.config(state=tk.DISABLED)
        self.update_bid_buttons()
        
        messagebox.showinfo("Player Unsold", f"{player_name} will be re-auctioned later!")
    
    def update_display(self):
        """Update the main auction display"""
        
        # Update status
        total_budget_left = sum(manager.budget for manager in self.managers.values())
        total_spent = sum(manager.get_total_spent() for manager in self.managers.values())
        
        status_text = f"Players Remaining: {len(self.player_pool)} | Unsold: {len(self.unsold_players)} | "
        status_text += f"Total Budget Left: €{total_budget_left} | Total Spent: €{total_spent}"
        self.status_label.config(text=status_text)
        
        # Update current player display
        if self.current_player:
            self.player_name_label.config(text=self.current_player.name, fg='white')
            
            category_colors = {
                'Premium': '#ff8c42',
                'Standard': '#00ffff',
                'Rookie': '#90ee90',
                'Veteran': '#ffa500',
                'International': '#ff69b4'
            }
            category_color = category_colors.get(self.current_player.category, '#ffd700')
            
            self.player_details_label.config(
                text=f"Category: {self.current_player.category} | Base Price: €{self.current_player.base_price}",
                fg=category_color
            )
            
            bidder_text = f" - {self.highest_bidder}" if self.highest_bidder else ""
            self.current_bid_label.config(text=f"Current Bid: €{self.current_bid}{bidder_text}")
        else:
            self.player_name_label.config(text="Click 'Next Player' to continue auction", fg='#a0a9c0')
            self.player_details_label.config(text="")
            self.current_bid_label.config(text="")
    
    def update_bid_buttons(self):
        """Update bid button states"""
        
        if not self.current_player or not self.bidding_active:
            # Disable all bid buttons
            for manager_name, buttons in self.bid_buttons.items():
                buttons['bid'].config(state=tk.DISABLED, text="No Auction")
                buttons['pass'].config(state=tk.DISABLED)
                buttons['frame'].config(bg='#6b7280')  # Gray out
            return
        
        next_bid = self.current_bid + self.config.bid_increment
        
        for manager_name, buttons in self.bid_buttons.items():
            manager = self.managers[manager_name]
            
            can_bid = manager.can_bid(next_bid, self.current_player.category)
            
            if can_bid:
                buttons['bid'].config(
                    state=tk.NORMAL,
                    text=f"Bid €{next_bid}",
                    bg='#10b981' if self.highest_bidder != manager_name else '#ffd700'
                )
                buttons['pass'].config(state=tk.NORMAL)
                buttons['frame'].config(bg='#4f46e5' if self.highest_bidder != manager_name else '#ff8c42')
            else:
                buttons['bid'].config(state=tk.DISABLED, text="Cannot Bid", bg='#6b7280')
                buttons['pass'].config(state=tk.DISABLED)
                buttons['frame'].config(bg='#6b7280')
    
    def update_teams_display(self):
        """Update all team displays"""
        
        for manager_name, manager in self.managers.items():
            team_data = self.team_frames[manager_name]
            
            # Update budget
            team_data['budget_label'].config(text=f"€{manager.budget} left")
            
            # Update category stats
            category_text = f"Players: {len(manager.players)}/{manager.max_players}"
            for cat_name, count in manager.category_counts.items():
                limit = manager.category_limits.get(cat_name, 0)
                category_text += f" | {cat_name}: {count}/{limit}"
            team_data['category_label'].config(text=category_text)
            
            # Update players list
            players_text = team_data['players_text']
            players_text.delete('1.0', tk.END)
            
            if manager.players:
                for i, player in enumerate(manager.players, 1):
                    players_text.insert(tk.END, f"{i}. {player.name}\n")
                    players_text.insert(tk.END, f"   ({player.category}) - €{player.sold_price}\n\n")
            else:
                players_text.insert(tk.END, "No players yet")
    
    def export_teams(self):
        """Export team data to file"""
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Auction Results"
        )
        
        if not filename:
            return
        
        try:
            if filename.endswith('.csv'):
                self.export_csv(filename)
            else:
                self.export_text(filename)
            
            messagebox.showinfo("Export Complete", f"Auction results exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def export_text(self, filename):
        """Export as formatted text file"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{self.config.title.upper()} - AUCTION RESULTS\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            # Team summaries
            f.write("TEAM SUMMARY\n")
            f.write("=" * 30 + "\n\n")
            
            for manager in self.managers.values():
                total_spent = manager.get_total_spent()
                f.write(f"{manager.team_name.upper()}\n")
                f.write(f"Manager: {manager.name}\n")
                f.write(f"Budget Left: €{manager.budget}\n")
                f.write(f"Total Spent: €{total_spent}\n")
                f.write(f"Players: {len(manager.players)}/{manager.max_players}\n")
                
                # Category counts
                for cat_name, count in manager.category_counts.items():
                    limit = manager.category_limits.get(cat_name, 0)
                    f.write(f"{cat_name}: {count}/{limit} ")
                f.write("\n\nPLAYERS:\n")
                
                for player in manager.players:
                    f.write(f"  • {player.name} ({player.category}) - €{player.sold_price}\n")
                f.write("\n" + "-" * 40 + "\n\n")
            
            # Statistics
            f.write("AUCTION STATISTICS\n")
            f.write("=" * 30 + "\n")
            f.write(f"Remaining Players: {len(self.player_pool)}\n")
            f.write(f"Unsold Players: {len(self.unsold_players)}\n")
            f.write(f"Total Budget Used: €{sum(manager.get_total_spent() for manager in self.managers.values())}\n")
    
    def export_csv(self, filename):
        """Export as CSV file"""
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(["Team", "Manager", "Budget Left", "Total Spent", "Player", "Category", "Price"])
            
            # Write team data
            for manager in self.managers.values():
                total_spent = manager.get_total_spent()
                
                if manager.players:
                    for player in manager.players:
                        writer.writerow([
                            manager.team_name,
                            manager.name,
                            manager.budget,
                            total_spent,
                            player.name,
                            player.category,
                            player.sold_price
                        ])
                else:
                    writer.writerow([
                        manager.team_name,
                        manager.name,
                        manager.budget,
                        total_spent,
                        "No players",
                        "",
                        ""
                    ])
    
    def back_to_setup(self):
        """Return to setup configuration"""
        
        result = messagebox.askyesno(
            "Back to Setup",
            "Are you sure you want to go back to setup? This will reset the entire auction."
        )
        
        if result:
            # Reset auction state
            self.config = None
            self.managers = {}
            self.player_pool = []
            self.current_player = None
            self.current_bid = 0
            self.highest_bidder = None
            self.bidding_active = False
            self.sold_players = []
            self.unsold_players = []
            
            # Show setup again
            self.show_setup()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Set window icon and properties
    root.withdraw()  # Hide initially until setup is complete
    
    try:
        app = AuctionApp(root)
        
        # Show window if auction was configured
        if app.config and app.config.is_configured:
            root.deiconify()  # Show window
            root.mainloop()
        else:
            root.quit()
            
    except Exception as e:
        messagebox.showerror("Application Error", f"An error occurred: {str(e)}")
        root.quit()


if __name__ == "__main__":
    main()
