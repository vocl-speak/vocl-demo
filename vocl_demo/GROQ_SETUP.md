# Groq API Setup Instructions

## 🚀 Get Your Free API Key (2 minutes)

### Step 1: Sign Up
1. Go to: **https://console.groq.com**
2. Click **"Sign Up"** or **"Get Started"**
3. Sign up with Google or GitHub (free, no credit card required)
4. Verify your email if needed

### Step 2: Create API Key
1. Once logged in, click **"API Keys"** in the sidebar
2. Click **"Create API Key"** button
3. Give it a name (e.g., "VOCL Demo")
4. Click **"Submit"**
5. **Copy the key immediately** (starts with `gsk_...`)
   - ⚠️ You won't be able to see it again!

### Step 3: Add to Local Environment

For **local testing**, create a secrets file:

1. Create file: `.streamlit/secrets.toml` (in `vocl_demo/` directory)
2. Add your key:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
3. Save the file
4. Restart Streamlit app: `streamlit run app.py`

**Note**: This file is gitignored - your key won't be committed to GitHub.

### Step 4: Add to Streamlit Cloud

For **cloud deployment**, add the secret in Streamlit Cloud:

1. Go to: **https://share.streamlit.io**
2. Find your deployed `vocl-demo` app
3. Click **"⚙️ Settings"** (gear icon in top right)
4. Click **"Secrets"** tab
5. Paste your API key:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
6. Click **"Save"**
7. App will automatically restart (takes ~1 minute)

## ✅ Test It Works

### Local Testing
1. Make sure `.streamlit/secrets.toml` has your API key
2. Run: `streamlit run app.py`
3. Go to "Phoneme Builder"
4. Select: `HH` → `EH` → `L` → `OW`
5. Click "Build Word"
6. **Expected**: Should show "hello" (not "HH EH L OW")

### Cloud Testing
1. Make sure you added the secret in Streamlit Cloud
2. Wait for app to restart
3. Go to "Phoneme Builder"
4. Select: `HH` → `EH` → `L` → `OW`
5. Click "Build Word"
6. **Expected**: Should show "hello" (not "HH EH L OW")

## 📊 Free Tier Limits

- **14,400 requests/day** (plenty for demos!)
- **300+ tokens/second** (very fast)
- **No credit card required**
- **No expiration** (as long as you use it)

## 🐛 Troubleshooting

### "LLM correction unavailable"
- **Check**: API key is set correctly
- **Check**: Key starts with `gsk_`
- **Check**: No extra spaces or quotes
- **Check**: File is `.streamlit/secrets.toml` (not `secrets.txt`)

### "Groq library not installed"
- Run: `pip install groq`
- Or: `pip install -r requirements.txt`

### Still not working?
1. Check terminal/console for error messages
2. Verify API key is valid at https://console.groq.com
3. Try creating a new API key
4. Make sure you're using the latest version of the app

## 🔒 Security Notes

- ✅ `.streamlit/secrets.toml` is gitignored (won't be committed)
- ✅ Streamlit Cloud secrets are encrypted
- ✅ API key is only used for LLM requests
- ⚠️ Don't share your API key publicly
- ⚠️ Don't commit secrets.toml to GitHub

## 📚 More Info

- Groq Console: https://console.groq.com
- Groq Docs: https://console.groq.com/docs
- Streamlit Secrets: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management

---

**That's it!** Your LLM correction will now work both locally and on Streamlit Cloud. 🎉

