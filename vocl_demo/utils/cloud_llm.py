"""
Cloud-Compatible LLM using Groq API

Fast, free LLM correction that works on Streamlit Cloud.
"""

import os
import streamlit as st
from typing import Optional, List, Union


def correct_phonemes_with_groq(phoneme_sequence: Union[str, List[str]], timeout: int = 15) -> Optional[str]:
    """
    Correct phoneme sequence using Groq API (cloud-compatible).
    
    Args:
        phoneme_sequence: Space-separated phoneme string or list of phonemes
                          e.g., "HH EH L OW" or ["HH", "EH", "L", "OW"]
        timeout: Request timeout in seconds
    
    Returns:
        Corrected text string (e.g., "hello") or None if unavailable
    """
    try:
        # Convert list to string if needed
        if isinstance(phoneme_sequence, list):
            phonemes_str = " ".join(phoneme_sequence)
        else:
            phonemes_str = phoneme_sequence.strip()
        
        if not phonemes_str:
            st.warning("⚠️ Empty phoneme sequence")
            return None
        
        # Get API key from Streamlit secrets (cloud) or environment (local)
        api_key = None
        try:
            # Try Streamlit secrets first (for cloud deployment)
            api_key = st.secrets.get("GROQ_API_KEY", None)
        except (AttributeError, FileNotFoundError, KeyError):
            # Fallback to environment variable (for local development)
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            st.warning("⚠️ API key not found. Add GROQ_API_KEY to .streamlit/secrets.toml")
            return None
        
        # Import Groq (lazy import to avoid errors if not installed)
        try:
            from groq import Groq
        except ImportError:
            st.error("❌ Groq library not installed. Run: pip install groq")
            return None
        
        # Initialize Groq client
        client = Groq(api_key=api_key)
        
        # Create prompt - improved for better results
        prompt = f"""Convert these phonemes to natural English text. Output ONLY the text, nothing else.

Phonemes: {phonemes_str}

Text:"""
        
        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Fast, accurate model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=50,
            timeout=timeout
        )
        
        # Extract text
        text = response.choices[0].message.content.strip()
        
        # Clean up any remaining formatting
        text = text.replace('"', '').replace("'", "").strip()
        
        # Remove common LLM artifacts
        text = _clean_response(text)
        
        if not text:
            st.warning("⚠️ LLM returned empty response")
            return None
        
        return text
        
    except Exception as e:
        # Show detailed error for debugging
        error_msg = str(e)
        st.error(f"❌ LLM Error: {error_msg}")
        
        # Show traceback in expander for debugging
        with st.expander("🔍 Error Details", expanded=False):
            import traceback
            st.code(traceback.format_exc())
        
        # Return None to trigger fallback
        return None


def _clean_response(text: str) -> str:
    """Clean LLM response text."""
    import re
    
    # Remove common LLM artifacts
    text = re.sub(r'^Text:\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^Output:\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^Result:\s*', '', text, flags=re.IGNORECASE)
    
    # Remove quotes if entire response is quoted
    text = text.strip('"\'')
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def is_groq_available() -> bool:
    """
    Check if Groq API is available (has API key).
    
    Returns:
        True if API key is configured, False otherwise
    """
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
        if api_key:
            return True
    except (AttributeError, FileNotFoundError, KeyError):
        pass
    
    # Check environment variable
    api_key = os.getenv("GROQ_API_KEY")
    return api_key is not None and len(api_key.strip()) > 0

