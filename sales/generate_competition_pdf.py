#!/usr/bin/env python3.12
"""競合分析MD → PDF生成スクリプト（Chrome headless使用）"""

import pathlib, subprocess, tempfile, sys
from markdown_it import MarkdownIt

SALES_DIR = pathlib.Path("/Users/gon/Documents/AIMemory/crux/sales")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

FILES = [
    "XOP_競合分析",
    "FC_競合分析",
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif;
    font-size: 10pt;
    line-height: 1.8;
    color: #1a1a1a;
    background: #fff;
    padding: 0;
}

.page {
    max-width: 170mm;
    margin: 0 auto;
    padding: 8mm 0;
}

/* Cover header */
.cover {
    background: #0A0A0A;
    color: #F5F3EF;
    padding: 12mm 20mm;
    margin-bottom: 8mm;
}
.cover h1 {
    font-size: 18pt;
    color: #C9A84C;
    font-weight: 700;
    margin-bottom: 4mm;
    border: none;
}
.cover .meta {
    font-size: 9pt;
    color: #8C8C8C;
}

h1 {
    font-size: 14pt;
    font-weight: 700;
    color: #0A0A0A;
    border-left: 4px solid #C9A84C;
    padding-left: 6px;
    margin: 8mm 0 4mm 0;
}

h2 {
    font-size: 11pt;
    font-weight: 700;
    color: #C9A84C;
    margin: 6mm 0 3mm 0;
    padding-bottom: 1mm;
    border-bottom: 1px solid #e0d8c8;
}

h3 {
    font-size: 10pt;
    font-weight: 700;
    color: #1C2B3A;
    margin: 4mm 0 2mm 0;
}

h4 {
    font-size: 10pt;
    font-weight: 700;
    color: #8C8C8C;
    margin: 3mm 0 1mm 0;
}

p {
    margin-bottom: 3mm;
}

ul, ol {
    padding-left: 6mm;
    margin-bottom: 3mm;
}

li {
    margin-bottom: 1mm;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 4mm 0;
    font-size: 9pt;
}

thead tr {
    background: #0A0A0A;
    color: #F5F3EF;
}

thead th {
    padding: 3mm 4mm;
    text-align: left;
    font-weight: 700;
}

tbody tr:nth-child(even) {
    background: #FAFAF8;
}

tbody td {
    padding: 2.5mm 4mm;
    border-bottom: 0.5px solid #e8e0d0;
    vertical-align: top;
}

tbody tr:first-child td {
    border-top: 1px solid #C9A84C;
}

/* Blockquote for トーク素材 */
blockquote {
    border-left: 3px solid #C9A84C;
    background: #FAF8F4;
    padding: 4mm 6mm;
    margin: 4mm 0;
    color: #1C2B3A;
    font-style: normal;
}

blockquote p {
    margin-bottom: 1mm;
}

/* Code / preformatted (for matrix) */
pre {
    background: #F5F3EF;
    border: 1px solid #e0d8c8;
    padding: 4mm;
    font-family: 'Courier New', monospace;
    font-size: 8pt;
    white-space: pre;
    overflow: visible;
    margin: 4mm 0;
    line-height: 1.6;
    color: #1a1a1a;
}

/* HR */
hr {
    border: none;
    border-top: 1px solid #C9A84C;
    margin: 6mm 0;
}

/* Inline bold/em */
strong { font-weight: 700; color: #0A0A0A; }
em { font-style: normal; color: #1C2B3A; }

/* Note / small */
.note {
    font-size: 8.5pt;
    color: #8C8C8C;
}

@page {
    size: A4;
    margin: 18mm 20mm;
}

@media print {
    .cover { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    thead tr { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    tbody tr:nth-child(even) { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    blockquote { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    pre { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    h1 { page-break-after: avoid; }
    h2 { page-break-after: avoid; }
    h3 { page-break-after: avoid; }
    table { page-break-inside: avoid; }
}
"""

def md_to_html(md_text: str, title: str) -> str:
    md = MarkdownIt("commonmark")
    body = md.render(md_text)

    # Extract first h1 for cover
    lines = md_text.split("\n")
    doc_title = title
    doc_date = ""
    for line in lines:
        if line.startswith("# "):
            doc_title = line[2:].strip()
        if "作成日" in line or "最終更新" in line:
            doc_date = line.replace(">", "").replace("作成日：", "").replace("最終更新：", "").strip()

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{doc_title}</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="cover">
  <h1>{doc_title}</h1>
  <div class="meta">クラックス合同会社（CRUX G.K.）&nbsp;&nbsp;|&nbsp;&nbsp;{doc_date}&nbsp;&nbsp;|&nbsp;&nbsp;社外秘</div>
</div>
<div class="page">
{body}
</div>
</body>
</html>"""

def generate_pdf(name: str):
    md_path = SALES_DIR / f"{name}.md"
    pdf_path = SALES_DIR / f"{name}.pdf"
    html_path = SALES_DIR / f"{name}_tmp.html"

    md_text = md_path.read_text(encoding="utf-8")
    html = md_to_html(md_text, name)
    html_path.write_text(html, encoding="utf-8")

    cmd = [
        CHROME,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file://{html_path}",
    ]

    print(f"  Generating: {name}.pdf ...", end="", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    html_path.unlink(missing_ok=True)

    if pdf_path.exists() and pdf_path.stat().st_size > 1000:
        size_kb = pdf_path.stat().st_size / 1024
        print(f" OK ({size_kb:.0f} KB)")
        return True
    else:
        print(f" FAILED")
        if result.stderr:
            print(f"  stderr: {result.stderr[:300]}")
        return False

if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else FILES
    ok = 0
    for name in targets:
        if generate_pdf(name):
            ok += 1
    print(f"\n{ok}/{len(targets)} PDFs generated.")
    print(f"Output: {SALES_DIR}")
