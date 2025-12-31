"""
LLM Phoneme Corrector - Cloud-Compatible Version

Graceful fallback if Ollama is unavailable (for Streamlit Cloud deployment).
"""

import requests
from typing import Optional


def correct_phonemes_with_llm(phoneme_sequence: str, timeout: int = 5) -> Optional[str]:
    """
    Correct phoneme sequence using Ollama LLM (optional - graceful fallback).
    
    Args:
        phoneme_sequence: Space-separated phoneme string
        timeout: Request timeout in seconds (short for cloud)
    
    Returns:
        Corrected text string, or None if LLM unavailable
    """
    if not phoneme_sequence or not phoneme_sequence.strip():
        return None
    
    # Try Ollama API (localhost won't work on cloud, but try anyway)
    api_url = "http://localhost:11434/api/generate"
    model = "llama3.2:3b"
    
    prompt = f"""Convert these phonemes to English text. Output ONLY the text, nothing else.

Phonemes: {phoneme_sequence}

Text:"""
    
    try:
        response = requests.post(
            api_url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            corrected_text = result.get('response', '').strip()
            
            # Clean up response
            corrected_text = _clean_response(corrected_text)
            return corrected_text
        else:
            return None
            
    except (requests.exceptions.RequestException, requests.exceptions.Timeout, ConnectionError):
        # Ollama unavailable - graceful fallback
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

