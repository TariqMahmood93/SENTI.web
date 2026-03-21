#!/usr/bin/env python3
"""
build.py — SENTI website builder
---------------------------------
Assembles TIDI_website_v0.html from modular section files.

USAGE:
    python3 build.py

HOW IT WORKS:
    1. Edit SECTIONS below to add/remove/reorder sections.
    2. For the 'screenshots' section, edit SCREENSHOTS to configure images.
    3. Run this script — it writes TIDI_website_v0.html ready to open in a browser.

NOTES:
    - Screenshot images are referenced by filename (not embedded).
    - Keep your image files in the same folder as build.py and TIDI_website_v0.html.
    - Open the HTML via a local server (python3 -m http.server) for images to load,
      OR just double-click it — modern browsers allow same-folder image references.
"""

import re
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────────

SECTIONS_DIR = Path(__file__).parent / "sections"
OUTPUT       = Path(__file__).parent / "TIDI_website_v0.html"

# ── Sections to include ──────────────────────────────────────────────────────────
# Comment out any line to exclude that section. Reorder to change page order.

SECTIONS = [
    "hero",
    "about",
    "how",
    "examples",
    "architecture",
    "screenshots",    # ← comment this out to hide the screenshots section
    "features",
   # "quickstart",
    "results",
   # "related",
    "citation",
    "contact",
    "demo",
]

# ── Screenshots configuration ─────────────────────────────────────────────────────
# Only used when "screenshots" is in SECTIONS.
# "file" = image filename that lives in the same folder as build.py.
# Comment out any entry to exclude that screenshot.

SCREENSHOTS = [
    {
        "file":        "null_inject.png",
        "step":        "01",
        "title":       "Inject Nulls",
        "description": "Start here — upload your CSV and choose a null injection rate and pattern (MCAR, MAR, or MNAR). The table preview highlights injected missing cells in red so you can verify the simulation before moving to imputation.",
        "tags":        ["Missing Data", "Simulation", "CSV Upload"],
    },
    {
        "file":        "imputation.png",
        "step":        "02",
        "title":       "Imputation",
        "description": "Select static or incremental mode, pick your transformer model, and run imputation. The output table highlights recovered values in green — each cell filled by majority vote from the k most semantically similar complete tuples. No training required.",
        "tags":        ["SBERT", "KNN", "Imputation"],
    },
    {
        "file":        "evaluation.png",
        "step":        "03",
        "title":       "Evaluation",
        "description": "After imputation, load the original complete dataset as ground truth. The evaluation panel reports accuracy, F1, precision, recall, and RMSE per column — giving you a clear picture of how well SENTI recovered the missing values.",
        "tags":        ["RMSE", "Accuracy", "Benchmarks"],
    },

]

# ── Helpers ───────────────────────────────────────────────────────────────────────

def build_screenshots_html(shots: list[dict], base_dir: Path) -> str:
    items = ""
    for i, s in enumerate(shots):
        img_path = base_dir / s["file"]
        if not img_path.exists():
            print(f"  ⚠  Not found (will show broken image): {s['file']}")
        else:
            print(f"  ✓  {s['file']}")

        # plain filename — browser resolves it relative to the HTML file
        src = s["file"]

        tags_html = "".join(f'<span class="ss-tag">{t}</span>' for t in s["tags"])
        side = "ss-item--left"  # caption left, image right for all items
        items += f"""
    <div class="ss-item {side}">
      <div class="ss-browser">
        <div class="ss-chrome"><span></span><span></span><span></span></div>
        <img src="{src}" alt="{s['title']} screenshot" loading="lazy"/>
      </div>
      <div class="ss-caption">
        <span class="ss-step">{s['step']}</span>
        <h3>{s['title']}</h3>
        <p>{s['description']}</p>
        <div class="ss-tags">{tags_html}</div>
      </div>
    </div>"""

    return f"""
<section id="screenshots" class="section">
  <div class="container">
    <div class="section-label">App Preview</div>
    <h2 class="section-title">See It in Action</h2>
    <p class="section-sub">Walk through the SENTI Streamlit interface — from injecting nulls to reading the final evaluation.</p>
    <div class="ss-list">{items}
    </div>
  </div>
</section>"""


def nav_link_html(sec_id: str, label: str, cta: bool) -> str:
    if not label:
        return ""
    cls = ' class="nav-cta"' if cta else ""
    return f'<li><a href="#{sec_id}"{cls}>{label}</a></li>'


# ── Main ──────────────────────────────────────────────────────────────────────────

def main():
    script_dir = Path(__file__).parent
    main_html  = (script_dir / "main.html").read_text(encoding="utf-8")

    sections_html  = ""
    nav_links_html = ""

    for name in SECTIONS:
        section_file = SECTIONS_DIR / f"section_{name}.html"

        if name == "screenshots":
            print("Building screenshots section...")
            sections_html  += "\n" + build_screenshots_html(SCREENSHOTS, script_dir)
            nav_links_html += nav_link_html("screenshots", "App Preview", False) + "\n          "
            continue

        if not section_file.exists():
            print(f"  ⚠  Section file not found, skipping: {section_file.name}")
            continue

        content = section_file.read_text(encoding="utf-8")

        # Parse nav link metadata from comment
        nav_match = re.search(r'<!-- NAV_LINK: id="([^"]*)" label="([^"]*)" cta="([^"]*)" -->', content)
        if nav_match:
            sec_id, label, cta_str = nav_match.groups()
            nav_links_html += nav_link_html(sec_id, label, cta_str.lower() == "true") + "\n          "

        # Strip marker comments before injecting into page
        content = re.sub(r'<!-- ═══ SECTION:.*?-->\n?', '', content)
        content = re.sub(r'<!-- ════.*?-->\n?', '', content)
        content = re.sub(r'<!-- NAV_LINK:.*?-->\n?', '', content)
        sections_html += "\n" + content.strip()

    output = main_html.replace("<!-- BUILD:SECTIONS -->", sections_html.strip())
    output = output.replace("<!-- nav links injected by build.py -->", nav_links_html.strip())

    OUTPUT.write_text(output, encoding="utf-8")
    print(f"\n✅  Built: {OUTPUT}  ({OUTPUT.stat().st_size // 1024} KB)")
    print(f"   Sections: {', '.join(SECTIONS)}")


if __name__ == "__main__":
    main()
