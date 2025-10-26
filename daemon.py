"""
AI Upscaler Daemon - Always Running Background Service
Auto-detects games and applies upscaling
Toggle with Ctrl+Alt+U hotkey
"""

import sys
import time
import threading
from pathlib import Path
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import keyboard
from upscaler import AMDUpscaler
from game_upscaler import GameUpscaler

class UpscalerDaemon:
    def __init__(self):
        self.enabled = False
        self.upscaler = None
        self.upscaler_thread = None
        self.running = True
        
        # Load config
        self.config_path = Path("daemon_config.txt")
        self.load_config()
        
        print("=" * 60)
        print("AI UPSCALER DAEMON - Background Service")
        print("=" * 60)
        print(f"\nStatus: {'ENABLED' if self.enabled else 'DISABLED'}")
        print("Hotkey: Ctrl+Alt+U to toggle")
        print("System tray icon for control")
    
    def load_config(self):
        """Load saved state"""
        if self.config_path.exists():
            state = self.config_path.read_text().strip()
            self.enabled = state == "enabled"
    
    def save_config(self):
        """Save current state"""
        self.config_path.write_text("enabled" if self.enabled else "disabled")

    
    def toggle(self):
        """Toggle upscaling on/off"""
        self.enabled = not self.enabled
        self.save_config()
        
        if self.enabled:
            print("\n✓ UPSCALING ENABLED")
            self.start_upscaling()
        else:
            print("\n✗ UPSCALING DISABLED")
            self.stop_upscaling()
    
    def start_upscaling(self):
        """Start upscaling in background thread"""
        if self.upscaler_thread and self.upscaler_thread.is_alive():
            return
        
        self.upscaler_thread = threading.Thread(target=self._upscale_loop, daemon=True)
        self.upscaler_thread.start()
    
    def stop_upscaling(self):
        """Stop upscaling"""
        # Thread will stop on next check
        pass
    
    def _upscale_loop(self):
        """Background upscaling loop"""
        try:
            upscaler = GameUpscaler(monitor=1)
            while self.enabled and self.running:
                # Run upscaling
                upscaler.run(display_output=False, fps_target=60)
                time.sleep(0.1)
        except Exception as e:
            print(f"Upscaling error: {e}")

    
    def create_icon_image(self):
        """Create system tray icon"""
        width = 64
        height = 64
        color1 = (0, 255, 0) if self.enabled else (128, 128, 128)
        color2 = (255, 255, 255)
        
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle([width // 4, height // 4, width * 3 // 4, height * 3 // 4], 
                     fill=color2)
        
        return image
    
    def setup_hotkey(self):
        """Setup Ctrl+Alt+U hotkey"""
        keyboard.add_hotkey('ctrl+alt+u', self.toggle)
        print("Hotkey registered: Ctrl+Alt+U")
    
    def setup_tray(self):
        """Setup system tray icon"""
        menu = Menu(
            MenuItem('Toggle (Ctrl+Alt+U)', self.toggle),
            MenuItem('Exit', self.quit)
        )
        
        icon = Icon("AI Upscaler", self.create_icon_image(), 
                   "AI Upscaler: " + ("ON" if self.enabled else "OFF"),
                   menu)
        
        icon.run()
    
    def quit(self):
        """Shutdown daemon"""
        self.running = False
        self.enabled = False
        print("\nShutting down...")
        sys.exit(0)

    
    def detect_game(self):
        """Detect if a game is running"""
        import psutil
        
        # Common game process patterns
        game_patterns = [
            'game', 'play', '.exe',
            'steam', 'epic', 'origin', 
            'uplay', 'launcher'
        ]
        
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower()
                if any(pattern in name for pattern in game_patterns):
                    return True
            except:
                pass
        
        return False
    
    def run(self):
        """Main daemon loop"""
        # Setup hotkey
        self.setup_hotkey()
        
        # If enabled, start upscaling
        if self.enabled:
            self.start_upscaling()
        
        # Run system tray (blocking)
        print("\nDaemon running in background...")
        print("Use system tray icon or Ctrl+Alt+U to control\n")
        self.setup_tray()


if __name__ == "__main__":
    daemon = UpscalerDaemon()
    daemon.run()
