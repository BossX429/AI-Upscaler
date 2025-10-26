"""
AMD AI Upscaler - Inference Engine
Uses cloned ONNX models for real-time 2x upscaling
"""

import numpy as np
import onnxruntime as ort
from PIL import Image
import time

class AMDUpscaler:
    def __init__(self, model_path="models/upscale2x_c3_rt_f16.onnx"):
        """Initialize the AI upscaler with AMD's ONNX model"""
        print(f"Loading model: {model_path}")
        
        # Create ONNX Runtime session
        # Use DirectML execution provider for AMD GPUs
        providers = ['DmlExecutionProvider', 'CPUExecutionProvider']
        self.session = ort.InferenceSession(model_path, providers=providers)
        
        # Get model input/output details
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        
        print(f"✓ Model loaded successfully")
        print(f"  Provider: {self.session.get_providers()[0]}")
        print(f"  Input: {self.input_name}")
        print(f"  Output: {self.output_name}")
    
    def upscale_image(self, image_path, output_path=None):
        """Upscale a single image 2x"""
        
        # Load and preprocess image
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img).astype(np.float32) / 255.0
        
        # ONNX expects NCHW format (batch, channels, height, width)
        # PIL gives us HWC (height, width, channels)
        img_array = np.transpose(img_array, (2, 0, 1))  # HWC -> CHW
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        
        # Run inference
        start_time = time.time()
        outputs = self.session.run([self.output_name], {self.input_name: img_array})
        inference_time = time.time() - start_time
        
        # Post-process output
        output = outputs[0][0]  # Remove batch dimension
        output = np.transpose(output, (1, 2, 0))  # CHW -> HWC
        output = np.clip(output * 255.0, 0, 255).astype(np.uint8)
        
        # Convert back to image
        upscaled = Image.fromarray(output)
        
        print(f"✓ Upscaled: {img.size} -> {upscaled.size}")
        print(f"  Inference time: {inference_time*1000:.2f}ms")
        
        if output_path:
            upscaled.save(output_path)
            print(f"  Saved to: {output_path}")
        
        return upscaled

    
    def upscale_array(self, img_array):
        """Upscale a numpy array (for real-time processing)"""
        # Ensure float32 and normalized
        if img_array.dtype != np.float32:
            img_array = img_array.astype(np.float32) / 255.0
        
        # Convert to NCHW if needed
        if len(img_array.shape) == 3:  # HWC
            img_array = np.transpose(img_array, (2, 0, 1))
            img_array = np.expand_dims(img_array, axis=0)
        
        # Run inference
        outputs = self.session.run([self.output_name], {self.input_name: img_array})
        
        # Post-process
        output = outputs[0][0]
        output = np.transpose(output, (1, 2, 0))
        output = np.clip(output * 255.0, 0, 255).astype(np.uint8)
        
        return output


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("AMD AI UPSCALER - Cloned Technology")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage: python upscaler.py <image_path> [output_path]")
        print("\nExample:")
        print("  python upscaler.py test.jpg test_upscaled.jpg")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "upscaled_output.jpg"
    
    # Initialize upscaler
    upscaler = AMDUpscaler()
    
    # Upscale image
    upscaler.upscale_image(input_path, output_path)
    
    print("\n✓ Done!")
