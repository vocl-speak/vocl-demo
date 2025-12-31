"""
VOCL Platform Demo - Safe Version (with TensorFlow crash protection)

This version checks if TensorFlow can be imported before starting.
"""

import streamlit as st
import sys
import os

# Configure environment FIRST
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'

# Page configuration
st.set_page_config(
    page_title="VOCL Demo",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Test TensorFlow import before proceeding
@st.cache_resource
def check_tensorflow():
    """Check if TensorFlow can be imported safely."""
    try:
        import tensorflow as tf
        return True, f"TensorFlow {tf.__version__}", None
    except Exception as e:
        return False, None, str(e)

# Header
st.markdown('<div class="main-header">🎤 VOCL Demo Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Voice Output Communication Link - EMG to Speech Restoration</div>', unsafe_allow_html=True)

# Check TensorFlow
tf_ok, tf_version, tf_error = check_tensorflow()

if not tf_ok:
    st.error("⚠️ TensorFlow Import Failed")
    st.markdown("---")
    st.warning("**TensorFlow cannot be imported in this environment.**")
    st.markdown("""
    This is a known issue on macOS with Python 3.9 and TensorFlow.
    
    **Solutions:**
    1. **Upgrade to Python 3.10+** (Recommended)
       ```bash
       brew install python@3.10
       python3.10 -m pip install tensorflow streamlit
       python3.10 -m streamlit run vocl_demo/app.py
       ```
    
    2. **Use Virtual Environment**
       ```bash
       python3 -m venv venv
       source venv/bin/activate
       pip install tensorflow streamlit
       streamlit run vocl_demo/app.py
       ```
    
    3. **Downgrade Protobuf**
       ```bash
       pip install protobuf==3.20.3
       ```
    """)
    
    with st.expander("Error Details"):
        st.code(tf_error)
    
    st.stop()

# If TensorFlow works, proceed with normal app
st.success(f"✓ TensorFlow {tf_version} loaded successfully")

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.pipeline import get_pipeline
from components.emg_visualizer import plot_emg_signals
from components.phoneme_display import display_phonemes
from components.text_output import display_final_text

# Rest of the app code...
st.info("App is ready! Use the navigation sidebar to access features.")

