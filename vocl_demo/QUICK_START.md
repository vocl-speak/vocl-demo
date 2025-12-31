# VOCL Demo - Quick Start (Pre-generated Version)

## ✅ FAST PATH - No TensorFlow Required!

This version uses pre-generated demo data, so it works immediately without TensorFlow crashes.

## Run the App

```bash
cd /Users/idhantranjan/Downloads/ConradML/neurotechML
streamlit run vocl_demo/app_pregenerated.py
```

The app will:
- ✅ Load instantly (no model startup)
- ✅ Display all 5 phrases perfectly
- ✅ Show EMG signals, phonemes, and corrected text
- ✅ Zero crashes, 100% reliable

## What's Included

- **5 Pre-generated Phrases:**
  - Hello
  - Help me
  - I love you
  - Thank you
  - How are you

- **Full 3-Column Display:**
  - EMG signal plots (4 channels)
  - Phoneme sequences with confidences
  - LLM-corrected text output

## To Generate New Data (Optional)

If you want to regenerate the demo data with real model outputs:

1. **Use a working Python environment** (where TensorFlow doesn't crash)
2. Run:
   ```bash
   python3 generate_demo_data.py
   ```
3. This creates `vocl_demo/demo_data/demo_phrases.json`

## Files

- `app_pregenerated.py` - Main app (no TensorFlow)
- `demo_data/demo_phrases.json` - Pre-computed results
- `generate_demo_data.py` - Data generator (requires working TensorFlow)

## Status

✅ **Ready for demo!** All 5 phrases work perfectly.

