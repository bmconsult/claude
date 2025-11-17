# 🪟 Windows Quick Start Guide

## ⚡ 60-Second Setup

### 1. Check if Python is Installed

Open PowerShell and type:
```powershell
python --version
```

**See a version number?** ✅ You're good! Skip to step 3.

**Error?** ❌ Go to step 2.

### 2. Install Python (if needed)

1. Go to: https://www.python.org/downloads/
2. Click "Download Python 3.x"
3. Run the installer
4. **IMPORTANT:** Check "Add Python to PATH" ✅
5. Click Install
6. Restart PowerShell

### 3. Navigate to the Folder

In PowerShell:
```powershell
cd Downloads\claude-claude-explore-api-capabilities-019mgsLKKAPjYvWic7XDv4vR\claude-claude-explore-api-capabilities-019mgsLKKAPjYvWic7XDv4vR\alt_news
```

*Adjust the path to wherever you extracted the files.*

### 4. Run It!

```powershell
python run.py
```

You'll see:
```
======================================================================
  🔍 ALTERNATIVE NEWS AGGREGATOR
  What Mainstream Media Isn't Covering
======================================================================
...
✅ SUCCESS!
```

### 5. Open Your News Page

Double-click `alternative_news.html`

**Or** run:
```powershell
python run.py --open
```

---

## 🎉 That's It!

You now have a beautiful news homepage showing stories mainstream media isn't covering.

---

## 📅 Daily Use

### Every Morning:

```powershell
# Open PowerShell in the alt_news folder
python run.py --open
```

Get your daily dose of alternative news in seconds!

---

## 🔧 Troubleshooting

### "python is not recognized..."

**Problem:** Python not in PATH

**Fix:**
1. Reinstall Python
2. Make sure "Add Python to PATH" is checked ✅
3. Restart PowerShell

### "No module named..."

**Problem:** Usually a typo in the command

**Fix:** Make sure you're in the right folder:
```powershell
cd path\to\alt_news
dir  # Should show run.py, aggregator.py, etc.
```

### HTML looks broken

**Problem:** Browser cache or file permissions

**Fix:**
1. Right-click `alternative_news.html` → Open with → Chrome/Firefox
2. Press Ctrl+Shift+R to hard refresh
3. Or delete the file and regenerate: `python run.py`

---

## 💡 Pro Tips

### Tip 1: Create a Shortcut

1. Create a `.bat` file called `daily_news.bat`:
   ```batch
   @echo off
   cd C:\path\to\alt_news
   python run.py --open
   pause
   ```

2. Double-click it every morning!

### Tip 2: Pin to Start Menu

1. Right-click `daily_news.bat`
2. Send to → Desktop (create shortcut)
3. Drag shortcut to Start Menu

### Tip 3: Automate It

**Windows Task Scheduler:**
1. Press Windows key, search "Task Scheduler"
2. Create Basic Task
3. Name: "Daily Alternative News"
4. Trigger: Daily at 7:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `C:\full\path\to\alt_news\run.py --open`
6. Finish

Now you get fresh news every morning automatically!

---

## 🎯 What to Expect

### First Run (Demo Mode)

You'll see **10 example stories** that demonstrate:
- ✅ What the page looks like
- ✅ How scoring works
- ✅ The layout and design
- ✅ How to read and navigate

**These are realistic examples, not real current news.**

### Real News (Coming Soon)

To get actual current news, you'd need to add:
- Web scraping from your favorite sources
- Or news API connections
- Or RSS feed parsing

**Want help setting this up?** Just ask!

---

## 📱 Mobile Access

The HTML page is **responsive** and works great on phones!

**To use on mobile:**
1. Generate the HTML on your PC: `python run.py`
2. Email `alternative_news.html` to yourself
3. Open on your phone
4. Bookmark it!

Or sync via:
- OneDrive
- Google Drive
- Dropbox

---

## 🎨 Customization

### Change Colors

Edit `generate_html.py`:
- Line 27: Header color
- Line 175: Link color
- Play with the gradient!

### More/Fewer Stories

Edit `run.py`, line 20:
```python
max_stories=10  # Change to 5, 15, 20, etc.
```

### Add Sources

Edit `aggregator.py`, add to the sources list around line 24.

---

## ❓ Questions?

**"Is this safe?"**
Yes! Everything runs locally on your PC. No data sent anywhere.

**"Do I need to be online?"**
Yes, to fetch news. But once generated, the HTML works offline.

**"Can I customize it?"**
Absolutely! It's your tool. Change whatever you want.

**"Can I share my news page?"**
Yes! It's just an HTML file. Email it, post it, whatever.

**"Is this better than reading those sites directly?"**
Saves time, shows you what's important, no ads, unified format!

---

## 🚀 Ready?

```powershell
python run.py --open
```

**See what mainstream media isn't telling you!** 🔍
