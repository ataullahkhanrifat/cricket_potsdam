#!/usr/bin/env python3
"""
Test script for Cricket Potsdam Auction App
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        print("✅ tkinter - OK")
    except ImportError as e:
        print(f"❌ tkinter - FAILED: {e}")
        return False
    
    try:
        import pygame
        print("✅ pygame - OK")
    except ImportError as e:
        print(f"⚠️  pygame - WARNING: {e} (Sound effects will be disabled)")
    
    try:
        import random
        import csv
        from datetime import datetime
        print("✅ Standard libraries - OK")
    except ImportError as e:
        print(f"❌ Standard libraries - FAILED: {e}")
        return False
    
    return True

def test_auction_classes():
    """Test the main auction classes"""
    print("\nTesting Cricket Auction classes...")
    
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Test imports without pygame dependency
        import importlib.util
        spec = importlib.util.spec_from_file_location("cricket_auction", "cricket_auction.py")
        cricket_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cricket_module)
        
        Player = cricket_module.Player
        Manager = cricket_module.Manager
        AuctionApp = cricket_module.AuctionApp
        
        # Test Player class
        player = Player("Test Player", 100, "TIGER")
        assert player.name == "Test Player"
        assert player.base_price == 100
        assert player.category == "TIGER"
        print("✅ Player class - OK")
        
        # Test Manager class
        manager = Manager("Test Manager", "Test Team")
        assert manager.name == "Test Manager"
        assert manager.team_name == "Test Team"
        assert manager.budget == 1300
        assert manager.can_bid(100, "TIGER") == True
        print("✅ Manager class - OK")
        
        print("✅ All classes imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Class testing - FAILED: {e}")
        return False

def test_gui_creation():
    """Test if GUI can be created (without showing it)"""
    print("\nTesting GUI creation...")
    
    try:
        import tkinter as tk
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Import module dynamically to avoid pygame dependency
        import importlib.util
        spec = importlib.util.spec_from_file_location("cricket_auction", "cricket_auction.py")
        cricket_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cricket_module)
        
        AuctionApp = cricket_module.AuctionApp
        
        # Create root window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create app instance
        app = AuctionApp(root)
        
        # Basic checks
        assert len(app.managers) == 3
        assert len(app.tiger_pool) == 11
        assert len(app.lion_pool) == 9
        
        root.destroy()
        print("✅ GUI creation - OK")
        return True
        
    except Exception as e:
        print(f"❌ GUI creation - FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("🏏 Cricket Potsdam Auction - System Test")
    print("=" * 50)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_auction_classes():
        all_passed = False
    
    if not test_gui_creation():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! The auction app is ready to use.")
        print("\nTo start the auction:")
        print("  1. Run: python cricket_auction.py")
        print("  2. Or double-click: run_auction.bat")
        print("  3. Or use VS Code task: 'Run Cricket Auction'")
    else:
        print("❌ SOME TESTS FAILED! Please check the errors above.")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
