#!/usr/bin/env python3
"""
Test script to verify VOCL demo setup without Streamlit.
This helps identify issues before running the full app.
"""

import sys
import os

print("=" * 80)
print("VOCL Demo Setup Test")
print("=" * 80)
print()

# Test 1: Python version
print("1. Python Version:")
print(f"   {sys.version}")
print(f"   Executable: {sys.executable}")
print()

# Test 2: Import TensorFlow
print("2. Testing TensorFlow import...")
try:
    import tensorflow as tf
    print(f"   ✓ TensorFlow {tf.__version__} imported")
except Exception as e:
    print(f"   ✗ TensorFlow import failed: {e}")
    sys.exit(1)
print()

# Test 3: Import other dependencies
print("3. Testing other dependencies...")
deps = ['numpy', 'pandas', 'sklearn', 'matplotlib', 'requests']
for dep in deps:
    try:
        if dep == 'sklearn':
            import sklearn
            print(f"   ✓ scikit-learn imported")
        else:
            __import__(dep)
            print(f"   ✓ {dep} imported")
    except Exception as e:
        print(f"   ✗ {dep} import failed: {e}")
        sys.exit(1)
print()

# Test 4: Check model file
print("4. Checking model file...")
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'LSTM_all44_seed489_5_5_224k')
if os.path.exists(model_path):
    print(f"   ✓ Model found at: {model_path}")
else:
    print(f"   ✗ Model not found at: {model_path}")
    sys.exit(1)
print()

# Test 5: Try loading model
print("5. Testing model loading...")
try:
    # Try SavedModel format (most likely)
    model = tf.saved_model.load(model_path)
    print(f"   ✓ Model loaded successfully (SavedModel format)")
    print(f"   Signatures: {list(model.signatures.keys())}")
except Exception as e:
    print(f"   ✗ Model loading failed: {e}")
    sys.exit(1)
print()

# Test 6: Check data files
print("6. Checking data files...")
data_files = [
    os.path.join(os.path.dirname(__file__), '..', 'X_all44_3220_4_5_5.npy'),
    os.path.join(os.path.dirname(__file__), '..', 'y_all44_3220_4_5_5.npy')
]
for data_file in data_files:
    if os.path.exists(data_file):
        print(f"   ✓ Found: {os.path.basename(data_file)}")
    else:
        print(f"   ✗ Missing: {os.path.basename(data_file)}")
        sys.exit(1)
print()

# Test 7: Test pipeline import
print("7. Testing pipeline import...")
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from utils.pipeline import VOCLPipeline
    print(f"   ✓ Pipeline class imported")
except Exception as e:
    print(f"   ✗ Pipeline import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# Test 8: Test Ollama connection
print("8. Testing Ollama connection...")
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        print(f"   ✓ Ollama server is running")
    else:
        print(f"   ⚠ Ollama server returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"   ⚠ Ollama server not running (optional for testing)")
except Exception as e:
    print(f"   ⚠ Ollama check failed: {e}")
print()

print("=" * 80)
print("✓ All critical tests passed!")
print("=" * 80)
print()
print("You can now run the Streamlit app:")
print("  streamlit run vocl_demo/app.py")

