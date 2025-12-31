"""
VOCL Platform Demo - Minimal Version (Crash-Proof)

Simplified version for debugging - no complex operations that can crash.
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from components.phoneme_builder import (
    render_phoneme_selector,
    display_current_sequence,
    clear_sequence,
    remove_last_phoneme
)

# Page configuration
st.set_page_config(
    page_title="VOCL Demo (Minimal)",
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎤 VOCL Demo Platform (Minimal)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Voice Output Communication Link - EMG to Speech Restoration</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select Section",
        ["Working Demo", "Phoneme Builder", "Clinical Context", "Technical Details"],
        index=1  # Start on Phoneme Builder
    )

# Main content
if page == "Phoneme Builder":
    st.header("Part 1b: Interactive Phoneme Builder (Minimal)")
    st.markdown("---")
    st.info("🔧 **Minimal Version** - This version shows phoneme sequences without complex operations to avoid crashes.")
    
    # Two-column layout: Left = Phoneme selector, Right = Current sequence + Build button
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("🔤 Phoneme Selector")
        
        # Tabs for vowels and consonants
        tab1, tab2 = st.tabs(["Vowels", "Consonants"])
        
        with tab1:
            render_phoneme_selector("vowels")
        
        with tab2:
            render_phoneme_selector("consonants")
    
    with col_right:
        display_current_sequence()
        
        # Control buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            remove_last_phoneme()
        with col_btn2:
            clear_sequence()
        
        st.markdown("---")
        
        # Build Word button - MINIMAL VERSION (no complex operations)
        if st.button("🔨 Build Word", type="primary", use_container_width=True):
            selected_phonemes = st.session_state.get('selected_phonemes', [])
            
            if not selected_phonemes:
                st.warning("Please select at least one phoneme first!")
            else:
                # MINIMAL: Just show the sequence - no EMG, no LLM, no TensorFlow
                phoneme_string = " ".join(selected_phonemes)
                
                # Store in session state
                st.session_state['builder_phoneme_sequence'] = phoneme_string
                st.session_state['builder_processing'] = True
                
                st.success("✓ Word built successfully!")
    
    # Display results if processing is complete
    if st.session_state.get('builder_processing', False):
        st.markdown("---")
        st.subheader("📊 Built Word Results (Minimal)")
        
        # Simple display - no complex components
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 EMG Signals")
            st.info("🔧 EMG plotting disabled in minimal version")
            st.caption("(Will be enabled once basic version works)")
        
        with col2:
            st.markdown("### 🗣️ Phoneme Sequence")
            if 'builder_phoneme_sequence' in st.session_state:
                phoneme_seq = st.session_state['builder_phoneme_sequence']
                st.code(phoneme_seq, language=None)
                st.caption(f"{len(phoneme_seq.split())} phoneme(s)")
            else:
                st.info("No sequence built yet")
        
        with col3:
            st.markdown("### 📝 Corrected Text")
            if 'builder_phoneme_sequence' in st.session_state:
                phoneme_seq = st.session_state['builder_phoneme_sequence']
                st.info("🔧 LLM correction disabled in minimal version")
                st.caption("Raw phonemes:")
                st.markdown(f"## **{phoneme_seq}**")
            else:
                st.info("No sequence built yet")
        
        # Reset button
        if st.button("🔄 Build Another Word"):
            st.session_state['builder_processing'] = False
            st.rerun()
    
    else:
        # Placeholder when no processing
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("👈 Select phonemes and click 'Build Word'")
        with col2:
            st.info("👈 Phoneme sequence will appear here")
        with col3:
            st.info("👈 Text will appear here")

elif page == "Working Demo":
    st.header("Part 1: Working Demo")
    st.markdown("---")
    st.info("🔧 Working Demo section - use main app.py for full version")

elif page == "Clinical Context":
    st.header("Part 2: Clinical Context")
    st.markdown("---")
    st.info("Clinical context section will be implemented in CHECKPOINT B3")

elif page == "Technical Details":
    st.header("Part 3: Technical Details")
    st.markdown("---")
    st.info("Technical details section will be implemented in CHECKPOINT B4")

