import torch
import torch_directml
import time

def test_dml():
    print("Testing DirectML availability...")
    try:
        device = torch_directml.device()
        print(f"Device found: {device}")
        
        print("Creating tensor on CPU...")
        x = torch.tensor([1.0, 2.0, 3.0])
        print(f"x: {x}, device: {x.device}")
        
        print("Moving to DirectML device...")
        x_dml = x.to(device)
        print(f"x_dml: {x_dml}, device: {x_dml.device}")
        
        print("Performing operation (multiplication)...")
        y_dml = x_dml * 2
        print(f"y_dml: {y_dml}")
        
        assert torch.equal(y_dml.cpu(), torch.tensor([2.0, 4.0, 6.0]))
        print("Operation successful!")
        
        print("Testing float16 support...")
        x_half = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float16).to(device)
        y_half = x_half * 2
        print(f"y_half: {y_half}, dtype: {y_half.dtype}")
        
        print("DirectML Test PASSED.")
        
    except Exception as e:
        print(f"DirectML Test FAILED: {e}")
        # Identify if it's the specific DirectML assert error
        if "INTERNAL ASSERT FAILED" in str(e):
             print("\nNote: This might be a known issue with torch-directml versions. Ensure compatibility.")

if __name__ == "__main__":
    test_dml()
