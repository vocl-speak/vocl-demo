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

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Phoneme Builder", "Exhibits"],
        index=0
    )

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
    if page == "Phoneme Builder":
        st.markdown('<div class="main-header">VOCL Phoneme Builder</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Electromyographic Signal Analysis & Phoneme Reconstruction</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-header">Visualization Exhibits</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">EMG Signal Correlation Analysis</div>', unsafe_allow_html=True)

# Main content
st.markdown("---")

if page == "Exhibits":
    st.markdown("## 📊 Visualization Exhibits")
    st.markdown("---")
    st.markdown("""
    This section presents visualizations demonstrating the **98.34% cosine similarity** 
    between silent and vocalized+whispered speech EMG signals. Each exhibit shows 
    the correlation from a different analytical perspective.
    """)
    
    # Define exhibits with their images and explanations
    # Images are in vocl_demo/exhibits_images/ folder (renamed for clarity)
    def get_image_path(filename):
        """Get image path that works both locally and on Streamlit Cloud."""
        # Simple approach: use relative path from app.py location
        # Streamlit Cloud runs from repo root, so path is vocl_demo/exhibits_images/filename.png
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, 'exhibits_images', filename)
        
        # Return the path - Streamlit will resolve it correctly
        return image_path
    
    exhibits = [
        {
            "title": "1. Scatter Plot: Mean Feature Vectors",
            "image": get_image_path("scatter_mean_features.png"),
            "explanation": """
            **WHAT IT IS:** A scatter plot where each point represents one feature dimension (out of 160 features).
            - X-axis = Mean feature value for Silent speech (normalized)
            - Y-axis = Mean feature value for Vocalized+Whispered speech (normalized)
            
            **WHAT IT SHOWS:**
            - Each dot = one feature's average value in both conditions
            - Red dashed line = Perfect correlation line (y=x)
            - Green line = Actual trend line through the data points
            
            **HOW IT PROVES HIGH CORRELATION:**
            ✓ Points cluster tightly along the diagonal (y=x line) → Features follow the same pattern in both conditions
            ✓ Trend line is very close to the perfect correlation line → Strong relationship, not just coincidence
            ✓ The closer points are to y=x, the higher the correlation
            
            **KEY INSIGHT:** If conditions were UNcorrelated, points would be scattered randomly. Instead, they form a clear diagonal pattern = STRONG CORRELATION.
            """
        },
        {
            "title": "2. Radar Chart: Feature Profile Comparison",
            "image": get_image_path("radar_chart_features.png"),
            "explanation": """
            **WHAT IT IS:** A circular (radar/spider) chart comparing the top 12 most important features.
            Each axis represents one feature dimension showing the "profile" or "signature" of each condition.
            
            **WHAT IT SHOWS:**
            - Red polygon = Silent speech feature profile
            - Green polygon = Vocalized+Whispered feature profile
            - Each axis = One feature dimension (F0, F1, F2, etc.)
            - Distance from center = Feature value magnitude
            
            **HOW IT PROVES HIGH CORRELATION:**
            ✓ The two polygons have SIMILAR SHAPES → Both conditions activate features in similar patterns
            ✓ Polygons overlap substantially → Feature values are similar across conditions
            ✓ When red goes up, green also goes up → Features change together, indicating correlation
            
            **KEY INSIGHT:** If conditions were different, polygons would have different shapes. Similar shapes = Similar activation patterns = HIGH CORRELATION.
            """
        },
        {
            "title": "3. Violin Plots: Feature Distribution Comparison",
            "image": get_image_path("violin_plots_features.png"),
            "explanation": """
            **WHAT IT IS:** Four side-by-side comparisons showing the distribution of feature values.
            Each plot shows one feature, with distributions for both conditions.
            Violin shape = Distribution density (wider = more samples at that value)
            
            **WHAT IT SHOWS:**
            - Left violin (red) = Silent speech distribution
            - Right violin (green) = Vocalized+Whispered distribution
            - Width = How many samples have that feature value
            - White dot = Mean value
            - Thick line = Median value
            
            **HOW IT PROVES HIGH CORRELATION:**
            ✓ Overlapping violins = Similar distributions → Both conditions have similar feature value ranges
            ✓ Similar shapes = Similar patterns → Features behave similarly across conditions
            ✓ Means/medians are close = Similar central tendencies → Average activation is similar
            
            **KEY INSIGHT:** If conditions were different, violins would be separated and different shapes. Overlapping violins with similar shapes = HIGH CORRELATION.
            """
        },
        {
            "title": "4. Bar Chart: Cosine Similarity with Context",
            "image": get_image_path("cosine_similarity_bar_chart.png"),
            "explanation": """
            **WHAT IT IS:** A bar chart comparing your result (0.9834) to reference values.
            Shows where your result falls on the similarity scale.
            
            **WHAT IT SHOWS:**
            - Five bars: Perfect Match (1.0), Your Result (0.9834), High (0.9), Moderate (0.7), Low (0.5)
            - Your result bar is highlighted in red
            - Each bar shows the value as both number and percentage
            
            **HOW IT PROVES HIGH CORRELATION:**
            ✓ Your result (0.9834) is VERY CLOSE to Perfect Match (1.0) → Almost identical feature patterns
            ✓ Your result is HIGHER than "High Similarity" (0.9) → Exceeds the threshold for strong correlation
            ✓ Only 1.66% away from perfect (100% - 98.34% = 1.66%) → Extremely high similarity
            
            **KEY INSIGHT:** This chart CONTEXTUALIZES the number - showing that 0.98 is not "some correlation" but "VERY HIGH correlation" (almost perfect).
            """
        },
        {
            "title": "5. t-SNE with Density Contours",
            "image": get_image_path("tsne_with_contours.png"),
            "explanation": """
            **WHAT IT IS:** A 2D visualization of the high-dimensional feature space (160 dimensions → 2D).
            Each point = one EMG sample (256 silent + 256 vocalized+whispered)
            Contour lines = Density of samples (like a topographic map)
            
            **WHAT IT SHOWS:**
            - Red points = Silent speech samples
            - Green points = Vocalized+Whispered samples
            - Contour lines = Regions where many samples cluster
            - Overlapping contours = Shared clustering regions
            
            **HOW IT PROVES HIGH CORRELATION:**
            ✓ Red and green points are MIXED TOGETHER, not separated → Samples from both conditions occupy similar feature space
            ✓ Contour lines OVERLAP substantially → Both conditions cluster in the same regions
            ✓ No clear separation between conditions → They share feature space, indicating correlation
            
            **KEY INSIGHT:** If conditions were UNcorrelated, you'd see two separate clusters. Instead, you see ONE overlapping cluster = HIGH CORRELATION.
            """
        },
        {
            "title": "6. Feature-by-Feature Correlation Scatter",
            "image": get_image_path("feature_correlations_scatter.png"),
            "explanation": """
            **WHAT IT IS:** A scatter plot showing the correlation coefficient for each individual feature.
            Each point = One feature's correlation between Silent and V+W conditions.
            Features are sorted by correlation strength (strongest first).
            
            **WHAT IT SHOWS:**
            - X-axis = Feature index (sorted by correlation strength)
            - Y-axis = Pearson correlation coefficient (-1 to +1)
            - Green points = Strong correlation (>0.7)
            - Orange points = Moderate correlation (0.4-0.7)
            - Red points = Weak correlation (<0.4)
            
            **HOW IT PROVES HIGH CORRELATION:**
            ✓ Many features have HIGH correlation (>0.7, shown in green) → Many features match well between conditions
            ✓ Overall pattern shows more green/orange than red → Most features correlate positively
            ✓ The average of these correlations supports the 98.34% cosine similarity → Granular analysis confirms overall similarity
            
            **KEY INSIGHT:** This shows the GRANULAR detail - not just overall similarity, but WHICH features contribute most. Many strong correlations = HIGH OVERALL CORRELATION.
            """
        },
        {
            "title": "7. Cosine Similarity Visualization (Vector Angle)",
            "image": get_image_path("cosine_similarity_visualization.png"),
            "explanation": """
            **WHAT IT IS:** A geometric visualization showing the angle between the two feature vectors.
            Shows cosine similarity as the angle between vectors in 2D space.
            
            **WHAT IT SHOWS:**
            - Red arrow = Silent speech mean feature vector (direction)
            - Green arrow = Vocalized+Whispered mean feature vector (direction)
            - Blue arc = Angle between vectors (10.5°)
            - Unit circle = Reference circle
            
            **HOW IT PROVES HIGH CORRELATION:**
            ✓ Small angle (10.5°) = Vectors point in almost the SAME direction → Feature patterns are almost identical
            ✓ Angle is very close to 0° (perfect match) → Very high similarity
            ✓ Cosine similarity = cos(angle) = cos(10.5°) = 0.9834 → Mathematical proof of high correlation
            
            **KEY INSIGHT:** This is the GEOMETRIC PROOF - showing that 0.98 cosine similarity means the vectors are only 10.5° apart (almost parallel). This is VERY HIGH similarity.
            """
        }
    ]
    
    # Display each exhibit
    for i, exhibit in enumerate(exhibits):
        st.markdown(f"### {exhibit['title']}")
        
        # Two-column layout: Image on left, Explanation on right
        col_img, col_exp = st.columns([1, 1])
        
        with col_img:
            try:
                st.image(exhibit['image'], use_container_width=True)
            except Exception as e:
                st.error(f"Could not load image: {exhibit['image']}")
                st.caption(f"Error: {str(e)}")
        
        with col_exp:
            st.markdown(exhibit['explanation'])

        if i < len(exhibits) - 1:
            st.markdown("---")
    
    # Summary section
    st.markdown("---")
    st.markdown("### Summary: How All Visualizations Work Together")
    st.markdown("""
    Each visualization proves correlation in a different way:
    
    1. **SCATTER PLOT** → Shows the RELATIONSHIP (points cluster on diagonal)
    2. **RADAR CHART** → Shows the PATTERN (similar shapes)
    3. **VIOLIN PLOTS** → Shows the DISTRIBUTION (overlapping distributions)
    4. **BAR CHART** → Shows the CONTEXT (98% is very high)
    5. **t-SNE CONTOURS** → Shows the CLUSTERING (overlapping clusters)
    6. **FEATURE SCATTER** → Shows the DETAILS (many features correlate)
    7. **ANGLE VISUALIZATION** → Shows the MATH (10.5° angle = high similarity)
    
    **TOGETHER, these prove:**
    - Silent and vocalized+whispered speech share **98.34% feature space similarity**
    - This similarity is visible in multiple ways (scatter, radar, distributions)
    - The finding is robust (consistent across visualization methods)
    - Transfer learning is scientifically justified
    """)

