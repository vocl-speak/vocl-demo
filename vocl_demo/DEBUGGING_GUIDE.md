# Debugging Guide - Phoneme Builder Crashes

## Two Versions Available

### 1. Minimal Version (Guaranteed to Work)
**File**: `app_minimal.py`  
**URL**: http://localhost:8502  
**Features**:
- ✅ Shows phoneme grid
- ✅ User can select phonemes
- ✅ Shows phoneme sequence as text
- ❌ NO EMG plotting
- ❌ NO LLM calls
- ❌ NO TensorFlow
- **Cannot crash** - zero dependencies

**Use this to verify basic functionality works.**

### 2. Full Version (With Debugging)
**File**: `app.py`  
**URL**: http://localhost:8501  
**Features**:
- ✅ Full functionality
- ✅ Extensive logging added
- ✅ Error handling at each step

**Check terminal output when clicking "Build Word" to see which STEP crashes.**

## Debugging Steps

### Step 1: Test Minimal Version
1. Open http://localhost:8502
2. Select phonemes: `HH` → `EH` → `L` → `OW`
3. Click "Build Word"
4. **Expected**: Should show phoneme sequence "HH EH L OW" without crashing

### Step 2: Test Full Version with Logging
1. Open http://localhost:8501
2. Go to "Phoneme Builder"
3. Select phonemes: `HH` → `EH` → `L` → `OW`
4. Click "Build Word"
5. **Watch terminal output** - you'll see:
   ```
   ============================================================
   BUILD WORD CLICKED - Starting process...
   Selected phonemes: ['HH', 'EH', 'L', 'OW']
   ============================================================
   
   STEP A: Calling build_emg_sequence_from_library...
   STEP 1: Starting build_emg_sequence_from_library...
   STEP 2: Loading EMG library...
   STEP 2 SUCCESS: Loaded 44 phonemes from library
   STEP 3: Processing phonemes...
     STEP 3.1: Processing phoneme 'HH'...
     STEP 3.1 SUCCESS: Found 'HH' in library
     ...
   STEP 6 SUCCESS: Returning sequence 'HH EH L OW'...
   STEP A SUCCESS: Got emg_data=True, phoneme_seq='HH EH L OW'...
   STEP B: Storing in session state...
   STEP B SUCCESS: Session state updated
   ```

6. **If it crashes**, the last STEP shown tells you where it failed:
   - **STEP 2** = EMG library loading issue
   - **STEP 3.X** = Phoneme lookup issue
   - **STEP 4** = EMG data processing issue
   - **STEP A/B** = Session state or display issue

### Step 3: Check Logs
```bash
# View live logs
tail -f /tmp/streamlit_log.txt

# Or check terminal where Streamlit is running
```

## Common Crash Points

### 1. EMG Library Loading
**Symptom**: Crashes at STEP 2  
**Fix**: Check `vocl_demo/data/phoneme_emg_library.npz` exists

### 2. EMG Plotting
**Symptom**: Crashes after STEP B, when displaying EMG  
**Fix**: Comment out `plot_emg_signals()` call in app.py

### 3. LLM Correction
**Symptom**: Crashes when calling LLM  
**Fix**: Error handling already added, but check Ollama is running

### 4. TensorFlow Import
**Symptom**: Crashes immediately on app load  
**Fix**: Should not happen - we removed TensorFlow from phoneme builder

## Quick Fixes

### Disable EMG Plotting (if that's crashing)
In `app.py`, line ~286, comment out:
```python
# fig = plot_emg_signals(st.session_state['builder_emg_data'])
# st.pyplot(fig)
st.info("EMG plotting disabled for debugging")
```

### Disable LLM (if that's crashing)
In `app.py`, line ~302, comment out:
```python
# with st.spinner("Correcting phonemes with LLM..."):
#     pipeline = load_pipeline()
#     ...
st.info("LLM disabled for debugging")
display_final_text(phoneme_seq, success=False)
```

## Next Steps

1. **Test minimal version first** - verify basic flow works
2. **Test full version** - watch logs to see where it crashes
3. **Report which STEP crashes** - I'll fix that specific component
4. **Add features back one by one** - once basic version works

