#!/usr/bin/env python3
"""
Simple HTTP Server for Sports Auction
A basic web server that serves our auction files
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

class AuctionHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for auction files"""
    
    def end_headers(self):
        # Add CORS headers to allow local file access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    """Start the local web server"""
    
    # Change to the project root directory (parent of scripts)
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    PORT = 8080
    
    print("🏆 Universal Sports Auction Server")
    print("=" * 40)
    print(f"🚀 Starting server on port {PORT}...")
    print(f"📁 Serving files from: {os.getcwd()}")
    
    try:
        with socketserver.TCPServer(("", PORT), AuctionHTTPRequestHandler) as httpd:
            print(f"✅ Server running at: http://localhost:{PORT}")
            print(f"🎯 Auction App: http://localhost:{PORT}/src/web/auction_web.html")
            print(f"📋 Landing Page: http://localhost:{PORT}/index.html")
            print(f"📊 Project Structure: http://localhost:{PORT}")
            print("\n🎮 Ready for auction! Open the URLs above in your browser.")
            print("Press Ctrl+C to stop the server.")
            
            # Automatically open the landing page in browser
            try:
                webbrowser.open(f"http://localhost:{PORT}/index.html")
                print("🌐 Opening landing page in your default browser...")
            except:
                print("⚠️  Please manually open the URL in your browser")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print("Try a different port or close other applications using this port.")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    start_server()
