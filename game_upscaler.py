"""
Real-Time Game Upscaling
Captures game frames and applies AI upscaling on-the-fly
"""

import numpy as np
import cv2
from mss import mss
from upscaler import AMDUpscaler
import time

class GameUpscaler:
    def __init__(self, monitor=1):
        """Initialize game upscaler"""
        self.upscaler = AMDUpscaler()
        self.sct = mss()
        self.monitor = self.sct.monitors[monitor]
        
        print(f"Monitoring: {self.monitor['width']}x{self.monitor['height']}")
    
    def run(self, display_output=True, fps_target=60):
        """Run real-time upscaling"""
        print("\n" + "="*60)
        print("REAL-TIME GAME UPSCALING ACTIVE")
        print("="*60)
        print("\nPress 'Q' to quit")
        
        frame_time = 1.0 / fps_target
        fps_list = []
        
        try:
            while True:
                loop_start = time.time()
                
                # Capture frame
                capture_start = time.time()
                screenshot = np.array(self.sct.grab(self.monitor))
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB)
                capture_time = time.time() - capture_start
                
                # Upscale frame
                upscale_start = time.time()
                upscaled = self.upscaler.upscale_array(screenshot)
                upscale_time = time.time() - upscale_start
                
                # Calculate FPS
                total_time = time.time() - loop_start
                current_fps = 1.0 / total_time if total_time > 0 else 0
                fps_list.append(current_fps)
                if len(fps_list) > 30:
                    fps_list.pop(0)
                avg_fps = sum(fps_list) / len(fps_list)
                
                # Display info
                info_text = f"FPS: {avg_fps:.1f} | Capture: {capture_time*1000:.1f}ms | Upscale: {upscale_time*1000:.1f}ms"
                cv2.putText(upscaled, info_text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display output
                if display_output:
                    cv2.imshow('AI Upscaled Game', cv2.cvtColor(upscaled, cv2.COLOR_RGB2BGR))
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                # Throttle to target FPS
                elapsed = time.time() - loop_start
                if elapsed < frame_time:
                    time.sleep(frame_time - elapsed)
        
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            cv2.destroyAllWindows()
            print(f"\n[OK] Average FPS: {avg_fps:.1f}")


if __name__ == "__main__":
    upscaler = GameUpscaler(monitor=1)
    upscaler.run(display_output=True, fps_target=60)