else:  # Phoneme Builder page
    # Two-column layout: Left = Phoneme selector, Right = Current sequence + Build button
    col_left, col_right = st.columns([2.5, 1])
    
    with col_left:
        st.markdown("### Phoneme Selection Grid")
        st.caption("Select phonemes from the grid below to build your word. Each phoneme represents a distinct EMG signal pattern.")
        
        # Tabs for vowels and consonants
        tab1, tab2 = st.tabs(["Vowels", "Consonants"])
        
        with tab1:
            render_phoneme_selector("vowels")
        
        with tab2:
            render_phoneme_selector("consonants")
    
    with col_right:
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
            else:
                with st.spinner("Processing EMG signals..."):
                    try:
                        # Build EMG sequence from pre-generated library
                        emg_windows, phoneme_seq, _ = build_emg_sequence_from_library(selected_phonemes)
                        
                        if emg_windows is None or len(emg_windows) == 0:
                            st.error("❌ Failed to build EMG sequence. Please check that phoneme_emg_library.npz exists.")
                        else:
                            # Store in session state
                            st.session_state['builder_emg_windows'] = emg_windows
                            st.session_state['builder_phoneme_sequence'] = phoneme_seq
                            st.session_state['builder_phonemes_list'] = phoneme_seq.split() if isinstance(phoneme_seq, str) else phoneme_seq
                            st.session_state['builder_processing'] = True
                            st.session_state['builder_error'] = None
                        
                    except Exception as e:
                        import traceback
                        error_msg = str(e)
                        st.error(f"❌ Error building word: {error_msg}")
                        st.code(traceback.format_exc())
                        st.session_state['builder_processing'] = False
                        st.session_state['builder_error'] = error_msg
    
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
                    st.warning("⚠️ Could not generate EMG plots")
                except Exception as e:
                import traceback
                    st.warning("⚠️ EMG plotting failed - showing placeholder")
                st.error(f"Error: {str(e)}")
                st.code(traceback.format_exc())
        
        # Two-column layout for phonemes and text
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
