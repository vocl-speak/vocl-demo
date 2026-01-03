"""
VOCL Phoneme Builder - Scientific EMG Analysis Interface

Interactive phoneme builder with advanced EMG signal visualization.
"""

import streamlit as st
import sys
import os
import base64

# Configure environment
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'

# Add current directory to path (for Streamlit Cloud compatibility)
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from components.emg_visualizer import plot_phoneme_emg_grid
from components.phoneme_display import display_phonemes
from components.text_output import display_final_text
from components.phoneme_builder import (
render_phoneme_selector,
display_current_sequence,
clear_sequence,
remove_last_phoneme,
build_emg_sequence_from_library
)

# Page configuration
st.set_page_config(
page_title="VOCL Phoneme Builder",
page_icon=None,  # Using custom favicon via JavaScript below
layout="wide",
initial_sidebar_state="expanded"
)

# Add favicon using JavaScript (runs after page load)
try:
    logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = base64.b64encode(f.read()).decode()
        favicon_script = f"""
        <script>
            (function() {{
                const link = document.createElement('link');
                link.rel = 'icon';
                link.type = 'image/png';
                link.href = 'data:image/png;base64,{logo_data}';
                // Remove existing favicon if any
                const existing = document.querySelector('link[rel="icon"]');
                if (existing) existing.remove();
                document.head.appendChild(link);
            }})();
        </script>
        """
        st.markdown(favicon_script, unsafe_allow_html=True)
except:
    pass

# Initialize session state variables if they don't exist
if 'selected_phonemes' not in st.session_state:
    st.session_state['selected_phonemes'] = []
if 'builder_processing' not in st.session_state:
    st.session_state['builder_processing'] = False
if 'builder_error' not in st.session_state:
    st.session_state['builder_error'] = None

# Scientific UI CSS
st.markdown("""
<style>
/* Main styling - text centered in its column (from logo right to page right) */
.main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        width: 100%;
}
.sub-header {
        font-size: 1rem;
        color: #666666;
        text-align: center;
        margin-bottom: 0;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
}

/* Ensure the title column centers its content */
div[data-testid="column"]:has(.main-header) {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
}

/* Scientific color scheme - Black & White with subtle accents */
:root {
        --primary-black: #000000;
        --primary-dark: #1a1a1a;
        --accent-gray: #4a4a4a;
        --accent-light: #e0e0e0;
        --bg-light: #fafafa;
        --bg-card: #ffffff;
        --text-primary: #000000;
        --text-secondary: #666666;
        --border-color: #d0d0d0;
}

/* Card styling */
.stContainer {
        background-color: var(--bg-card);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
}

/* Button styling */
.stButton>button {
        width: 100%;
        background: #000000;
        color: white !important;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        border: 2px solid #000000;
        transition: all 0.3s ease;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
}
.stButton>button:hover {
        background: #1a1a1a;
        color: white !important;
        border-color: #1a1a1a;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
.stButton>button:focus {
        color: white !important;
        background: #000000;
}
.stButton>button:active {
        color: white !important;
        background: #000000;
}

/* Phoneme buttons */
button[kind="secondary"] {
        background: #000000 !important;
        color: white !important;
        border: 2px solid #000000 !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
}
button[kind="secondary"]:hover {
        background: #1a1a1a !important;
        border-color: #1a1a1a !important;
        color: white !important;
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}
button[kind="secondary"]:focus {
        color: white !important;
        background: #000000 !important;
}
button[kind="secondary"]:active {
        color: white !important;
        background: #000000 !important;
}

/* Section headers */
h2 {
        color: #000000;
        font-weight: 700;
        font-size: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #000000;
        padding-bottom: 0.5rem;
}

h3 {
        color: #1a1a1a;
        font-weight: 600;
        font-size: 1.2rem;
        margin-top: 1rem;
}

/* Info boxes */
.stInfo {
        background-color: #f5f5f5;
        border-left: 4px solid #000000;
        border-radius: 4px;
}

/* Code blocks */
.stCodeBlock {
        background-color: #f5f7fa;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 1rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
        gap: 8px;
}
.stTabs [data-baseweb="tab"] {
        background-color: #f5f5f5;
        border-radius: 6px 6px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
}
.stTabs [aria-selected="true"] {
        background-color: #000000;
        color: white;
}

/* Metric cards */
.metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Remove default Streamlit styling */
.main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
}

/* Sequence display */
.phoneme-sequence {
        background: #fafafa;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #000000;
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-align: center;
        color: #000000;
}
</style>
""", unsafe_allow_html=True)

# Navigation removed - only Phoneme Builder page

# Header with Logo - text centered from logo right edge to page right edge
col_logo, col_title = st.columns([1.2, 8.8])
with col_logo:
    try:
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        if os.path.exists(logo_path):
            st.image(logo_path, width=120)
        else:
            st.image('vocl_demo/logo.png', width=120)
    except:
        try:
            st.image('logo.png', width=120)
        except:
            pass

with col_title:
    # Use CSS to center text in this column (which spans from logo right to page right)
st.markdown('<div class="main-header">VOCL Phoneme Builder</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Electromyographic Signal Analysis & Phoneme Reconstruction</div>', unsafe_allow_html=True)

# Product Description
st.markdown("""
**VOCL** is a non-invasive, wearable headset that measures electromyographic (EMG) signals from facial muscles during subvocalization (silent speech). By classifying phonemes and reconstructing natural language, VOCL enables silent communication for individuals with speech impairments.

This interactive demonstration simulates the VOCL experience. Build phoneme sequences through subvocalization patterns, then visualize real-world EMG signals captured from actual users. Each phoneme represents distinct muscle activation patterns that VOCL learns to recognize and translate into speech.
""")

