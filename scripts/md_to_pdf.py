#!/usr/bin/env python3
"""Convert Markdown research report to beautifully formatted PDF.

Usage:
    python md_to_pdf.py input.md output.pdf --title "报告标题" [--author "作者"] [--subtitle "副标题"]
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import markdown
except ImportError:
    print("Error: 'markdown' package is required. Install with: pip install markdown", file=sys.stderr)
    sys.exit(1)

try:
    import weasyprint
except ImportError:
    print("Error: 'weasyprint' package is required. Install with: pip install weasyprint", file=sys.stderr)
    sys.exit(1)


def get_css():
    """Return the complete CSS stylesheet."""
    return """
/* ===== Page Setup ===== */
@page {
    size: A4;
    margin: 25mm 20mm 20mm 20mm;

    @top-center {
        content: string(page-header);
        font-size: 8pt;
        color: #999;
        font-family: "Noto Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Droid Sans Fallback", Helvetica, Arial, sans-serif;
    }

    @bottom-center {
        content: "第 " counter(page) " 页";
        font-size: 8pt;
        color: #999;
        font-family: "Noto Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Droid Sans Fallback", Helvetica, Arial, sans-serif;
    }
}

@page :first {
    @top-center { content: none; }
    @bottom-center { content: none; }
}

/* ===== Base Styles ===== */
body {
    font-family: "Noto Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Droid Sans Fallback", Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #2c3e50;
    text-align: justify;
    orphans: 3;
    widows: 3;
}

p {
    margin: 0 0 0.5em 0;
}

a {
    color: #2980b9;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* ===== Page Header String ===== */
.page-header-setter {
    string-set: page-header content(text);
    display: none;
}

/* ===== Cover Page ===== */
.cover-page {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    text-align: center;
}

.cover-title {
    font-size: 28pt;
    color: #1a5276;
    font-weight: bold;
    margin-bottom: 16px;
    line-height: 1.3;
}

.cover-subtitle {
    font-size: 14pt;
    color: #7f8c8d;
    margin-bottom: 30px;
}

.cover-divider {
    width: 60%;
    height: 2px;
    background: linear-gradient(to right, #1a5276, #2e86c1);
    border: none;
    margin: 20px auto;
}

.cover-author {
    font-size: 12pt;
    color: #2c3e50;
    margin-top: 20px;
}

.cover-date {
    font-size: 11pt;
    color: #7f8c8d;
    margin-top: 12px;
}

.cover-meta {
    font-size: 10pt;
    color: #7f8c8d;
    margin-top: 16px;
    line-height: 1.6;
}

/* ===== Headings ===== */
h1 {
    font-size: 20pt;
    color: #1a5276;
    border-bottom: 2px solid #1a5276;
    padding-bottom: 6px;
    margin-top: 1.5em;
    margin-bottom: 0.6em;
    page-break-after: avoid;
}

h2 {
    font-size: 16pt;
    color: #1e8449;
    margin-top: 1.3em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}

h3 {
    font-size: 13pt;
    color: #2e86c1;
    margin-top: 1.1em;
    margin-bottom: 0.4em;
    page-break-after: avoid;
}

h4 {
    font-size: 11.5pt;
    color: #5b2c6f;
    margin-top: 1em;
    margin-bottom: 0.3em;
    page-break-after: avoid;
}

h5, h6 {
    font-size: 10.5pt;
    color: #2c3e50;
    margin-top: 0.8em;
    margin-bottom: 0.3em;
    page-break-after: avoid;
}

/* ===== Blockquote ===== */
blockquote {
    border-left: 3pt solid #1a5276;
    background-color: #f8f9fa;
    padding: 12px 20px;
    margin: 0.8em 0;
    font-style: italic;
    color: #555;
}

blockquote p {
    margin: 0.3em 0;
}

/* ===== Tables ===== */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 9.5pt;
}

thead th {
    background-color: #1a5276;
    color: white;
    font-weight: bold;
    padding: 8px 12px;
    text-align: left;
    border: 1px solid #1a5276;
}

tbody td {
    padding: 8px 12px;
    border: 1px solid #ddd;
}

tbody tr:nth-child(even) {
    background-color: #f2f3f4;
}

/* ===== Code ===== */
code {
    font-family: "SF Mono", "Monaco", "Menlo", "Consolas", "Courier New", monospace;
    font-size: 9pt;
    background: #f4f4f4;
    padding: 1px 4px;
    border-radius: 3px;
}

pre {
    background: #f4f4f4;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 12px 16px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.5;
    margin: 0.8em 0;
}

pre code {
    background: none;
    padding: 0;
    border-radius: 0;
}

/* ===== Lists ===== */
ul, ol {
    margin: 0.5em 0;
    padding-left: 2em;
}

li {
    margin-bottom: 0.2em;
}

/* ===== Horizontal Rule ===== */
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 1.5em 0;
}

/* ===== Images ===== */
img {
    max-width: 100%;
    height: auto;
}

/* ===== Strong / Em ===== */
strong {
    font-weight: bold;
}

