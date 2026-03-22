# SENTI — Semantic-Aware Data Imputation

Marketing and documentation website for **SENTI**, a zero-shot data imputation framework using sentence transformers and semantic similarity to recover missing values in relational datasets.

Developed at [DIMES, University of Calabria](https://dimes.unical.it).
Published in *Information Fusion*, 2026.

---

## Project Structure

```
SENTI.web/
├── build.py            # Build script — assembles index.html from sections
├── main.html           # Base HTML template (CSS, JS, nav shell)
├── index.html          # Generated output — open this in a browser
├── sections/           # Modular HTML section files
│   ├── section_hero.html
│   ├── section_about.html
│   ├── section_how.html
│   ├── section_examples.html
│   ├── section_architecture.html
│   ├── section_features.html
│   ├── section_results.html
│   ├── section_citation.html
│   ├── section_contact.html
│   └── section_demo.html
├── null_inject.png     # App screenshot — step 01
├── imputation.png      # App screenshot — step 02
└── evaluation.png      # App screenshot — step 03
```

---

## Building the Site

**Requirements:** Python 3.8+ (standard library only, no external dependencies)

```bash
python3 build.py
```

This assembles `index.html` from `main.html` and all enabled section files.

### Adding or Removing Sections

Edit the `SECTIONS` list in `build.py`:

```python
SECTIONS = [
    "hero",
    "about",
    # "quickstart",   # comment out to hide
    "results",
    "contact",
]
```

### Previewing Locally

Open `index.html` directly in a browser, or serve it via a local server for images to load correctly:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

---

## Live App

[senti-data-imputation.streamlit.app](https://senti-data-imputation.streamlit.app/)

---

## Research Team

- **Prof. Sergio Greco** — Group Lead, DIMES University of Calabria
- **Tariq Mahmood** — Postdoc Fellow
- **Gianvincenzo Alfano** — Assistant Professor
- **Lucio La Cava** — Assistant Professor
- **Irina Trubitsyna** — Associate Professor
