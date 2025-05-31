# DAT Hebrew Transpiler

A desktop application built with Tkinter and SentenceTransformers that calculates the Divergent Association Task (DAT) score for Hebrew word sets using multilingual or Hebrew-compatible language models.

This tool is intended for researchers, educators, or linguists working with creativity metrics in Hebrew.

---

## Features

- Load `.xlsx` files containing Hebrew word sets (one row = one set of 10 words)
- Compute semantic distance between words using pretrained Hugging Face models
- Supports multiple multilingual and Hebrew-specific models
- Automatically adds a `DAT_score` column to the output
- Detects cached models and logs download events
- Simple, interactive Tkinter-based user interface with real-time logging

---

## Technologies Used

- Python 3.11+
- tkinter (GUI)
- pandas (Excel I/O)
- sentence-transformers (embedding and similarity)
- huggingface-hub (model download and cache management)

---

## Installation

```bash
git clone https://github.com/your-username/dat-hebrew-transpiler.git
cd dat-hebrew-transpiler
python -m venv .venv
.venv\Scripts\activate  # On Windows
python -m pip install -r requirements.txt
python main.py
```
