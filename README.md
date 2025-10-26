# AMD AI Upscaler - Cloned & Weaponized

## What We Found
AMD Radeon Software uses ONNX AI models for real-time upscaling and denoising.

**Key Model:** `upscale2x_c3_rt_f16.onnx`
- Size: 0.15 MB (tiny = fast)
- Type: 2x upscaler, 3-channel RGB, real-time optimized
- Precision: FP16 (half-precision for AMD GPUs)

## Source Location
```
C:\Program Files\AMD\CNext\CNext\models\
```

## Available Models
1. `upscale2x_c3_rt_f16.onnx` - 2x upscaler (MAIN TARGET)
2. `denoise_c3_ldr_float16.onnx` - LDR denoising
3. `denoise_c3_hdr_gamma_2.5_f16.onnx` - HDR denoising
4. `denoise_c9_ldr_f16.onnx` - Advanced LDR denoising
5. `denoise_c9_hdr_gamma_2.5_f16.onnx` - Advanced HDR denoising

## The Plan - Apply to Gaming

### Method 1: Python + ONNX Runtime (EASIEST)
Build a Python script that:
1. Captures game frames
2. Runs through ONNX model
3. Outputs upscaled frames
4. Can work as overlay or injection

### Method 2: ReShade Integration
Use ReShade framework to inject AI processing into game rendering pipeline.

### Method 3: DirectX Hook (ADVANCED)
Create a DLL that hooks D3D11/12 and applies upscaling to frame buffer.

### Method 4: Hydra Agent (AUTOMATED)
Create a Hydra agent that monitors games and automatically applies upscaling based on performance.

## Implementation Status
- [x] Models discovered
- [ ] Models copied to project
- [ ] ONNX Runtime installed
- [ ] Python inference script
- [ ] Game injection system
- [ ] Hydra integration
