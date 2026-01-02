"""
Phoneme Display Component

Component for displaying phoneme sequences in the Streamlit demo.
"""

import streamlit as st


def display_phonemes(phoneme_sequence, confidences=None):
    """
    Display phoneme sequence.
    
    Args:
        phoneme_sequence: Space-separated phoneme string
        confidences: Ignored (kept for backward compatibility)
    """
    # Display phonemes in a clean format
    phonemes = phoneme_sequence.split() if isinstance(phoneme_sequence, str) else phoneme_sequence
    
    # Create a visual display with badges
    phoneme_display = " ".join([f"**{p}**" for p in phonemes])
    st.markdown(phoneme_display)
    
    # Show full sequence in code block
    sequence_text = " ".join(phonemes)
    st.code(sequence_text, language=None)
