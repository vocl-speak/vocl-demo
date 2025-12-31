"""
VOCL Platform Demo - Pre-generated Data Version

This version loads pre-computed results from JSON files instead of
running TensorFlow inference. Perfect for demos - no crashes, instant loading!
"""

import streamlit as st
import json
import os
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="VOCL Demo",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load demo data
DEMO_DATA_FILE = os.path.join(os.path.dirname(__file__), 'demo_data', 'demo_phrases.json')

@st.cache_data
def load_demo_data():
    """Load pre-generated demo data."""
    if not os.path.exists(DEMO_DATA_FILE):
        return None
    
    with open(DEMO_DATA_FILE, 'r') as f:
        return json.load(f)


def plot_emg_signals(emg_data):
    """Plot 4-channel EMG signals."""
    channels = ['DLI', 'OOS', 'OOI', 'Platysma']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    fig.suptitle('EMG Signal Channels', fontsize=14, fontweight='bold')
    
    time_points = np.arange(5) * 4  # 4ms per sample
    
    for i, (channel, color) in enumerate(zip(channels, colors)):
        axes[i].plot(time_points, emg_data[i], marker='o', color=color, linewidth=2, markersize=6)
        axes[i].set_ylabel(channel, fontweight='bold')
        axes[i].grid(True, alpha=0.3)
        axes[i].set_ylim([0, 1])  # Normalized data range
    
    axes[-1].set_xlabel('Time (ms)', fontweight='bold')
    plt.tight_layout()
    
    return fig


def display_phonemes(phoneme_sequence, confidences=None):
    """Display phoneme sequence with confidence scores."""
    st.subheader("📝 Phoneme Sequence")
    
    if confidences:
        phonemes = phoneme_sequence.split()
        cols = st.columns(min(len(phonemes), 10))
        
        for i, (phoneme, conf) in enumerate(zip(phonemes, confidences)):
            with cols[i % len(cols)]:
                st.metric(
                    label=phoneme,
                    value=f"{conf:.1%}",
                    delta=None
                )
    else:
        st.code(phoneme_sequence, language=None)
    
    with st.expander("View full sequence"):
        st.text(phoneme_sequence)


def display_final_text(text, success=True):
    """Display final corrected text."""
    st.subheader("✨ Final Text Output")
    
    if success and text and not text.startswith("Error") and not text.startswith("LLM"):
        st.success("✓ Conversion Successful")
        st.markdown(f"### {text}")
        st.caption("Text generated from EMG signals via phoneme classification and LLM correction")
    else:
        st.info("ℹ️ " + text)
        st.caption("Pre-generated result")


# Header
st.markdown('<div class="main-header">🎤 VOCL Demo Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Voice Output Communication Link - EMG to Speech Restoration</div>', unsafe_allow_html=True)

# Load demo data
demo_data = load_demo_data()

if demo_data is None:
    st.error("⚠️ Demo data not found!")
    st.markdown(f"""
    **File not found:** `{DEMO_DATA_FILE}`
    
    **To generate demo data:**
    1. Run in your working Python environment:
       ```bash
       python3 generate_demo_data.py
       ```
    2. This will create the JSON file with pre-computed results
    3. Then refresh this page
    """)
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select Section",
        ["Working Demo", "Clinical Context", "Technical Details"],
        index=0
    )

# Main content
if page == "Working Demo":
    st.header("Part 1: Working Demo")
    st.markdown("---")
    
    # Phrase selector
    st.subheader("Select a Phrase")
    
    phrase_options = list(demo_data.keys())
    
    selected_phrase = st.selectbox(
        "Choose a phrase to process:",
        options=phrase_options,
        index=0
    )
    
    # Process button
    if st.button("🚀 Process Phrase", type="primary"):
        st.session_state['selected_phrase'] = selected_phrase
        st.session_state['processing'] = True
    
    # Display results
    if st.session_state.get('processing', False) and 'selected_phrase' in st.session_state:
        selected_phrase = st.session_state['selected_phrase']
        phrase_data = demo_data[selected_phrase]
        
        st.markdown("---")
        st.subheader("Processing Results")
        
        # 3-column layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 EMG Signals")
            emg_data = np.array(phrase_data['emg_data'])
            fig = plot_emg_signals(emg_data)
            st.pyplot(fig)
        
        with col2:
            display_phonemes(
                phrase_data['phoneme_sequence'],
                phrase_data.get('confidences')
            )
        
        with col3:
            display_final_text(phrase_data['corrected_text'], success=True)
        
        # Reset button
        if st.button("🔄 Process Another Phrase"):
            st.session_state['processing'] = False
            st.rerun()
    
    else:
        # Placeholder
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("👈 Select a phrase and click 'Process Phrase' to see EMG signals")
        with col2:
            st.info("👈 Phoneme sequence will appear here after processing")
        with col3:
            st.info("👈 Corrected text will appear here after LLM processing")

elif page == "Clinical Context":
    st.header("Part 2: Clinical Context")
    st.markdown("---")
    st.info("Clinical context section will be implemented in CHECKPOINT B3")

elif page == "Technical Details":
    st.header("Part 3: Technical Details")
    st.markdown("---")
    st.info("Technical details section will be implemented in CHECKPOINT B4")

