#!/usr/bin/env python3
"""Convert all .md files to .html with proper styling for GitHub Pages."""

import markdown
import os
import re
import shutil

DOCS = "docs"
os.makedirs(DOCS, exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — History Study</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<nav class="top-nav">
  <a href="index.html">🏠 Home</a>
  <span class="nav-sep">|</span>
  <a href="review_guide.html">Topic 5 Guide</a>
  <a href="key_concepts.html">Key Concepts</a>
  <a href="mock_exam.html">Mock Exam v1</a>
  <a href="mock_exam_v2.html">Mock Exam v2</a>
  <a href="depth_index.html">Depth Index</a>
  <span class="nav-group-title">Skills</span>
  <a href="skills_source_analysis.html">Source</a>
  <a href="skills_causality.html">Causality</a>
  <a href="skills_comparison.html">Compare</a>
  <a href="skills_evaluation.html">Evaluate</a>
</nav>
<main class="content">
{body}
</main>
<footer class="site-footer">
  <p>History Study Materials · <a href="https://github.com/gzxmren/western-history-review">GitHub</a></p>
</footer>
</body>
</html>"""

EXTENSIONS = [
    'markdown.extensions.tables',
    'markdown.extensions.fenced_code',
    'markdown.extensions.codehilite',
    'markdown.extensions.toc',
    'markdown.extensions.nl2br',
]

# Mapping: source filename (basename without .md) → output slug
SLUG_MAP = {
    # Western History — Topic 5
    'diagnostic_report': 'diagnostic_report',
    'review_guide': 'review_guide',
    'key_concepts_bilingual': 'key_concepts',
    'topic8_review_guide': 'topic8_review_guide',
    '认知深度索引图_Western': 'depth_index',
    '技能框架_史料分析_Western': 'skills_source_analysis',
    '技能框架_因果链分析_Western': 'skills_causality',
    '技能框架_对比分析_Western': 'skills_comparison',
    '技能框架_评价分析_Western': 'skills_evaluation',
    # Chinese History
    '認知深度索引圖': 'depth_index_cn',
    '技能框架_史料分析': 'skills_source_analysis_cn',
    '技能框架_因果鏈分析': 'skills_causality_cn',
    '技能框架_對比分析': 'skills_comparison_cn',
    '技能框架_評價分析': 'skills_evaluation_cn',
    'agent_handoff_deliverable': 'agent_handoff_deliverable',
    # Geography
    'agent_handoff_history_methodology': 'agent_handoff_history_methodology',
}

# Likewise for titles
TITLE_MAP = {
    'diagnostic_report': 'Diagnostic Report — Western History Topic 5',
    'review_guide': 'Topic 5 Review Guide — The Rise of Modern Europe',
    'key_concepts_bilingual': 'Key Concepts (Bilingual) — Topic 5',
    'topic8_review_guide': 'Topic 8 Review Guide — Growth of Hong Kong',
    '认知深度索引图_Western': 'Cognitive Depth Index — Western History',
    '技能框架_史料分析_Western': 'Source Analysis Framework (S-T-A-R) — Western History',
    '技能框架_因果链分析_Western': 'Causality Chain Framework — Western History',
    '技能框架_对比分析_Western': 'Comparative Analysis Framework — Western History',
    '技能框架_评价分析_Western': 'Evaluation Framework (P-E-B-C) — Western History',
    '認知深度索引圖': '认知深度索引图 — 中国历史',
    '技能框架_史料分析': '史料分析框架 (S-T-A-R) — 中国历史',
    '技能框架_因果鏈分析': '因果链分析框架 — 中国历史',
    '技能框架_對比分析': '对比分析框架 — 中国历史',
    '技能框架_評價分析': '评价分析框架 (P-E-B-C) — 中国历史',
    'agent_handoff_deliverable': '中国历史 — Agent 交接文档',
    'agent_handoff_history_methodology': '地理科 — 实战复盘方法论',
}

def get_slug(basename):
    """Return the ASCII slug for a filename (without .md)."""
    return SLUG_MAP.get(basename, basename)

def get_title(basename):
    """Return the display title for a filename (without .md)."""
    return TITLE_MAP.get(basename, basename)

def convert_file(src_path):
    """Convert a single .md file to .html in the docs/ folder."""
    base = os.path.basename(src_path)
    basename_no_ext = os.path.splitext(base)[0]
    slug = get_slug(basename_no_ext)

    with open(src_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    html_body = markdown.markdown(md_text, extensions=EXTENSIONS)

    title = get_title(basename_no_ext)
    full_html = TEMPLATE.format(title=title, body=html_body)

    out_name = slug + '.html'
    out_path = os.path.join(DOCS, out_name)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"  ✓ {base} → docs/{out_name}")
    return out_name

# Collect all .md files from root + subdirs (no .git, no docs)
md_files = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or '/docs' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            md_files.append(os.path.join(root, f))

print(f"Found {len(md_files)} markdown files\n")

# Convert each
html_files = []
for md_path in sorted(md_files):
    html_name = convert_file(md_path)
    html_files.append(html_name)

# Copy existing HTML files into docs/ (only if not already there from this build)
print("\nCopying existing HTML files...")
for root, dirs, files in os.walk('.'):
    if '.git' in root or root.startswith('./docs'):
        continue
    for f in files:
        if f.endswith('.html') and f not in ['index.html']:
            src = os.path.join(root, f)
            dst = os.path.join(DOCS, f)
            shutil.copy2(src, dst)
            print(f"  ✓ {f}")

print(f"\nDone — {len(html_files)} markdown files converted")
