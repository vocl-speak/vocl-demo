# Streamlit Cloud Deployment Guide

## ✅ Pre-Deployment Checklist

Before deploying, verify:

- [x] `requirements.txt` has all dependencies
- [x] `.streamlit/config.toml` exists
- [x] `.gitignore` excludes large files
- [x] All data files in `vocl_demo/data/` (phoneme_emg_library.npz is 56KB - OK)
- [x] LLM correction has graceful fallback
- [x] No hardcoded local paths
- [x] `app.py` is the main file

## 🚀 Deployment Steps

### Step 1: Prepare Git Repository

```bash
# Navigate to vocl_demo directory
cd ~/Downloads/ConradML/neurotechML/vocl_demo

# Initialize git (if not already done)
git init

# Add all files
git add .

# Check what will be committed (verify no large files)
git status

# Commit
git commit -m "Initial VOCL Demo Platform - Ready for Streamlit Cloud"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `vocl-demo`
3. Description: "VOCL - Voice Output Communication Link Demo Platform"
4. Make it **Public** (required for free Streamlit Cloud)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

### Step 3: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/vocl-demo.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with your **GitHub account**
3. Click **"New app"** button
4. Fill in the form:
   - **Repository**: Select `vocl-demo`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: (auto-generated) `vocl-demo-YOUR_USERNAME`
5. Click **"Deploy"**
6. Wait 3-5 minutes for deployment
7. Your app will be live at: `https://vocl-demo-YOUR_USERNAME.streamlit.app`

## 🔍 Post-Deployment Verification

After deployment, test:

1. **App loads**: Should see VOCL Demo Platform header
2. **Working Demo**: Click "Process Phrase" - should show EMG, phonemes, text
3. **Phoneme Builder**: 
   - Select phonemes: `HH` → `EH` → `L` → `OW`
   - Click "Build Word"
   - Should show results (LLM will show fallback message - this is normal)
4. **No crashes**: App should work smoothly

## ⚠️ Expected Behavior on Cloud

### What Works:
- ✅ All UI components
- ✅ EMG visualization
- ✅ Phoneme selection and building
- ✅ Pre-generated data loading
- ✅ All features except LLM correction

### What Won't Work:
- ❌ LLM correction (Ollama not available on Streamlit Cloud)
  - **This is expected** - app will show: "ℹ️ LLM correction unavailable - showing raw phoneme sequence"
  - This is a graceful fallback, not an error

## 🐛 Troubleshooting

### Deployment Fails

**Error: "Module not found"**
- Check `requirements.txt` has all dependencies
- Verify versions are compatible

**Error: "File not found"**
- Check `phoneme_emg_library.npz` is in `data/` folder
- Verify file paths are relative (not absolute)

**Error: "Port already in use"**
- This shouldn't happen on Streamlit Cloud
- If it does, contact Streamlit support

### App Deploys But Doesn't Work

**Check logs:**
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View "Logs" tab
4. Look for error messages

**Common issues:**
- Missing data file: Check `data/phoneme_emg_library.npz` is committed
- Import errors: Check all imports in `app.py`
- Path issues: All paths should be relative to `vocl_demo/`

## 📝 Updating the App

To update after deployment:

```bash
# Make changes to files
# ...

# Commit changes
git add .
git commit -m "Update: [describe changes]"

# Push to GitHub
git push origin main

# Streamlit Cloud will auto-deploy (takes 1-2 minutes)
```

## 🔗 Useful Links

- Streamlit Cloud: https://share.streamlit.io
- Streamlit Docs: https://docs.streamlit.io
- GitHub: https://github.com

## 📧 Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Test locally first: `streamlit run app.py`
3. Verify all files are committed to GitHub
4. Check `.gitignore` isn't excluding needed files

---

**Ready to deploy!** Follow the steps above and your app will be live in ~5 minutes.

