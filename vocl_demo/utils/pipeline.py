"""
VOCL Pipeline Utilities

Utility functions for the full VOCL pipeline:
- Model loading
- Phoneme prediction
- LLM correction
"""

import numpy as np
import os
import sys

# Configure environment BEFORE any TensorFlow import to prevent crashes
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# Disable multiprocessing/threading to avoid crashes on macOS
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'
os.environ['TF_DISABLE_MKL'] = '1'  # Disable MKL threading

# Lazy import TensorFlow - only import when needed to avoid crashes
tf = None

def _import_tensorflow():
    """Lazy import TensorFlow with error handling."""
    global tf
    if tf is None:
        try:
            import tensorflow as tf
            # Configure TensorFlow to use single thread
            tf.config.threading.set_inter_op_parallelism_threads(1)
            tf.config.threading.set_intra_op_parallelism_threads(1)
        except Exception as e:
            raise RuntimeError(f"Failed to import TensorFlow: {e}")
    return tf

# Import cloud LLM corrector (cloud-compatible)
from .cloud_llm import correct_phonemes_with_groq

# Phoneme class list
PHONEMES = ['_', 'B', 'D', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'V', 'W', 'Y', 'Z', 'CH', 'SH', 'NG', 'DH', 'TH', 'ZH', 'WH', 'AA', 'AI(R)', 'I(R)', 'A(R)', 'ER', 'EY', 'IY', 'AY', 'OW', 'UW', 'AE', 'EH', 'IH', 'AO', 'AH', 'UH', 'OO', 'AW', 'OY']

# Model path (relative to neurotechML directory)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../models/LSTM_all44_seed489_5_5_224k')
X_DATA_PATH = os.path.join(os.path.dirname(__file__), '../../X_all44_3220_4_5_5.npy')
Y_DATA_PATH = os.path.join(os.path.dirname(__file__), '../../y_all44_3220_4_5_5.npy')


