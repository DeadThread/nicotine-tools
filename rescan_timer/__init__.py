# __init__.py
"""
Automatic Rescan Timer Plugin for Nicotine+
Automatically rescans shared folders at specified intervals.
"""

import threading
import time
from pynicotine.pluginsystem import BasePlugin

# Plugin configuration
RESCAN_INTERVAL_MINUTES = 1  # 6 hours - adjust as needed

class Plugin(BasePlugin):
    """Automatic rescan timer plugin for Nicotine+"""
    
    def __init__(self):
        """Initialize the plugin"""
        super().__init__()
        print("[RescanTimer] __init__ called!")  # Debug print
        
        # Try to start immediately in constructor
        self.running = False
        self.thread = None
        
        # Start a delayed initialization
        threading.Timer(2.0, self.delayed_init).start()
        print("[RescanTimer] Delayed init timer started!")
        
    def delayed_init(self):
        """Initialize after a short delay"""
        print("[RescanTimer] delayed_init() called!")
        try:
            self.start_timer()
        except Exception as e:
            print(f"[RescanTimer] Error in delayed_init: {e}")
    
    def start_timer(self):
        """Start the rescan timer"""
        print("[RescanTimer] start_timer() called!")
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.rescan_loop, daemon=True)
            self.thread.start()
            print("[RescanTimer] Thread started!")
            
            # Try to log
            try:
                self.log(f"✅ RescanTimer started! Rescanning every {RESCAN_INTERVAL_MINUTES} minutes")
            except Exception as e:
                print(f"[RescanTimer] Logging failed: {e}")
    
    # Keep all the other methods we tried
    def init(self):
        """Called when the plugin is loaded"""
        print("[RescanTimer] init() method called!")
        self.start_timer()
        
    def loaded_notification(self):
        """Alternative method that might be called when plugin loads"""
        print("[RescanTimer] loaded_notification() called!")
        self.start_timer()
    
    def enable_notification(self):
        """Another alternative method"""
        print("[RescanTimer] enable_notification() called!")
        self.start_timer()
        
    def disable(self):
        """Called when the plugin is disabled"""
        self.log("🛑 RescanTimer: disable() method called!")
        self.running = False
        if self.thread and self.thread.is_alive():
            self.log("⏳ Waiting for rescan thread to stop...")
            self.thread.join(timeout=1.0)
            self.log("✅ Thread stopped successfully")
        self.log("❌ RescanTimer stopped")
        
    def rescan_loop(self):
        """Main loop that triggers rescans at intervals"""
        self.log("🔄 RescanTimer: Background thread started!")
        
        while self.running:
            self.log(f"⏰ Waiting {RESCAN_INTERVAL_MINUTES} minutes until next rescan...")
            
            # Wait for the specified interval (but check every second if we should stop)
            for i in range(RESCAN_INTERVAL_MINUTES * 60):
                if not self.running:
                    self.log("🛑 Rescan loop stopping early - plugin disabled")
                    return
                time.sleep(1)
                
                # Log progress every 30 minutes for long intervals
                if RESCAN_INTERVAL_MINUTES >= 60 and i % (30 * 60) == 0 and i > 0:
                    remaining_minutes = (RESCAN_INTERVAL_MINUTES * 60 - i) // 60
                    self.log(f"⏱️ {remaining_minutes} minutes remaining until next rescan")
            
            if self.running:
                try:
                    self.log("🔍 Triggering automatic rescan now...")
                    # Trigger rescan through the core application
                    self.core.shares.rescan_shares()
                    self.log("✅ Automatic rescan completed successfully!")
                except Exception as e:
                    self.log(f"❌ Error during rescan: {e}")
        
        self.log("🔚 Rescan loop thread ended")
    
    def log(self, message):
        """Log a message to the Nicotine+ log"""
        try:
            # Try the primary logging method
            self.core.chatrooms.server_message_to_ui(f"[RescanTimer] {message}")
        except AttributeError:
            try:
                # Alternative logging method
                self.core.server_message_to_ui(f"[RescanTimer] {message}")
            except AttributeError:
                try:
                    # Another alternative
                    print(f"[RescanTimer] {message}")
                    # Try to log to the general log if available
                    if hasattr(self, 'core') and hasattr(self.core, 'log'):
                        self.core.log.add(f"[RescanTimer] {message}")
                except:
                    # Final fallback
                    print(f"[RescanTimer] {message}")