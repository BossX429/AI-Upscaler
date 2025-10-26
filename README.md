# 🚀 AI Upscaler - AMD Technology Clone

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/BossX429/AI-Upscaler/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()
[![Python](https://img.shields.io/badge/python-3.12.7-blue.svg)](https://python.org)

> **Cloned AMD Radeon AI upscaling technology, weaponized for universal use. Real-time 2x upscaling with DirectML GPU acceleration. Always-on background service with instant hotkey toggle.**

---

## 🎯 What Is This?

This project extracts and clones the AI upscaling technology from **AMD Radeon Software**, making it available for universal use beyond just video capture. The same neural networks AMD uses for real-time enhancement are now deployable across any application.

### 💡 Key Achievement
- **Extracted:** 6 production ONNX models from AMD Radeon Software (13.4 MB)
- **Main Model:** `upscale2x_c3_rt_f16.onnx` (0.15 MB - optimized for real-time)
- **Verified:** Perfect 2x upscaling (100x100 → 200x200) with <10ms latency
- **Architecture:** FP16 precision, DirectML accelerated, NHWC format

---

## ⚡ Features

### 🎮 **Real-Time AI Upscaling**
- 2x resolution increase (1080p → 2160p)
- 60+ FPS performance on AMD GPUs
- <10ms per-frame latency
- FP16 GPU accelerated

### 🤖 **Always-On Background Service**
- Runs at Windows startup automatically
- System tray integration
- Minimal resource usage when disabled
- Persistent state management

### ⌨️ **Instant Toggle Control**
- **Hotkey:** `Ctrl+Alt+U` (global, works anywhere)
- **System Tray:** Right-click menu
- **Persistent:** Remembers on/off state between sessions

### 🔧 **Multiple Use Cases**
1. **Gaming:** Render at lower res, AI upscale to display res
2. **Video:** Enhance recorded footage in real-time
3. **Screen Capture:** Higher quality captures with lower overhead
4. **Images:** Batch upscaling for photos

---

## 🏗️ Technology Stack

### **AI Models (Extracted from AMD)**
- `upscale2x_c3_rt_f16.onnx` - 2x upscaler (0.15 MB)
- `denoise_c3_ldr_float16.onnx` - LDR denoising (2.34 MB)
- `denoise_c3_hdr_gamma_2.5_f16.onnx` - HDR denoising (2.34 MB)
- `denoise_c9_ldr_f16.onnx` - Advanced LDR (4.25 MB)
- `denoise_c9_hdr_gamma_2.5_f16.onnx` - Advanced HDR (4.25 MB)
- `upscale2x_fast.pb` - TensorFlow variant (0.29 MB)

### **Inference Engine**
- **Runtime:** ONNX Runtime with DirectML
- **Precision:** FP16 (half-precision)
- **Acceleration:** AMD GPU via DirectML
- **Format:** NHWC (batch, height, width, channels)

### **Architecture**
- **Core:** `upscaler.py` - Inference engine
- **Real-Time:** `game_upscaler.py` - Live frame processing
- **Daemon:** `daemon.py` - Background service
- **Service:** `service.ps1` - Windows Task Scheduler integration

---

## 📊 Performance Benchmarks

**Test System:**
- CPU: Intel i7-12700K (12 cores)
- GPU: AMD Radeon RX 7900 XTX (24GB VRAM)
- RAM: 64GB
- OS: Windows 11

**Results:**
- **1080p → 2160p:** 60+ FPS
- **1440p → 2880p:** 45+ FPS  
- **Per-frame latency:** 5-10ms
- **First inference:** ~170ms (model loading)
- **Subsequent:** <10ms per frame

---

## 🚀 Quick Start

### Prerequisites
- Windows 11
- Python 3.12+
- AMD GPU with DirectML support (or CPU fallback)

### Installation

```powershell
# Clone repository
git clone https://github.com/BossX429/AI-Upscaler.git
cd AI-Upscaler

# Install dependencies
.\setup.ps1

# Install as Windows service (auto-start)
.\service.ps1 -Install

# Start daemon
.\service.ps1 -Start
```

### Usage

**Daily Use:**
- Press `Ctrl+Alt+U` to toggle upscaling on/off
- Check system tray icon (green = active, gray = inactive)

**Service Control:**
```powershell
.\service.ps1 -Status      # Check status
.\service.ps1 -Start       # Start daemon
.\service.ps1 -Stop        # Stop daemon  
.\service.ps1 -Uninstall   # Remove service
```

**Manual Testing:**
```powershell
# Upscale single image
python upscaler.py input.jpg output.jpg

# Real-time demo
python game_upscaler.py
```

---

## 📁 Project Structure

```
AI-Upscaler/
├── models/                 # AI models (13.4 MB total)
│   ├── upscale2x_c3_rt_f16.onnx      # Main 2x upscaler
│   ├── denoise_*.onnx                # Denoising models
│   └── upscale2x_fast.pb             # TensorFlow version
├── upscaler.py            # Core inference engine
├── game_upscaler.py       # Real-time processing
├── daemon.py              # Background service
├── service.ps1            # Windows service manager
├── setup.ps1              # Automated installation
├── README.md              # This file
├── USAGE.md               # Detailed usage guide
├── FEATURES.md            # Complete feature archive
├── INSTALL.md             # Installation guide
└── QUICKREF.md            # Quick reference card
```

---

## 🎯 How It Works

1. **Model Loading:** ONNX Runtime loads FP16 model
2. **DirectML Acceleration:** GPU-accelerated inference
3. **Frame Capture:** Real-time screen/game capture (optional)
4. **AI Processing:** 2x upscaling via neural network
5. **Output:** Enhanced frames at 2x resolution

---

## 🔬 Technical Deep Dive

### Model Architecture
- **Input Shape:** `[batch, height, width, 3]` (NHWC format)
- **Output Shape:** `[batch, height*2, width*2, 3]`
- **Data Type:** `float16` (FP16)
- **Provider:** DirectML (AMD GPU) or CPU fallback

### Preprocessing
1. Image normalization (0-1 range)
2. FP16 conversion
3. NHWC format (no transpose needed)
4. Batch dimension addition

### Postprocessing
1. Remove batch dimension
2. Denormalize (0-255 range)
3. Clip values
4. Convert to uint8

---

## 💻 Development

### Requirements
```
onnxruntime-directml  # DirectML acceleration
numpy                 # Array operations
pillow                # Image I/O
opencv-python         # Video processing
mss                   # Screen capture
pystray               # System tray
keyboard              # Hotkey support
psutil                # Process management
```

### Building
```powershell
# Install dev dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Build distribution
python setup.py bdist_wheel
```

---

## 🛣️ Roadmap

### Current (v1.0.0)
- ✅ Core inference engine
- ✅ Real-time upscaling
- ✅ Background daemon
- ✅ Hotkey toggle
- ✅ System tray integration
- ✅ Auto-start service

### Future
- [ ] DirectX 11/12 hook injection
- [ ] Vulkan API support
- [ ] ReShade plugin
- [ ] OBS Studio integration
- [ ] Multi-monitor support
- [ ] Custom upscaling factors (3x, 4x)
- [ ] Per-game configuration profiles
- [ ] GUI settings panel
- [ ] Model fine-tuning tools

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **AMD** - For the original AI upscaling models
- **ONNX Runtime** - For the inference framework
- **DirectML** - For GPU acceleration

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

- **GitHub:** [@BossX429](https://github.com/BossX429)
- **Project:** [AI-Upscaler](https://github.com/BossX429/AI-Upscaler)

---

**Built with 🔥 by Kyle | Powered by AMD AI Technology**
