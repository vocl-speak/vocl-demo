"""
VOCL Platform Demo - Main Streamlit Application

Complete demonstration platform for VOCL (Voice Output Communication Link)
"""

import streamlit as st
import sys
import os

# Configure environment BEFORE any imports to prevent crashes
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.pipeline import get_pipeline
from components.emg_visualizer import plot_emg_signals
from components.phoneme_display import display_phonemes
from components.text_output import display_final_text
from components.phoneme_builder import (
    render_phoneme_selector,
    display_current_sequence,
    clear_sequence,
    remove_last_phoneme,
    get_phoneme_indices,
    build_emg_sequence_from_library
)

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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎤 VOCL Demo Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Voice Output Communication Link - EMG to Speech Restoration</div>', unsafe_allow_html=True)

# Initialize pipeline (with caching and error handling)
# NOTE: This loads TensorFlow - only use for Working Demo, NOT for Phoneme Builder
@st.cache_resource
def load_pipeline():
    """Load the VOCL pipeline (cached)."""
    try:
        return get_pipeline()
    except Exception as e:
        print(f"Pipeline load error (non-fatal): {e}")
        # Don't stop the app - just return None
        return None

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select Section",
        ["Working Demo", "Phoneme Builder", "Clinical Context", "Technical Details"],
        index=0
    )

# Main content based on selected page
if page == "Working Demo":
    st.header("Part 1: Working Demo")
    st.markdown("---")
    
    # Phrase selector
    st.subheader("Select a Phrase")
    
    phrase_options = {
        "Hello": 0,
        "Help me": 100,
        "I love you": 200,
        "Thank you": 300,
        "How are you": 400
    }
    
    selected_phrase = st.selectbox(
        "Choose a phrase to process:",
        options=list(phrase_options.keys()),
        index=0
    )
    
    selected_index = phrase_options[selected_phrase]
    
    # Process button
    if st.button("🚀 Process Phrase", type="primary"):
        with st.spinner("Processing EMG signals..."):
            try:
                # Get pipeline
                pipeline = load_pipeline()
                if pipeline is None:
                    st.error("Pipeline not available. Please check console for errors.")
                    st.stop()
                
                # Get phrase data
                emg_data, true_phoneme, (phoneme_seq, confidences) = pipeline.get_phrase_data(selected_index)
                
                # Store in session state
                st.session_state['emg_data'] = emg_data
                st.session_state['phoneme_sequence'] = phoneme_seq
                st.session_state['confidences'] = confidences
                st.session_state['processing'] = True
                st.session_state['error'] = None
                
            except Exception as e:
                import traceback
                error_msg = str(e)
                st.error(f"Error processing phrase: {error_msg}")
                st.code(traceback.format_exc())
                st.session_state['processing'] = False
                st.session_state['error'] = error_msg
    
    # Display results if processing is complete
    if st.session_state.get('processing', False):
        st.markdown("---")
        st.subheader("Processing Results")
        
        # 3-column layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 EMG Signals")
            if 'emg_data' in st.session_state:
                fig = plot_emg_signals(st.session_state['emg_data'])
                st.pyplot(fig)
        
        with col2:
            st.markdown("### 🗣️ Phoneme Sequence")
            if 'phoneme_sequence' in st.session_state:
                display_phonemes(
                    st.session_state['phoneme_sequence'],
                    st.session_state.get('confidences')
                )
        
        with col3:
            st.markdown("### 📝 Corrected Text")
            if 'phoneme_sequence' in st.session_state:
                phoneme_seq = st.session_state['phoneme_sequence']
                
                # Try LLM correction with Groq API (cloud-compatible)
                try:
                    from utils.cloud_llm import correct_phonemes_with_groq, is_groq_available
                    
                    if is_groq_available():
                        with st.spinner("Correcting phonemes with LLM..."):
                            # Convert string to list if needed for better processing
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
                        st.info("ℹ️ LLM correction unavailable (API key not set) - showing raw phoneme sequence")
                        st.caption("💡 Tip: Add GROQ_API_KEY to Streamlit secrets for LLM correction")
                        display_final_text(phoneme_seq, success=False)
                except ImportError:
                    st.info("ℹ️ LLM not available - showing raw phonemes")
                    display_final_text(phoneme_seq, success=False)
                except Exception as e:
                    st.warning(f"⚠️ LLM error: {str(e)[:100]}")
                    display_final_text(phoneme_seq, success=False)
        
        # Reset button
        if st.button("🔄 Process Another Phrase"):
            st.session_state['processing'] = False
            st.rerun()
    
    else:
        # Placeholder when no processing
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("👈 Select a phrase and click 'Process Phrase' to see EMG signals")
        with col2:
            st.info("👈 Phoneme sequence will appear here after processing")
        with col3:
            st.info("👈 Corrected text will appear here after LLM processing")

