"""
Text Output Component

Component for displaying corrected text output in the Streamlit demo.
"""

import streamlit as st


def display_final_text(text, success=True):
    """
    Display final corrected text with success indicator.
    
    Args:
        text: Corrected text string
        success: Whether the correction was successful
    """
    st.subheader("✨ Final Text Output")
    
    if success and text and not text.startswith("Error"):
        # Success state
        st.success("✓ Conversion Successful")
        st.markdown(f"### {text}")
        st.caption("Text generated from EMG signals via phoneme classification and LLM correction")
    else:
        # Error state
        st.error("✗ Conversion Failed")
        st.code(text)
        st.caption("An error occurred during processing")
