# VOCL Demo Platform

**Voice Output Communication Link** - Non-invasive EMG-based speech restoration system.

## 🚀 Live Demo

[Live App URL will appear here after deployment to Streamlit Cloud]

## 📋 Features

- **Working Demo**: Process 5 pre-built phrases with full pipeline visualization
- **Interactive Phoneme Builder**: Build words by selecting individual phonemes
- **Real-time EMG Visualization**: 4-channel EMG signal plots
- **LLM Phoneme Correction**: Converts phoneme sequences to readable text (optional)

## 🛠️ Local Setup

### Prerequisites
- Python 3.9+
- pip

### Installation

1. **Clone or download this repository**
   ```bash
   cd vocl_demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - App will open at: http://localhost:8501

### Optional: LLM Correction (Groq API)

For phoneme-to-text correction, use Groq API (free, fast, cloud-compatible):

1. **Get your free API key** (2 minutes):
   - Go to: https://console.groq.com
   - Sign up with Google/GitHub (free, no credit card)
   - Click "API Keys" → "Create API Key"
   - Copy the key (starts with `gsk_...`)

2. **For local testing**, create `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```

3. **For Streamlit Cloud**, add the secret in app settings (see Deployment section)

**Note**: The app works without the API key - it will show raw phoneme sequences instead of corrected text. See `GROQ_SETUP.md` for detailed instructions.

## 📁 Project Structure

```
vocl_demo/
├── app.py                    # Main Streamlit application
├── components/               # UI components
│   ├── emg_visualizer.py    # EMG signal plotting
│   ├── phoneme_builder.py   # Interactive phoneme selector
│   ├── phoneme_display.py   # Phoneme sequence display
│   └── text_output.py       # Final text output
├── utils/                    # Utilities
│   ├── pipeline.py          # VOCL pipeline (for Working Demo)
│   └── llm_corrector.py     # LLM correction (cloud-compatible)
├── data/                     # Data files
│   ├── phoneme_library.json  # Phoneme definitions
│   └── phoneme_emg_library.npz  # Pre-generated EMG data
└── requirements.txt          # Python dependencies
```

## 🌐 Deployment to Streamlit Cloud

### Step 1: Prepare Repository

```bash
cd vocl_demo

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial VOCL Demo Platform"
```

### Step 2: Push to GitHub

1. Create a new repository on GitHub: https://github.com/new
   - Name: `vocl-demo`
   - Make it **Public**
   - Don't initialize with README (we already have one)

2. Add remote and push:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/vocl-demo.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repository: `vocl-demo`
5. **Main file path**: `app.py`
6. Click **"Deploy"**
7. Wait 3-5 minutes for deployment
8. Your app will be live at: `https://vocl-demo-YOUR_USERNAME.streamlit.app`

### Step 4: Add Groq API Key (Optional but Recommended)

1. Go to your deployed app dashboard: https://share.streamlit.io
2. Click on your `vocl-demo` app
3. Click **"⚙️ Settings"** (gear icon)
4. Click **"Secrets"** tab
5. Paste your Groq API key:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```
6. Click **"Save"**
7. App will restart automatically (takes ~1 minute)

Now LLM correction will work on your cloud deployment! 🎉

## ⚙️ Configuration

### Streamlit Config

Configuration is in `.streamlit/config.toml`:
- Theme colors
- Server settings
- Browser settings

### LLM Correction

The app uses Ollama for LLM correction, but gracefully falls back if unavailable:
- **Local**: Works if `ollama serve` is running
- **Cloud**: Shows raw phoneme sequences (Ollama not available on Streamlit Cloud)

## 🐛 Troubleshooting

### App won't start
- Check Python version: `python3 --version` (needs 3.9+)
- Install dependencies: `pip install -r requirements.txt`
- Check for port conflicts: `lsof -ti:8501`

### LLM correction not working
- Make sure Ollama is running: `ollama serve`
- Check model is pulled: `ollama list`
- App will show raw phonemes if LLM unavailable (this is normal)

### EMG plots not showing
- Check matplotlib is installed: `pip install matplotlib`
- Try refreshing the page

## 📝 Notes

- **No TensorFlow required** for Phoneme Builder (uses pre-generated data)
- **LLM is optional** - app works without it
- **All data is pre-generated** - no model inference needed
- **Cloud-ready** - designed for Streamlit Cloud deployment

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

Built for the Conrad Challenge - EMG-based speech restoration system.
