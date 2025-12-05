# Claude's Available Tools & Installable Capabilities

## What I Already Have (Pre-Installed)

### Document Processing
| Tool | What It Does | Python Import |
|------|--------------|---------------|
| python-docx | Create/edit Word documents | `from docx import Document` |
| python-pptx | Create/edit PowerPoint | `from pptx import Presentation` |
| pdfplumber | Extract text/tables from PDF | `import pdfplumber` |
| camelot-py | Extract tables from PDF | `import camelot` |
| pypdf | PDF manipulation | `import pypdf` |
| pikepdf | Advanced PDF editing | `import pikepdf` |
| xlsxwriter | Create Excel files | `import xlsxwriter` |
| img2pdf | Convert images to PDF | `import img2pdf` |

### Image & Vision
| Tool | What It Does | Python Import |
|------|--------------|---------------|
| opencv | Computer vision | `import cv2` |
| pillow | Image manipulation | `from PIL import Image` |
| pytesseract | OCR (text from images) | `import pytesseract` |

### Web & Browser
| Tool | What It Does | Python Import |
|------|--------------|---------------|
| playwright | Browser automation | `from playwright.sync_api import sync_playwright` |
| requests | HTTP requests | `import requests` |
| beautifulsoup4 | HTML parsing | `from bs4 import BeautifulSoup` |
| httpx | Async HTTP | `import httpx` |

### Data Processing
| Tool | What It Does | Python Import |
|------|--------------|---------------|
| pandas | DataFrames | `import pandas as pd` |
| numpy | Numerical computing | `import numpy as np` |
| scipy | Scientific computing | `import scipy` |
| matplotlib | Plotting | `import matplotlib.pyplot as plt` |

### Video/Audio
| Tool | What It Does | Python Import |
|------|--------------|---------------|
| imageio-ffmpeg | Video processing | `import imageio_ffmpeg` |

---

## Just Installed This Session

### AI/LLM SDKs
| Tool | What It Does | Python Import |
|------|--------------|---------------|
| anthropic | Claude API client | `import anthropic` |
| openai | OpenAI API client | `import openai` |

### Content Extraction
| Tool | What It Does | Python Import |
|------|--------------|---------------|
| youtube-transcript-api | Get YouTube transcripts | `from youtube_transcript_api import YouTubeTranscriptApi` |
| yt-dlp | Download YouTube videos/audio | `import yt_dlp` |
| trafilatura | Extract article text from URLs | `import trafilatura` |
| newspaper3k | Article scraping | `from newspaper import Article` |
| feedparser | Parse RSS feeds | `import feedparser` |

### CLI Tools
| Tool | What It Does | Python Import |
|------|--------------|---------------|
| rich | Beautiful terminal output | `from rich import print` |
| typer | CLI app builder | `import typer` |

---

## What I Can Install On-Demand

### Data/ML
```bash
pip install --break-system-packages polars  # Fast DataFrames
pip install --break-system-packages scikit-learn  # ML
pip install --break-system-packages transformers  # Hugging Face models (large!)
```

### Web Scraping
```bash
pip install --break-system-packages scrapy  # Web crawler
pip install --break-system-packages parsel  # Selector library
```

### Audio Processing
```bash
pip install --break-system-packages pydub  # Audio manipulation
pip install --break-system-packages whisper  # Speech-to-text (large!)
```

### Database
```bash
pip install --break-system-packages sqlalchemy  # SQL toolkit
pip install --break-system-packages aiosqlite  # Async SQLite
```

---

## NPM Tools Available

| Tool | What It Does |
|------|--------------|
| mermaid-cli | Diagrams from text |
| pptxgenjs | PowerPoint generation |
| sharp | Image processing |
| playwright | Browser automation |
| marked | Markdown to HTML |
| typescript | TypeScript compiler |

---

## Network Restrictions

**Can Access:**
- pypi.org (package installation)
- api.anthropic.com (Anthropic API)
- github.com (source code)
- npmjs.org (npm packages)

**API Keys:**
- NOT available in my bash environment
- Must be provided by you or used through my built-in tools

---

## Practical Examples

### Extract text from any PDF
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

### Get YouTube transcript
```python
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript("VIDEO_ID")
full_text = " ".join([t['text'] for t in transcript])
```

### Extract article from URL
```python
import trafilatura

downloaded = trafilatura.fetch_url("https://example.com/article")
text = trafilatura.extract(downloaded)
```

### OCR an image
```python
import pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open("image.png"))
```

### Automate browser
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    content = page.content()
    browser.close()
```

---

## Building Custom Skills

I can create skills that package these capabilities:

```
/mnt/skills/user/your-skill/
├── SKILL.md           # Instructions
├── scripts/
│   ├── extract_pdf.py
│   ├── scrape_site.py
│   └── process_data.py
├── references/
│   └── api_docs.md
└── assets/
    └── templates/
```

### Example: YouTube Research Skill

```markdown
# SKILL.md
---
name: youtube-research
description: Extract and analyze YouTube video content. Use when user 
wants transcripts, summaries, or analysis of YouTube videos.
---

## Workflow
1. Extract video ID from URL
2. Fetch transcript using youtube_transcript_api
3. Process/analyze as needed
4. Return structured output

## Scripts
- scripts/get_transcript.py - Fetch and format transcript
- scripts/analyze_content.py - Topic extraction, summarization
```

---

## What Should I Build For You?

Based on your APX work, useful skills might include:

1. **Content Research Skill** - YouTube transcripts + article extraction + summarization
2. **Document Pipeline Skill** - PDF → structured data → docx/pptx output
3. **Competitive Analysis Skill** - Scrape + analyze competitor content
4. **Framework Tester Skill** - Apply APX frameworks to test problems, measure effectiveness

Want me to build any of these?
