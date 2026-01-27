import requests
import time
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_generation_logging():
    print("=== Testing API Generation Logging ===")
    
    # 1. Start a fake generation (using the same structure as command interface)
    payload = {
        "title": "Log_Test_Song",
        "genre": "Test",
        "bpm": 100,
        "structure": [
            {"type": "intro", "bars": 2, "text": "Test"}
        ],
        "duration_target": 5 # Short
    }
    
    try:
        print("Sending generation request...")
        res = requests.post(f"{BASE_URL}/generate", json=payload)
        if res.status_code != 200:
            print(f"FAILED: Status {res.status_code} - {res.text}")
            return
            
        task_id = res.json()["task_id"]
        print(f"Task ID: {task_id}")
        
        # 2. Poll for logs
        print("Polling for logs...")
        max_retries = 20
        has_tqdm_log = False
        
        for _ in range(max_retries):
            status_res = requests.get(f"{BASE_URL}/status/{task_id}")
            data = status_res.json()
            
            logs = data.get("logs", [])
            progress = data.get("progress", 0)
            status = data.get("status", "unknown")
            
            print(f"Status: {status} | Progress: {progress}% | Log Lines: {len(logs)}")
            
            # Check for tqdm patterns in logs
            # Look for something like "10/100" or "%"
            for line in logs:
                if "%" in line and "/" in line and "[" in line:
                    print(f"VICTORY: Found tqdm-like log: {line.strip()}")
                    has_tqdm_log = True
                    break
            
            if status in ["completed", "failed"]:
                print("Task finished.")
                break
                
            if has_tqdm_log:
                print("Logs are confirmed flowing!")
                break
                
            time.sleep(1)
            
        if has_tqdm_log:
            print("SUCCESS: Logs captured correctly.")
        else:
            print("WARNING: Did not see clear tqdm logs (might be too fast or capture failed).")
            print("Dump of last 5 logs:")
            for l in logs[-5:]:
                print(f" - {l}")
                
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_generation_logging()
