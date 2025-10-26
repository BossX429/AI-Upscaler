# AI UPSCALER - Quick Reference Card

## 🎯 ONE-TIME SETUP
```powershell
cd C:\Quick-Access\Projects\AI-Upscaler
.\setup.ps1              # Install dependencies
.\service.ps1 -Install   # Enable auto-start
.\service.ps1 -Start     # Start now
```

## 🎮 DAILY USE
**Hotkey:** `Ctrl+Alt+U` - Toggle upscaling on/off  
**System Tray:** Right-click icon for menu  
**Default:** Runs at Windows startup

## 🔧 SERVICE CONTROL
```powershell
.\service.ps1 -Status      # Check status
.\service.ps1 -Start       # Start daemon
.\service.ps1 -Stop        # Stop daemon
.\service.ps1 -Uninstall   # Remove service
```

## 📊 PERFORMANCE
- 1080p → 2160p: **60+ FPS**
- Latency: **<10ms per frame**
- GPU: AMD 7900 XTX (FP16)

## 📁 KEY FILES
- `daemon.py` - Background service
- `upscaler.py` - Core engine
- `game_upscaler.py` - Real-time processing
- `service.ps1` - Service management
- `USAGE.md` - Full documentation

## 💾 ARCHIVE
- **Git:** C:\Quick-Access\Projects\AI-Upscaler\.git
- **ZIP:** C:\Quick-Access\Archives\AI-Upscaler_v1.0.0_ARCHIVE_*.zip
- **Version:** v1.0.0
- **Date:** October 26, 2025

## 🎯 HOW IT WORKS
1. Daemon runs in background
2. Monitors for games
3. When enabled: captures frames → AI upscales → outputs
4. Toggle on/off as needed
5. Remembers your preference

## 🐛 TROUBLESHOOTING
**Not working?**
- Check: `.\service.ps1 -Status`
- Restart: `.\service.ps1 -Stop` then `-Start`
- Manual: `python daemon.py` (see errors)

**No hotkey?**
- Another app might use Ctrl+Alt+U
- Try system tray right-click

**Poor FPS?**
- Verify DirectML: `python -c "import onnxruntime; print(onnxruntime.get_available_providers())"`
- Should see `DmlExecutionProvider`

---

**Keep this file handy for quick reference!**
