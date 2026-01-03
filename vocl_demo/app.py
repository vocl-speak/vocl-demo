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
            **What it is:** A scatter plot where each point represents one feature dimension (out of 160 features).
            - X-axis = Mean feature value for Silent speech (normalized)
            - Y-axis = Mean feature value for Vocalized+Whispered speech (normalized)
            
            **What it shows:**
            - Each dot represents one feature's average value in both conditions
            - Red dashed line shows the perfect correlation line (y=x)
            - Green line shows the actual trend line through the data points
            
            **What this suggests about correlation:**
            The points appear to cluster along the diagonal (y=x line), which suggests features might follow similar patterns in both conditions. The trend line seems close to the perfect correlation line, indicating there may be a relationship between the conditions. Generally, the closer points are to y=x, the stronger the correlation appears to be.
            
            **Takeaway:** If the conditions were uncorrelated, we might expect points to be scattered randomly. Instead, they seem to form a diagonal pattern, which could indicate some level of correlation between silent and vocalized+whispered speech.
            """
        },
        {
            "title": "2. Radar Chart: Feature Profile Comparison",
            "image": get_image_path("radar_chart_features.png"),
            "explanation": """
            **What it is:** A circular (radar/spider) chart comparing the top 12 most important features.
            Each axis represents one feature dimension showing the "profile" or "signature" of each condition.
            
            **What it shows:**
            - Red polygon represents the Silent speech feature profile
            - Green polygon represents the Vocalized+Whispered feature profile
            - Each axis represents one feature dimension (F0, F1, F2, etc.)
            - Distance from center indicates feature value magnitude
            
            **What this suggests about correlation:**
            The two polygons appear to have similar shapes, which might indicate that both conditions activate features in comparable patterns. The polygons seem to overlap substantially, suggesting feature values could be similar across conditions. When one polygon goes up on an axis, the other tends to follow, which could indicate features change together.
            
            **Takeaway:** If the conditions were quite different, we might expect the polygons to have noticeably different shapes. The similar shapes we observe here could suggest similar activation patterns, though this would need further validation.
            """
        },
        {
            "title": "3. Violin Plots: Feature Distribution Comparison",
            "image": get_image_path("violin_plots_features.png"),
            "explanation": """
            **What it is:** Four side-by-side comparisons showing the distribution of feature values.
            Each plot shows one feature, with distributions for both conditions.
            The violin shape represents distribution density (wider areas indicate more samples at that value).
            
            **What it shows:**
            - Left violin (red) shows the Silent speech distribution
            - Right violin (green) shows the Vocalized+Whispered distribution
            - Width indicates how many samples have that feature value
            - White dot marks the mean value
            - Thick line marks the median value
            
            **What this suggests about correlation:**
            The violins appear to overlap, which could indicate similar distributions and that both conditions might have comparable feature value ranges. The shapes seem somewhat similar, suggesting features might behave similarly across conditions. The means and medians appear relatively close, which could indicate similar central tendencies.
            
            **Takeaway:** If the conditions were quite different, we might expect the violins to be more separated with different shapes. The overlapping violins with similar shapes we see here might suggest some level of correlation, though this interpretation should be considered alongside other evidence.
            """
        },
        {
            "title": "4. Bar Chart: Cosine Similarity with Context",
            "image": get_image_path("cosine_similarity_bar_chart.png"),
            "explanation": """
            **What it is:** A bar chart comparing the result (0.9834) to reference values.
            This helps contextualize where the result falls on the similarity scale.
            
            **What it shows:**
            - Five bars: Perfect Match (1.0), Your Result (0.9834), High (0.9), Moderate (0.7), Low (0.5)
            - Your result bar is highlighted in red
            - Each bar shows the value as both number and percentage
            
            **What this suggests about correlation:**
            The result (0.9834) appears relatively close to Perfect Match (1.0), which might suggest the feature patterns could be quite similar. The result seems higher than the "High Similarity" threshold (0.9), though what constitutes "strong" correlation can depend on the context. The result is about 1.66% away from perfect, which seems like a relatively small difference.
            
            **Takeaway:** This chart helps put the number in context. A value of 0.98 appears to indicate fairly high similarity, though the interpretation depends on the specific application and what level of similarity is meaningful for the task at hand.
            """
        },
        {
            "title": "5. t-SNE with Density Contours",
            "image": get_image_path("tsne_with_contours.png"),
            "explanation": """
            **What it is:** A 2D visualization of the high-dimensional feature space (160 dimensions reduced to 2D).
            Each point represents one EMG sample (256 silent + 256 vocalized+whispered).
            Contour lines show density of samples, similar to a topographic map.
            
            **What it shows:**
            - Red points represent Silent speech samples
            - Green points represent Vocalized+Whispered samples
            - Contour lines indicate regions where many samples cluster
            - Overlapping contours suggest shared clustering regions
            
            **What this suggests about correlation:**
            The red and green points appear mixed together rather than clearly separated, which might indicate that samples from both conditions could occupy similar regions in feature space. The contour lines seem to overlap substantially, suggesting both conditions might cluster in comparable regions. There doesn't appear to be a clear separation between conditions, which could indicate they share some feature space.
            
            **Takeaway:** If the conditions were uncorrelated, we might expect to see two more distinct clusters. The overlapping pattern we observe here could suggest some level of correlation, though t-SNE is a nonlinear reduction technique and should be interpreted with caution.
            """
        },
        {
            "title": "6. Feature-by-Feature Correlation Scatter",
            "image": get_image_path("feature_correlations_scatter.png"),
            "explanation": """
            **What it is:** A scatter plot showing the correlation coefficient for each individual feature.
            Each point represents one feature's correlation between Silent and V+W conditions.
            Features are sorted by correlation strength (strongest first).
            
            **What it shows:**
            - X-axis = Feature index (sorted by correlation strength)
            - Y-axis = Pearson correlation coefficient (-1 to +1)
            - Green points indicate strong correlation (>0.7)
            - Orange points indicate moderate correlation (0.4-0.7)
            - Red points indicate weak correlation (<0.4)
            
            **What this suggests about correlation:**
            Many features appear to have relatively high correlation (>0.7, shown in green), which might suggest that many features could match reasonably well between conditions. The overall pattern seems to show more green and orange points than red, which could indicate that most features correlate positively to some degree. The distribution of these correlations seems consistent with the overall 98.34% cosine similarity measure.
            
            **Takeaway:** This provides a more granular view - showing not just overall similarity, but which individual features might contribute most to that similarity. The presence of many strong correlations could support the idea of overall correlation, though individual feature correlations can vary.
            """
        },
        {
            "title": "7. Cosine Similarity Visualization (Vector Angle)",
            "image": get_image_path("cosine_similarity_visualization.png"),
            "explanation": """
            **What it is:** A geometric visualization showing the angle between the two feature vectors.
            This illustrates cosine similarity as the angle between vectors in 2D space.
            
            **What it shows:**
            - Red arrow represents the Silent speech mean feature vector (direction)
            - Green arrow represents the Vocalized+Whispered mean feature vector (direction)
            - Blue arc shows the angle between vectors (10.5°)
            - Unit circle provides a reference scale
            
            **What this suggests about correlation:**
            The angle appears relatively small (10.5°), which might suggest the vectors point in similar directions. The angle seems close to 0° (which would be a perfect match), indicating potentially high similarity. The cosine similarity calculation gives cos(10.5°) = 0.9834, which is the mathematical relationship between the angle and the similarity measure.
            
            **Takeaway:** This provides a geometric interpretation of the cosine similarity measure. A value of 0.98 corresponds to vectors that are about 10.5° apart, which seems like a relatively small angle. Whether this represents "very high" similarity depends on the specific application and what level of similarity is meaningful for the task.
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
    Each visualization approaches the question of correlation from a different angle:
    
    1. **Scatter Plot** - Examines the relationship between feature values (points clustering on diagonal)
    2. **Radar Chart** - Compares feature activation patterns (similar shapes)
    3. **Violin Plots** - Looks at distribution overlap (overlapping distributions)
    4. **Bar Chart** - Provides context for the similarity measure (98% relative to other benchmarks)
    5. **t-SNE Contours** - Explores clustering patterns (overlapping clusters)
    6. **Feature Scatter** - Breaks down individual feature contributions (many features show correlation)
    7. **Angle Visualization** - Shows the geometric interpretation (10.5° angle corresponds to the similarity measure)
    
    **Taken together, these visualizations suggest:**
    - Silent and vocalized+whispered speech appear to share approximately 98.34% feature space similarity
    - This similarity seems to be visible across multiple visualization approaches
    - The patterns appear consistent across different analytical methods
    - These findings could potentially support the feasibility of transfer learning approaches, though further validation would be needed
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
                    st.warning("Could not generate EMG plots")
            except Exception as e:
                import traceback
                st.warning("EMG plotting failed - showing placeholder")
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