class VOCLPipeline:
    """
    Complete VOCL pipeline: EMG → Phonemes → Text
    """
    
    def __init__(self):
        """Initialize the pipeline with model and LLM corrector."""
        self.model = None
        self.corrector = None
        self.X_test = None
        self.y_test = None
        self._load_model()
        self._load_data()
        self._load_corrector()
    
    def _load_model(self):
        """Load the trained EMG model."""
        tf = _import_tensorflow()
        
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        
        try:
            # Try SavedModel format first (most likely)
            model = tf.saved_model.load(MODEL_PATH)
            infer = model.signatures["serving_default"]
            
            class SavedModelWrapper:
                def __init__(self, infer_func):
                    self.infer = infer_func
                def predict(self, x, verbose=0):
                    if isinstance(x, np.ndarray):
                        x = tf.constant(x, dtype=tf.float32)
                    output = self.infer(x)
                    result = list(output.values())[0]
                    return result.numpy()
            
            self.model = SavedModelWrapper(infer)
        except Exception as e1:
            # Try Keras format as fallback
            try:
                self.model = tf.keras.models.load_model(MODEL_PATH, safe_mode=False)
            except Exception as e2:
                raise RuntimeError(f"Failed to load model: SavedModel error: {e1}, Keras error: {e2}")
    
    def _load_data(self):
        """Load test data for phrase selection."""
        from sklearn.model_selection import train_test_split
        
        if not os.path.exists(X_DATA_PATH) or not os.path.exists(Y_DATA_PATH):
            raise FileNotFoundError(f"Data files not found: {X_DATA_PATH} or {Y_DATA_PATH}")
        
        X = np.load(X_DATA_PATH)
        y = np.load(Y_DATA_PATH)
        X = X.reshape(-1, 4, 5)
        
        _, self.X_test, _, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=489
        )
    
    def _load_corrector(self):
        """Load LLM corrector (cloud-compatible, no initialization needed)."""
        # Cloud LLM doesn't need initialization - it's called directly
        # Keep self.corrector for compatibility but it's not used
        self.corrector = True  # Indicates LLM is available
    
    def get_phrase_data(self, index: int):
        """
        Get EMG data for a specific phrase index.
        
        Args:
            index: Index in test dataset
            
        Returns:
            Tuple of (emg_data, true_label, phoneme_sequence)
        """
        if index >= len(self.X_test):
            index = index % len(self.X_test)
        
        emg_data = self.X_test[index]
        true_label = self.y_test[index]
        true_phoneme = PHONEMES[true_label]
        
        # Generate phoneme sequence (simulate multiple predictions)
        phoneme_sequence = self._generate_phoneme_sequence(emg_data)
        
        return emg_data, true_phoneme, phoneme_sequence
    
    def _generate_phoneme_sequence(self, emg_data, length=10):
        """
        Generate a phoneme sequence from EMG data.
        
        Args:
            emg_data: Single EMG sample (4, 5)
            length: Desired sequence length
            
        Returns:
            Tuple of (phoneme_string, confidences_list)
        """
        # Predict phoneme for this sample
        sample = emg_data.reshape(1, 4, 5)
        prediction = self.model.predict(sample, verbose=0)
        predicted_idx = np.argmax(prediction[0])
        confidence = prediction[0][predicted_idx]
        
        # Create a sequence by repeating with variations
        phonemes = []
        confidences = []
        
        for i in range(length):
            # Add some variation to make it more realistic
            if i == 0:
                phoneme = PHONEMES[predicted_idx]
                conf = confidence
            else:
                # Use top predictions for variation
                top_indices = np.argsort(prediction[0])[-3:][::-1]
                idx = top_indices[i % len(top_indices)]
                phoneme = PHONEMES[idx]
                conf = prediction[0][idx]
            
            if phoneme != '_':  # Skip silence
                phonemes.append(phoneme)
                confidences.append(conf)
        
        return ' '.join(phonemes), confidences[:len(phonemes)]
    
    def correct_phonemes(self, phoneme_sequence: str):
        """
        Correct phoneme sequence to text using cloud LLM (Groq API).
        
        Args:
            phoneme_sequence: Space-separated phoneme string
            
        Returns:
            Corrected text string, or None if LLM fails
        """
        if self.corrector is None:
            return None
        
        try:
            # Convert string to list for cloud_llm function
            if isinstance(phoneme_sequence, str):
                phoneme_list = phoneme_sequence.split()
            else:
                phoneme_list = phoneme_sequence
            
            # Use cloud LLM function
            result = correct_phonemes_with_groq(phoneme_list, timeout=15)
            
            # Return result or None
            if result and len(result.strip()) > 0:
                return result
            else:
                return None
        except Exception as e:
            # Return None to indicate failure (caller will handle gracefully)
            print(f"LLM correction error: {e}")
            return None
    
    def get_emg_for_phoneme(self, phoneme_index: int):
        """
        Get EMG data sample for a specific phoneme index.
        
        Args:
            phoneme_index: Index of phoneme in PHONEMES list
            
        Returns:
            EMG data array of shape (4, 5) or None if not found
        """
        # Find first occurrence of this phoneme in test data
        matching_indices = np.where(self.y_test == phoneme_index)[0]
        
        if len(matching_indices) > 0:
            # Return first match
            idx = matching_indices[0]
            return self.X_test[idx]
        else:
            # Return a default/random sample if phoneme not found
            return self.X_test[0]
    
    def build_emg_sequence(self, phoneme_indices: list):
        """
        Build concatenated EMG sequence from list of phoneme indices.
        
        Args:
            phoneme_indices: List of phoneme indices
            
        Returns:
            Tuple of (concatenated_emg_data, phoneme_sequence_string, confidences)
        """
        if not phoneme_indices:
            return None, "", []
        
        # Get EMG data for each phoneme
        emg_windows = []
        phonemes = []
        confidences = []
        
        for phoneme_idx in phoneme_indices:
            emg_window = self.get_emg_for_phoneme(phoneme_idx)
            emg_windows.append(emg_window)
            phonemes.append(PHONEMES[phoneme_idx])
        
        # Concatenate EMG windows along time axis
        # Each window is (4, 5), we'll stack them to create (4, 5*N)
        concatenated_emg = np.concatenate(emg_windows, axis=1)
        
        # For display, we'll use the first window (4, 5) as representative
        # In a real scenario, you'd process the full concatenated sequence
        representative_emg = emg_windows[0]
        
        # Generate phoneme sequence and confidences
        phoneme_string = ' '.join(phonemes)
        
        # Generate confidences by predicting each phoneme
        for emg_window in emg_windows:
            sample = emg_window.reshape(1, 4, 5)
            prediction = self.model.predict(sample, verbose=0)
            predicted_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_idx])
            confidences.append(confidence)
        
        return representative_emg, phoneme_string, confidences


# Global pipeline instance
_pipeline = None

def get_pipeline():
    """Get or create the global pipeline instance."""
    global _pipeline
    if _pipeline is None:
        _pipeline = VOCLPipeline()
    return _pipeline
