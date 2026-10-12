"""
Generates an academic, print-ready HTML version of the Minor Project Report.
Features university cover-page styling, A4 page pagination, and clean typography.
"""

import os
import markdown
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
REPORT_MD = ROOT_DIR / "docs" / "PROJECT_REPORT.md"
REPORT_HTML = ROOT_DIR / "docs" / "PROJECT_REPORT.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minor Project Report | Aman Kumar Choudhary (23011004016)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #0f62fe;
      --text: #161616;
      --text-muted: #525252;
      --border: #d1d5db;
      --bg-code: #f3f4f6;
    }

    * { box-sizing: border-box; }

    body {
      font-family: 'Crimson Pro', Georgia, serif;
      font-size: 16pt;
      line-height: 1.6;
      color: var(--text);
      background-color: #f8fafc;
      margin: 0;
      padding: 40px 20px;
    }

    .report-container {
      max-width: 900px;
      margin: 0 auto;
      background: #ffffff;
      padding: 70px 80px;
      border: 1px solid #e2e8f0;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    }

    /* Print Specific Styling */
    @media print {
      body {
        background: transparent;
        padding: 0;
        font-size: 12pt;
      }
      .report-container {
        border: none;
        box-shadow: none;
        padding: 0;
        max-width: 100%;
      }
      .no-print {
        display: none !important;
      }
      h1, h2, h3 {
        page-break-after: avoid;
      }
      table, pre, blockquote {
        page-break-inside: avoid;
      }
      div[style*="page-break-after: always;"] {
        page-break-after: always !important;
      }
    }

    /* Floating Print Button */
    .print-bar {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 1000;
    }
    .print-btn {
      background: #0f62fe;
      color: white;
      border: none;
      padding: 12px 24px;
      font-family: 'Inter', sans-serif;
      font-size: 14px;
      font-weight: 600;
      border-radius: 30px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(15, 98, 254, 0.4);
      display: flex;
      align-items: center;
      gap: 8px;
      transition: transform 0.2s, background-color 0.2s;
    }
    .print-btn:hover {
      background: #0353e9;
      transform: translateY(-2px);
    }

    /* Typography */
    h1 {
      font-family: 'Inter', sans-serif;
      font-size: 24pt;
      font-weight: 700;
      color: #111827;
      text-align: center;
      line-height: 1.3;
      margin-top: 30px;
      margin-bottom: 20px;
    }

    h2 {
      font-family: 'Inter', sans-serif;
      font-size: 18pt;
      font-weight: 700;
      color: #1f2937;
      border-bottom: 2px solid #e5e7eb;
      padding-bottom: 8px;
      margin-top: 40px;
      margin-bottom: 16px;
    }

    h3 {
      font-family: 'Inter', sans-serif;
      font-size: 14pt;
      font-weight: 600;
      color: #374151;
      margin-top: 28px;
      margin-bottom: 12px;
    }

    p {
      text-align: justify;
      margin-bottom: 14px;
    }

    strong {
      font-weight: 700;
      color: #111827;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 24px 0;
      font-size: 12pt;
      font-family: 'Inter', sans-serif;
    }

    th, td {
      border: 1px solid #d1d5db;
      padding: 10px 14px;
      text-align: left;
    }

    th {
      background-color: #f3f4f6;
      font-weight: 600;
      color: #1f2937;
    }

    tr:nth-child(even) {
      background-color: #f9fafb;
    }

    /* Code Blocks */
    pre {
      background-color: var(--bg-code);
      border: 1px solid #e5e7eb;
      border-radius: 6px;
      padding: 16px;
      overflow-x: auto;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10.5pt;
      line-height: 1.5;
      margin: 20px 0;
    }

    code {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11pt;
      background-color: #f3f4f6;
      padding: 2px 6px;
      border-radius: 4px;
      color: #b91c1c;
    }

    pre code {
      background-color: transparent;
      padding: 0;
      color: #1f2937;
    }

    blockquote {
      border-left: 4px solid var(--primary);
      margin: 20px 0;
      padding: 10px 20px;
      background-color: #eff6ff;
      font-style: italic;
      color: #1e3a8a;
    }

    hr {
      border: none;
      border-top: 1px solid #e5e7eb;
      margin: 40px 0;
    }

    ul, ol {
      margin-bottom: 16px;
      padding-left: 28px;
    }

    li {
      margin-bottom: 6px;
    }
  </style>
</head>
<body>
  <div class="print-bar no-print">
    <button class="print-btn" onclick="window.print()">
      🖨️ Print to PDF / Paper
    </button>
  </div>

  <div class="report-container">
    {CONTENT}
  </div>
</body>
</html>
"""

def generate():
    if not REPORT_MD.exists():
        print(f"Error: {REPORT_MD} does not exist.")
        return

    with open(REPORT_MD, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert Markdown to HTML
    html_body = markdown.markdown(
        md_text,
        extensions=[
            "tables",
            "fenced_code",
            "toc",
            "attr_list",
            "sane_lists"
        ]
    )

    final_html = HTML_TEMPLATE.replace("{CONTENT}", html_body)

    with open(REPORT_HTML, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"HTML Report successfully generated at: {REPORT_HTML}")

if __name__ == "__main__":
    generate()
