# plugin.py
"""
Automatic Rescan Timer Plugin for Nicotine+
Automatically rescans shared folders at specified intervals.
"""

import threading
import time
from pynicotine.pluginsystem import BasePlugin

# Plugin configuration
RESCAN_INTERVAL_MINUTES = 360  # 6 hours - adjust as needed

class Plugin(BasePlugin):
    """Automatic rescan timer plugin for Nicotine+"""
    
    def __init__(self, parent):
        """Initialize the plugin"""
        super().__init__(parent)
        self.running = False
        self.thread = None
        
    def init(self):
        """Called when the plugin is loaded"""
        self.running = True
        self.thread = threading.Thread(target=self.rescan_loop, daemon=True)
        self.thread.start()
        
        # Log plugin start
        self.log(f"RescanTimer started - rescanning every {RESCAN_INTERVAL_MINUTES} minutes")
        
    def disable(self):
        """Called when the plugin is disabled"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        self.log("RescanTimer stopped")
        
    def rescan_loop(self):
        """Main loop that triggers rescans at intervals"""
        while self.running:
            # Wait for the specified interval
            for _ in range(RESCAN_INTERVAL_MINUTES * 60):
                if not self.running:
                    return
                time.sleep(1)
            
            if self.running:
                try:
                    # Trigger rescan through the core application
                    self.core.shares.rescan_shares()
                    self.log("Automatic rescan triggered")
                except Exception as e:
                    self.log(f"Error during rescan: {e}")
    
    def log(self, message):
        """Log a message to the Nicotine+ log"""
        try:
            self.core.chatrooms.server_message_to_ui(f"[RescanTimer] {message}")
        except:
            # Fallback if server_message_to_ui is not available
            print(f"[RescanTimer] {message}")