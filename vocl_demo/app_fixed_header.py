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
