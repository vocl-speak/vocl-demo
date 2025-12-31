"""
Phoneme Display Component

Component for displaying phoneme sequences in the Streamlit demo.
"""

import streamlit as st


def display_phonemes(phoneme_sequence, confidences=None):
    """
    Display phoneme sequence with optional confidence scores.
    
    Args:
        phoneme_sequence: Space-separated phoneme string
        confidences: Optional list of confidence scores
    """
    st.subheader("📝 Phoneme Sequence")
    
    if confidences:
        # Display with confidence bars
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
        # Simple display
        st.code(phoneme_sequence, language=None)
    
    # Show full sequence
    with st.expander("View full sequence"):
        st.text(phoneme_sequence)
