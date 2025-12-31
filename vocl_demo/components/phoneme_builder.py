"""
Phoneme Builder Component

Interactive component for building phoneme sequences by selecting individual phonemes.
Uses pre-generated EMG library (no TensorFlow inference required).
"""

import streamlit as st
import json
import os
import numpy as np


def load_phoneme_library():
    """Load phoneme library from JSON file."""
    lib_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'phoneme_library.json')
    with open(lib_path, 'r') as f:
        return json.load(f)


@st.cache_resource
def load_emg_library():
    """
    Load pre-generated EMG library (cached).
    
    Returns:
        Dictionary mapping phoneme names to their EMG data and metadata
    """
    lib_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'phoneme_emg_library.npz')
    
    if not os.path.exists(lib_path):
        st.error(f"EMG library not found at {lib_path}. Please run generate_phoneme_library.py first.")
        return None
    
    try:
        data = np.load(lib_path, allow_pickle=True)
        
        # Extract metadata
        phonemes = data.get('metadata_phonemes', [])
        if len(phonemes) == 0:
            # Fallback: extract from keys
            phonemes = [k.replace('_emg', '') for k in data.keys() if k.endswith('_emg')]
        
        # Build library dictionary
        library = {}
        for phoneme in phonemes:
            emg_key = f"{phoneme}_emg"
            if emg_key in data:
                library[phoneme] = {
                    'emg_data': data[emg_key],
                    'phoneme_index': int(data.get(f"{phoneme}_index", 0)),
                    'confidence': float(data.get(f"{phoneme}_confidence", 0.8)),
                    'sample_index': int(data.get(f"{phoneme}_sample_idx", 0))
                }
        
        return library
    except Exception as e:
        st.error(f"Error loading EMG library: {e}")
        return None


def render_phoneme_selector(phoneme_type="vowels"):
    """
    Render a grid of clickable phoneme buttons.
    
    Args:
        phoneme_type: "vowels" or "consonants"
    
    Returns:
        Selected phoneme or None
    """
    library = load_phoneme_library()
    phonemes = library.get(phoneme_type, {})
    
    if not phonemes:
        return None
    
    # Initialize session state for selected phonemes if not exists
    if 'selected_phonemes' not in st.session_state:
        st.session_state['selected_phonemes'] = []
    
    st.subheader(f"{phoneme_type.capitalize()}")
    
    # Create grid layout (4 columns)
    cols = st.columns(4)
    col_idx = 0
    
    for phoneme, info in sorted(phonemes.items()):
        with cols[col_idx % 4]:
            # Create button with phoneme info
            button_label = f"{phoneme}\n({info['example']})"
            
            if st.button(
                button_label,
                key=f"phoneme_{phoneme_type}_{phoneme}",
                use_container_width=True
            ):
                # Add to selected phonemes
                st.session_state['selected_phonemes'].append(phoneme)
                st.rerun()
        
        col_idx += 1
    
    return None


def display_current_sequence():
    """Display the currently selected phoneme sequence."""
    if 'selected_phonemes' not in st.session_state:
        st.session_state['selected_phonemes'] = []
    
    selected = st.session_state['selected_phonemes']
    
    st.subheader("📝 Current Sequence")
    
    if selected:
        # Display as badges
        sequence_text = " ".join(selected)
        st.code(sequence_text, language=None)
        
        # Show phoneme count
        st.caption(f"{len(selected)} phoneme(s) selected")
        
        # Show examples
        library = load_phoneme_library()
        examples = []
        for phoneme in selected:
            # Find phoneme in library
            found = False
            for category in ['vowels', 'consonants']:
                if phoneme in library[category]:
                    examples.append(library[category][phoneme]['example'])
                    found = True
                    break
            if not found:
                examples.append("?")
        
        st.caption(f"Examples: {' - '.join(examples)}")
    else:
        st.info("👈 Select phonemes from the grid to build your sequence")
        st.code("", language=None)
    
    return selected


def clear_sequence():
    """Clear the selected phoneme sequence."""
    if st.button("🗑️ Clear Sequence", use_container_width=True):
        st.session_state['selected_phonemes'] = []
        st.rerun()


def remove_last_phoneme():
    """Remove the last phoneme from the sequence."""
    if st.button("↩️ Remove Last", use_container_width=True):
        if st.session_state.get('selected_phonemes'):
            st.session_state['selected_phonemes'].pop()
            st.rerun()


def get_phoneme_indices(phoneme_sequence):
    """
    Convert phoneme sequence to indices for EMG data lookup.
    
    Args:
        phoneme_sequence: List of phoneme strings
    
    Returns:
        List of phoneme indices
    """
    library = load_phoneme_library()
    indices = []
    
    for phoneme in phoneme_sequence:
        found = False
        for category in ['vowels', 'consonants']:
            if phoneme in library[category]:
                indices.append(library[category][phoneme]['index'])
                found = True
                break
        if not found:
            # Default to 0 (silence) if not found
            indices.append(0)
    
    return indices


def build_emg_sequence_from_library(phoneme_sequence):
    """
    Build EMG sequence from pre-generated library (no TensorFlow required).
    
    Args:
        phoneme_sequence: List of phoneme strings
    
    Returns:
        Tuple of (representative_emg_data, phoneme_string, confidences)
    """
    print(f"STEP 1: Starting build_emg_sequence_from_library with {len(phoneme_sequence)} phonemes")
    
    try:
        print("STEP 2: Loading EMG library...")
        emg_library = load_emg_library()
        
        if emg_library is None:
            print("STEP 2 ERROR: EMG library is None")
            return None, "", []
        
        print(f"STEP 2 SUCCESS: Loaded {len(emg_library)} phonemes from library")
        
        if not phoneme_sequence:
            print("STEP 3: Empty phoneme sequence")
            return None, "", []
        
        print("STEP 3: Processing phonemes...")
        # Get EMG data for each phoneme
        emg_windows = []
        phonemes = []
        confidences = []
        
        for i, phoneme in enumerate(phoneme_sequence):
            print(f"  STEP 3.{i+1}: Processing phoneme '{phoneme}'...")
            if phoneme in emg_library:
                emg_window = emg_library[phoneme]['emg_data']
                confidence = emg_library[phoneme]['confidence']
                
                emg_windows.append(emg_window)
                phonemes.append(phoneme)
                confidences.append(confidence)
                print(f"  STEP 3.{i+1} SUCCESS: Found '{phoneme}' in library")
            else:
                print(f"  STEP 3.{i+1} WARNING: Phoneme '{phoneme}' not found in library")
                st.warning(f"Phoneme '{phoneme}' not found in library")
        
        if not emg_windows:
            print("STEP 4 ERROR: No EMG windows collected")
            return None, "", []
        
        print("STEP 4: Creating representative EMG...")
        # Use first window as representative (for visualization)
        representative_emg = emg_windows[0]
        
        print("STEP 5: Creating phoneme string...")
        # Create phoneme string
        phoneme_string = ' '.join(phonemes)
        
        print(f"STEP 6 SUCCESS: Returning sequence '{phoneme_string}' with {len(confidences)} confidences")
        return representative_emg, phoneme_string, confidences
        
    except Exception as e:
        print(f"CRASH in build_emg_sequence_from_library: {e}")
        import traceback
        print(traceback.format_exc())
        st.error(f"Error building EMG sequence: {e}")
        return None, "", []