em {
    font-style: italic;
}
"""


def build_cover_page(title, subtitle, author, date_str, meta_info=None):
    """Build HTML for the cover page."""
    parts = []
    parts.append('<div class="cover-page">')
    parts.append(f'  <div class="cover-title">{_escape_html(title)}</div>')
    if subtitle:
        parts.append(f'  <div class="cover-subtitle">{_escape_html(subtitle)}</div>')
    parts.append('  <hr class="cover-divider">')
    if author:
        parts.append(f'  <div class="cover-author">{_escape_html(author)}</div>')
    parts.append(f'  <div class="cover-date">{_escape_html(date_str)}</div>')
    if meta_info:
        parts.append(f'  <div class="cover-meta">{meta_info}</div>')
    parts.append('</div>')
    return '\n'.join(parts)


def _escape_html(text):
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def parse_markdown(md_text):
    """Parse markdown and extract metadata.

    Returns:
        tuple: (html_body, extracted_title, meta_info)
            - html_body: HTML converted from markdown (first H1 removed)
            - extracted_title: title extracted from first H1 (or None)
            - meta_info: meta blockquote HTML after H1 (or None)
    """
    # Convert markdown to HTML
    extensions = ['tables', 'fenced_code', 'toc', 'smarty']
    html_body = markdown.markdown(md_text, extensions=extensions)

    extracted_title = None
    meta_info = None

    # Extract first H1 title
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_body, re.DOTALL)
    if h1_match:
        extracted_title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

        # Check for meta blockquote right after H1
        after_h1 = html_body[h1_match.end():].lstrip()
        bq_match = re.match(r'<blockquote>(.*?)</blockquote>', after_h1, re.DOTALL)
        if bq_match:
            bq_content = bq_match.group(1)
            # Check if it contains meta indicators
            if any(kw in bq_content for kw in ['研究时间', 'Generated', '生成时间', 'Date', '报告时间']):
                meta_info = bq_content
                # Remove the meta blockquote from body
                full_remove = h1_match.group(0) + html_body[h1_match.end():h1_match.end() + (bq_match.end() - 0 + len(after_h1) - len(after_h1.lstrip()))]
                # Simpler approach: remove H1 and the blockquote separately
                html_body = html_body[:h1_match.start()] + html_body[h1_match.end():]
                # Re-find and remove the meta blockquote
                bq_full_match = re.search(r'^\s*<blockquote>(.*?)</blockquote>', html_body.lstrip(), re.DOTALL)
                if bq_full_match and any(kw in bq_full_match.group(1) for kw in ['研究时间', 'Generated', '生成时间', 'Date', '报告时间']):
                    # Remove leading whitespace + blockquote
                    stripped = html_body.lstrip()
                    html_body = stripped[bq_full_match.end():]
            else:
                # Just remove H1, keep blockquote
                html_body = html_body[:h1_match.start()] + html_body[h1_match.end():]
        else:
            # Remove first H1 from body
            html_body = html_body[:h1_match.start()] + html_body[h1_match.end():]

    return html_body, extracted_title, meta_info


def build_html(md_text, title, subtitle, author):
    """Build complete HTML document."""
    html_body, extracted_title, meta_info = parse_markdown(md_text)

    # Use extracted title if --title not provided
    effective_title = title if title else (extracted_title or 'Research Report')
    effective_subtitle = subtitle

    date_str = datetime.now().strftime('%Y-%m-%d')

    # Build page header string for running header
    header_text = effective_title
    if effective_subtitle:
        header_text += f' | {effective_subtitle}'

    cover_html = build_cover_page(effective_title, effective_subtitle, author, date_str, meta_info)

    css = get_css()

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_escape_html(effective_title)}</title>
    <style>
{css}
    </style>
</head>
<body>
    <span class="page-header-setter">{_escape_html(header_text)}</span>
    {cover_html}
    <div class="content">
        {html_body}
    </div>
</body>
</html>"""

    return html


def convert_to_pdf(html_path, pdf_path):
    """Convert HTML to PDF using WeasyPrint."""
    try:
        doc = weasyprint.HTML(filename=str(html_path))
        doc.write_pdf(str(pdf_path))
        return True
    except Exception as e:
        print(f"Error converting to PDF: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown research report to beautifully formatted PDF.',
        epilog='Example: python md_to_pdf.py report.md report.pdf --title "AI趋势分析"'
    )
    parser.add_argument('input', help='Input Markdown file')
    parser.add_argument('output', help='Output PDF file')
    parser.add_argument('--title', help='Report title (overrides H1 from markdown)')
    parser.add_argument('--subtitle', default='Deep Research Report',
                        help='Report subtitle (default: "Deep Research Report")')
    parser.add_argument('--author', default='',
                        help='Author name (default: not shown)')
    args = parser.parse_args()

    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    html_path = output_path.with_suffix('.html')

    # Read markdown
    md_text = input_path.read_text(encoding='utf-8')
    if not md_text.strip():
        print("Error: Input file is empty.", file=sys.stderr)
        sys.exit(1)

    # Build HTML
    print(f"📄 Reading: {input_path}")
    html_content = build_html(md_text, args.title, args.subtitle, args.author)

    # Write intermediate HTML
    html_path.write_text(html_content, encoding='utf-8')
    print(f"🌐 HTML saved: {html_path}")

    # Convert to PDF
    print(f"📑 Converting to PDF...")
    success = convert_to_pdf(html_path, output_path)

    if success:
        pdf_size = output_path.stat().st_size
        size_str = f"{pdf_size / 1024:.1f} KB" if pdf_size < 1024 * 1024 else f"{pdf_size / (1024*1024):.1f} MB"
        print(f"✅ PDF saved: {output_path} ({size_str})")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