# Main content
st.markdown("---")

# Two-column layout: Left = Phoneme selector, Right = Current sequence + Build button
col_left, col_right = st.columns([2.5, 1])

    st.markdown("### Phoneme Selection Grid")
st.caption("Select phonemes from the grid below to build your word. Each phoneme represents a distinct EMG signal pattern.")
        
        # Tabs for vowels and consonants
        tab1, tab2 = st.tabs(["Vowels", "Consonants"])
        
        with tab1:
            render_phoneme_selector("vowels")
        
        with tab2:
            render_phoneme_selector("consonants")

    st.markdown("### Current Sequence")
        display_current_sequence()
        
        # Control buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            remove_last_phoneme()
        with col_btn2:
            clear_sequence()
        
st.markdown("---")
        
        # Build Word button
if st.button("🔬 Analyze EMG Signals", type="primary", use_container_width=True):
            selected_phonemes = st.session_state.get('selected_phonemes', [])
            
            if not selected_phonemes:
            st.warning("⚠️ Please select at least one phoneme first!")
            st.rerun()
            else:
            with st.spinner("Processing EMG signals..."):
                try:
                    # Build EMG sequence from pre-generated library
                    emg_windows, phoneme_seq, _ = build_emg_sequence_from_library(selected_phonemes)
                    
                    if emg_windows is None or len(emg_windows) == 0:
                        st.error("❌ Failed to build EMG sequence. Please check that phoneme_emg_library.npz exists.")
                        st.session_state['builder_processing'] = False
                        else:
                            # Store in session state
                        st.session_state['builder_emg_windows'] = emg_windows
                            st.session_state['builder_phoneme_sequence'] = phoneme_seq
                        st.session_state['builder_phonemes_list'] = phoneme_seq.split() if isinstance(phoneme_seq, str) else phoneme_seq
                            st.session_state['builder_processing'] = True
                            st.session_state['builder_error'] = None
                    
                    st.rerun()
                        
                    except Exception as e:
                        import traceback
                        error_msg = str(e)
                    st.error(f"❌ Error building word: {error_msg}")
                        st.code(traceback.format_exc())
                        st.session_state['builder_processing'] = False
                        st.session_state['builder_error'] = error_msg
                    st.rerun()

    # Display results if processing is complete
    if st.session_state.get('builder_processing', False):
    st.markdown("---")
    st.markdown("## Analysis Results")

    # EMG Signals Section (Full Width)
    st.markdown("### Electromyographic Signal Visualization")
    st.caption("Interactive EMG signals for each phoneme. Use zoom, pan, and hover tools to explore the data.")

    if 'builder_emg_windows' in st.session_state and 'builder_phonemes_list' in st.session_state:
        try:
            emg_windows = st.session_state['builder_emg_windows']
            phonemes = st.session_state['builder_phonemes_list']
            
            # Use matplotlib visualization
            fig = plot_phoneme_emg_grid(emg_windows, phonemes)
            if fig:
                st.pyplot(fig, use_container_width=True)
            else:
                st.warning("Could not generate EMG plots")
        except Exception as e:
            import traceback
            st.warning("EMG plotting failed - showing placeholder")
            st.error(f"Error: {str(e)}")
            st.code(traceback.format_exc())

    # Two-column layout: Left = Phoneme selector, Right = Current sequence + Build button
    col1, col2 = st.columns(2)
        
        with col1:
        st.markdown("### Phoneme Sequence")
        if 'builder_phoneme_sequence' in st.session_state:
            display_phonemes(st.session_state['builder_phoneme_sequence'])
        
        with col2:
        st.markdown("### Reconstructed Text")
            if 'builder_phoneme_sequence' in st.session_state:
                phoneme_seq = st.session_state['builder_phoneme_sequence']
                
            # Try LLM correction with Groq API
                try:
                    from utils.cloud_llm import correct_phonemes_with_groq, is_groq_available
                    
                    if is_groq_available():
                        with st.spinner("Correcting phonemes with LLM..."):
                            if isinstance(phoneme_seq, str):
                                phoneme_list = phoneme_seq.split()
        else:
                                phoneme_list = phoneme_seq
                            
                            corrected_text = correct_phonemes_with_groq(phoneme_list, timeout=15)
                            
                            if corrected_text and len(corrected_text.strip()) > 0:
                                display_final_text(corrected_text, success=True)
        else:
                                st.info("ℹ️ LLM correction unavailable - showing raw phoneme sequence")
                                display_final_text(phoneme_seq, success=False)
                    else:
                    st.info("ℹ️ LLM correction unavailable (API key not set)")
                        st.caption("💡 Tip: Add GROQ_API_KEY to Streamlit secrets for LLM correction")
                        display_final_text(phoneme_seq, success=False)
                            
                except ImportError:
                    st.info("ℹ️ LLM not available - showing raw phonemes")
                    display_final_text(phoneme_seq, success=False)
                except Exception as e:
                    st.warning(f"⚠️ LLM error: {str(e)[:100]}")
                    display_final_text(phoneme_seq, success=False)
        
        # Reset button
    st.markdown("---")
    if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state['builder_processing'] = False
            st.rerun()

    else:
        # Placeholder when no processing
    st.markdown("---")
    st.info("👈 Select phonemes from the grid above and click 'Analyze EMG Signals' to begin analysis.")
