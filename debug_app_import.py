import sys
import os
# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

print("Attempting to import app.main...")
try:
    from app.main import app
    print("Success: app.main imported")
except Exception as e:
    import traceback
    traceback.print_exc()
