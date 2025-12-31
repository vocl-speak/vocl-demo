# Crash Fix Guide

## Problem
Python crashes with "mutex lock failed" during TensorFlow/PyArrow initialization on macOS.

## Root Cause
- Protobuf version conflict (TensorFlow uses 5.28.3, runtime has 6.31.1)
- Threading issues during library initialization
- Multiple library initialization conflicts

## Solution Applied
1. **Lazy TensorFlow Loading**: Only import TensorFlow when needed
2. **Single Threading**: Disable multiprocessing/threading
3. **Environment Variables**: Set before any imports
4. **Error Handling**: Better error messages and graceful failures

## Testing
Run the test script first:
```bash
python3 vocl_demo/test_setup.py
```

If it crashes, the issue is with TensorFlow initialization, not the app.

## Alternative: Use Virtual Environment
If crashes persist, consider using a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install tensorflow streamlit numpy pandas scikit-learn matplotlib requests
```

## Alternative: Use Python 3.10+
The crashes are more common with Python 3.9. Consider upgrading to Python 3.10+ if possible.

