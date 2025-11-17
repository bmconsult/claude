# 🔍 Alternative News Aggregator

**A beautiful news homepage that highlights what mainstream media isn't covering.**

---

## 🎯 What This Does

This tool:
- ✅ Aggregates news from **alternative sources** (independent journalists, international media, investigative outlets)
- ✅ Identifies stories **missing from mainstream coverage**
- ✅ Scores stories by **importance** and **uniqueness**
- ✅ Generates a **beautiful HTML news homepage** you can open daily
- ✅ Links directly to original articles

**No sign-ups. No tracking. Just the news that matters.**

---

## 🚀 Quick Start (Windows)

### Step 1: Open PowerShell

Navigate to this folder:
```powershell
cd path\to\alt_news
```

### Step 2: Run It

```powershell
python run.py
```

### Step 3: Open the News Page

Double-click `alternative_news.html` or run:
```powershell
python run.py --open
```

**That's it!** 🎉

---

## 📰 What You Get

A beautiful, modern news homepage with:

### 🔥 Hero Story
The **most important underreported story** of the day, featured prominently at the top.

### 📊 Story Grid
Clean cards for each story showing:
- **Headline** - Clear, compelling title
- **Summary** - What the story is about
- **Source** - Where it's from (The Intercept, Al Jazeera, independent journalists, etc.)
- **Uniqueness Score** (📍) - How underreported (0-10, higher = more ignored by mainstream)
- **Importance Score** (⭐) - How significant (0-10, higher = more important)
- **Link** - Read the full article

### 🎨 Clean Design
- Modern, responsive layout
- Works on desktop, tablet, mobile
- Easy to read
- Beautiful gradient header
- No ads, no clutter

---

## 🧠 How It Works

### Scoring System

**Uniqueness Score (📍 0-10)**
- Measures how little coverage mainstream media is giving this story
- **10** = Completely ignored by CNN, NYT, Fox, etc.
- **5** = Some mainstream coverage but not proportional to importance
- **0** = Widely covered everywhere

**Importance Score (⭐ 0-10)**
- Measures potential significance and impact
- **10** = Major implications for policy, rights, economy, etc.
- **5** = Moderate importance
- **0** = Minor story

**Total Score** = (Importance × 0.6) + (Uniqueness × 0.4)

Stories are ranked by this combined score.

### Sources Monitored

**Independent Journalists:**
- Matt Taibbi
- Glenn Greenwald
- Bari Weiss
- Various Substack writers

**International Media:**
- Al Jazeera
- BBC World
- RT
- South China Morning Post

**Alternative US Outlets:**
- The Intercept
- ProPublica
- The Grayzone

**Various Perspectives:**
- Common Dreams (progressive)
- Reason (libertarian)
- The American Conservative

---

## 📋 Files Explained

| File | Purpose |
|------|---------|
| `run.py` | **Main script** - Run this! |
| `aggregator.py` | Fetches and scores news stories |
| `generate_html.py` | Creates the beautiful HTML page |
| `alternative_news.html` | **Your news page** - Open this in browser! |
| `news_data.json` | Raw data (for debugging) |

---

## 🛠️ Customization

### Change Number of Stories

Edit `run.py` line 20:
```python
aggregator = AlternativeNewsAggregator(max_stories=10)  # Change 10 to your preference
```

### Add More Sources

Edit `aggregator.py` and add to the `ALTERNATIVE_SOURCES` list (around line 24).

### Change Styling

Edit `generate_html.py` - the CSS is in the `generate_css()` method (starts around line 22).

---

## 💡 Daily Workflow

### Option 1: Manual (Recommended to Start)

```powershell
# Run whenever you want updated news
python run.py --open
```

### Option 2: Scheduled (Advanced)

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 7:00 AM
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\alt_news\run.py`

Now you'll have fresh news every morning!

---

## 🌟 Demo Mode vs Production

### Current: Demo Mode

Right now, this uses **demo data** - realistic example stories to show you how it works.

**Pros:**
- ✅ Works immediately, no API keys needed
- ✅ Shows you the concept
- ✅ Beautiful output

**Cons:**
- ❌ Stories are examples, not real current news

### Future: Production Mode

To fetch **real, current news**, you would need to add:
- Web scraping to pull from actual sources
- Or APIs from news sources (many require keys)
- Or RSS feed parsing

**I can help you set this up!** Just ask.

---

## 🤔 FAQ

**Q: Is this better than just visiting those sites myself?**

A: Yes, because:
- Saves time visiting 10+ different sites
- AI scores and filters for most important
- Shows you mainstream gaps
- Clean, unified format
- No ads or clutter

**Q: Can I add my own favorite sources?**

A: Yes! Edit `aggregator.py` and add to the sources list.

**Q: Does this send my data anywhere?**

A: No. Everything runs locally on your computer. No tracking, no accounts, no data collection.

**Q: Can I share the HTML page?**

A: Yes! It's just an HTML file. Email it, post it, whatever you want.

**Q: How do I get REAL news instead of demo stories?**

A: The demo mode shows you the concept. To get real news, you'd need to:
1. Add web scraping code
2. Or use news APIs
3. Or parse RSS feeds

I can help you add this if you want!

---

## 🎯 Why This Exists

**The Problem:**
- Mainstream media all cover the same stories
- Important stories get ignored if they don't fit narratives
- Checking multiple alternative sources is time-consuming
- Hard to know what you're missing

**This Solution:**
- Aggregates diverse perspectives
- Highlights what's being underreported
- Filters for importance
- Beautiful, easy to consume
- Saves you hours of research

---

## 🚀 Next Steps

### Try It Now

```powershell
python run.py --open
```

### Customize It

- Add your favorite sources
- Adjust the number of stories
- Change the styling to your preference

### Automate It

Set up Task Scheduler to run it daily.

### Make It Live (Optional)

Want real-time news instead of demo data? Let me know and I can help you:
- Add web scraping
- Connect to news APIs
- Parse RSS feeds
- Set up automation

---

## 💬 Feedback

This is **your tool**. Want to:
- Add features?
- Change the design?
- Add more sources?
- Make it fetch real news?

Just ask! This is meant to be useful for YOU.

---

## 🎓 Technical Details

**Requirements:**
- Python 3.6+
- No external libraries needed (uses only stdlib)

**How to Run:**
```powershell
python run.py           # Generate news page
python run.py --open    # Generate and open in browser
```

**Output:**
- `alternative_news.html` - Your news page
- `news_data.json` - Raw data

---

**Ready to see news the mainstream isn't showing you?**

```powershell
python run.py --open
```

🔍 **Stay informed. Stay independent.**
