# Crash Diagnostic & Fix

## Issue
Python crashes with "mutex lock failed" when importing TensorFlow. This is a known issue on macOS with:
- Python 3.9 from Command Line Tools
- TensorFlow 2.x
- Protobuf version conflicts

## Quick Test
Run this to verify TensorFlow works:
```bash
python3 test_tf_simple.py
```

If it crashes, TensorFlow cannot be used in this environment.

## Solutions

### Option 1: Use Python 3.10+ (Recommended)
```bash
# Install Python 3.10+ via Homebrew
brew install python@3.10
python3.10 -m pip install tensorflow streamlit numpy pandas scikit-learn matplotlib requests
python3.10 -m streamlit run vocl_demo/app.py
```

### Option 2: Use Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install tensorflow==2.15.0 streamlit numpy pandas scikit-learn matplotlib requests
streamlit run vocl_demo/app.py
```

### Option 3: Downgrade Protobuf (Temporary)
```bash
pip install protobuf==3.20.3
```

### Option 4: Use Conda Environment
```bash
conda create -n vocl python=3.10
conda activate vocl
pip install tensorflow streamlit numpy pandas scikit-learn matplotlib requests
streamlit run vocl_demo/app.py
```

## Current Status
The app code is ready, but TensorFlow crashes on import in your current Python 3.9 environment.