elif page == "Phoneme Builder":
    st.header("Part 1b: Interactive Phoneme Builder")
    st.markdown("---")
    st.markdown("Build words by selecting individual phonemes from the grid below.")
    
    # Debug: Check if API key is loaded
    with st.expander("🔍 Debug: API Key Status", expanded=False):
        try:
            api_key = st.secrets.get("GROQ_API_KEY", None)
            if api_key:
                st.success(f"✅ API Key loaded (starts with: {api_key[:10]}...)")
                st.caption(f"Full key length: {len(api_key)} characters")
            else:
                st.error("❌ API Key not found in secrets")
                st.info("Create `.streamlit/secrets.toml` with: GROQ_API_KEY = \"your_key\"")
        except Exception as e:
            st.warning(f"⚠️ Could not check secrets: {e}")
    
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
        
        # Build Word button
        if st.button("🔨 Build Word", type="primary", use_container_width=True):
            selected_phonemes = st.session_state.get('selected_phonemes', [])
            
            if not selected_phonemes:
                st.warning("Please select at least one phoneme first!")
            else:
                with st.spinner("Building word from phonemes..."):
                    print(f"\n{'='*60}")
                    print("BUILD WORD CLICKED - Starting process...")
                    print(f"Selected phonemes: {selected_phonemes}")
                    print(f"{'='*60}\n")
                    
                    try:
                        print("STEP A: Calling build_emg_sequence_from_library...")
                        # Build EMG sequence from pre-generated library (no TensorFlow!)
                        emg_data, phoneme_seq, confidences = build_emg_sequence_from_library(selected_phonemes)
                        print(f"STEP A SUCCESS: Got emg_data={emg_data is not None}, phoneme_seq='{phoneme_seq}', confidences={len(confidences)}")
                        
                        if emg_data is None:
                            print("STEP B: EMG data is None - showing error")
                            st.error("Failed to build EMG sequence. Please check that phoneme_emg_library.npz exists.")
                        else:
                            print("STEP B: Storing in session state...")
                            # Store in session state
                            st.session_state['builder_emg_data'] = emg_data
                            st.session_state['builder_phoneme_sequence'] = phoneme_seq
                            st.session_state['builder_confidences'] = confidences
                            st.session_state['builder_processing'] = True
                            st.session_state['builder_error'] = None
                            print("STEP B SUCCESS: Session state updated")
                        
                    except Exception as e:
                        import traceback
                        error_msg = str(e)
                        print(f"\n{'='*60}")
                        print(f"CRASH DETECTED: {error_msg}")
                        print(traceback.format_exc())
                        print(f"{'='*60}\n")
                        st.error(f"Error building word: {error_msg}")
                        st.code(traceback.format_exc())
                        st.session_state['builder_processing'] = False
                        st.session_state['builder_error'] = error_msg
    
    # Display results if processing is complete
    if st.session_state.get('builder_processing', False):
        st.markdown("---")
        st.subheader("📊 Built Word Results")
        
        # 3-column layout (same as Part 1)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 EMG Signals")
            if 'builder_emg_data' in st.session_state:
                try:
                    print("STEP C: Plotting EMG signals...")
                    fig = plot_emg_signals(st.session_state['builder_emg_data'])
                    st.pyplot(fig)
                    print("STEP C SUCCESS: EMG plotted")
                except Exception as e:
                    print(f"STEP C ERROR: EMG plotting failed: {e}")
                    st.warning("⚠️ EMG plotting failed - showing placeholder")
                    st.info("EMG data available but visualization failed")
        
        with col2:
            st.markdown("### 🗣️ Phoneme Sequence")
            if 'builder_phoneme_sequence' in st.session_state:
                display_phonemes(
                    st.session_state['builder_phoneme_sequence'],
                    st.session_state.get('builder_confidences')
                )
        
        with col3:
            st.markdown("### 📝 Corrected Text")
            if 'builder_phoneme_sequence' in st.session_state:
                phoneme_seq = st.session_state['builder_phoneme_sequence']
                
                # Try LLM correction with Groq API (cloud-compatible)
                print("STEP D: Attempting LLM correction with Groq...")
                try:
                    from utils.cloud_llm import correct_phonemes_with_groq, is_groq_available
                    
                    # Check if Groq is available
                    if is_groq_available():
                        print("STEP D.1: Groq API key found, calling API...")
                        with st.spinner("Correcting phonemes with LLM..."):
                            # Convert string to list if needed for better processing
                            if isinstance(phoneme_seq, str):
                                phoneme_list = phoneme_seq.split()
                            else:
                                phoneme_list = phoneme_seq
                            
                            corrected_text = correct_phonemes_with_groq(phoneme_list, timeout=15)
                            print(f"STEP D.1 Result: {corrected_text}")
                            
                            if corrected_text and len(corrected_text.strip()) > 0:
                                print("STEP D SUCCESS: Groq LLM correction worked")
                                display_final_text(corrected_text, success=True)
                            else:
                                print("STEP D FALLBACK: Groq returned empty - showing raw phonemes")
                                st.info("ℹ️ LLM correction unavailable - showing raw phoneme sequence")
                                display_final_text(phoneme_seq, success=False)
                    else:
                        print("STEP D FALLBACK: Groq API key not configured")
                        st.info("ℹ️ LLM correction unavailable (API key not set) - showing raw phoneme sequence")
                        st.caption("💡 Tip: Add GROQ_API_KEY to Streamlit secrets for LLM correction")
                        display_final_text(phoneme_seq, success=False)
                            
                except ImportError:
                    print("STEP D ERROR: Cannot import Groq LLM")
                    st.info("ℹ️ LLM not available - showing raw phonemes")
                    display_final_text(phoneme_seq, success=False)
                except Exception as e:
                    # Complete fallback - just show phonemes
                    print(f"STEP D ERROR: {e}")
                    st.warning(f"⚠️ LLM error: {str(e)[:100]}")
                    display_final_text(phoneme_seq, success=False)
        
        # Reset button
        if st.button("🔄 Build Another Word"):
            st.session_state['builder_processing'] = False
            st.rerun()
    
    else:
        # Placeholder when no processing
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("👈 Select phonemes and click 'Build Word' to see EMG signals")
        with col2:
            st.info("👈 Phoneme sequence will appear here after building")
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
