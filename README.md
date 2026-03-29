# 🚀 SitemapXtractor

A powerful Python CLI tool to download, decompress, and extract structured data from `.xml.gz` sitemap files.

---

## 🔥 Features

* ✅ Download sitemap directly from URL
* ✅ Supports `.xml.gz` compressed files
* ✅ Extracts:

  * URLs (loc)
  * lastmod
  * priority
  * changefreq
  * alternate links (hreflang)
* ✅ Progress tracking (download + parsing)
* ✅ Works with large sitemaps (thousands of URLs)
* ✅ Save output to file

---

## 📦 Installation

```bash
git clone https://github.com/your-username/sitemapxtractor.git
cd sitemapxtractor
pip install -r requirements.txt
```

 

1.** **Install Python**** (if not installed):

   - Download from: https://www.python.org/downloads/

   - Run installer (check "Add Python to PATH")

 

2.** **Install required library****:

   ```bash

   pip install requests

   ```

  

**## Requirements**

 

- Python 3.x or higher

- requests library

 
  

---

## ▶️ Usage

### 🔹 From URL

```bash
python extract.py "https://example.com/sitemap.xml.gz"
```

### 🔹 From Local File

```bash
python extract.py sitemap.xml.gz
```

### 🔹 Save Output

```bash
python extract.py sitemap.xml.gz -o output.txt
```

---

## 📊 Example Output

```
loc: https://example.com/page1
lastmod: 2024-01-01
priority: 0.8
changefreq: daily
```

---

## ⚙️ Tech Stack

* Python
* requests
* gzip
* xml.etree.ElementTree

---

## 🚧 Use Cases

* SEO analysis
* Web scraping pipelines
* Search engine indexing
* Data extraction for databases (MongoDB, MeiliSearch)

---

## 👨‍💻 Author

Raj_Patil
