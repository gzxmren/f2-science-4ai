#!/usr/bin/env python3
"""将 F2 Science 项目中所有 .md 文件转为 .html（内联样式，不依赖外链）"""

import os, re, html as htmlmod

BASE = "/home/xmren/Documents/ebooks/karina book/F2/Sience/4ai"

CSS_TEMPLATE = """\
body{font-family:-apple-system,'Segoe UI','Noto Sans SC',sans-serif;background:#f5f5f7;color:#1d1d1f;line-height:1.7;padding:20px;margin:0}
.container{max-width:800px;margin:0 auto}
.header{background:linear-gradient(135deg,#34c759,#5856d6);color:#fff;padding:24px;border-radius:16px;margin-bottom:24px}
.header h1{font-size:26px;margin-bottom:4px}.header .sub{opacity:.85;font-size:14px}
.card{background:#fff;border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
.card h2{font-size:20px;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #f0f0f2}
.card h3{font-size:16px;margin:16px 0 8px}
.card h4{font-size:14px;margin:10px 0 4px;color:#555}
.data-table{width:100%;border-collapse:collapse;margin:8px 0;font-size:13px}
.data-table th{background:#e8edf5;padding:6px 10px;text-align:center;font-weight:600;border:1px solid #d0d5dd}
.data-table td{padding:6px 10px;text-align:center;border:1px solid #d0d5dd}
pre{background:#f0f0f2;padding:12px;border-radius:8px;font-size:13px;white-space:pre-wrap;line-height:1.6;overflow-x:auto}
code{background:#f0f0f2;padding:2px 4px;border-radius:4px;font-size:13px}
pre code{background:none;padding:0}
.context-box{background:#f0f4ff;border-radius:8px;padding:12px;margin:10px 0;border-left:3px solid #007aff;font-size:13px;color:#555;line-height:1.6}
.block-highlight{background:#fffde7;border-left:4px solid #ffd600;border-radius:8px;padding:10px 14px;margin:10px 0;font-size:13px}
.tag{display:inline-block;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:600}
.tag-recall{background:#e8f5e9;color:#2e7d32}.tag-understand{background:#fff3e0;color:#e65100}
.tag-explain{background:#e3f2fd;color:#1565c0}.tag-analyze{background:#fce4ec;color:#c62828}
.tag-compare{background:#f3e5f5;color:#6a1b9a}.tag-evaluate{background:#ffebee;color:#b71c1c}
.q-item{background:#f9f9fb;border-radius:10px;padding:14px;margin:10px 0;border-left:4px solid #34c759;cursor:pointer}
.q-item .q{font-weight:600;font-size:14px;margin-bottom:4px}
.q-item .hint{font-size:12px;color:#8e8e93;margin:4px 0}
.q-item .a{display:none;background:#e8f5e9;border-radius:8px;padding:10px;margin-top:8px;font-size:13px;line-height:1.8}
.q-item.show .a{display:block}
ul,ol{padding-left:20px;font-size:14px;color:#333;line-height:1.8}
li{margin:4px 0}
p{font-size:14px;color:#333;line-height:1.8;margin:8px 0}
strong{color:#1d1d1f}
hr{display:none}
@media(max-width:600px){.data-table{font-size:12px}}
"""

def escape(text):
    return htmlmod.escape(text)

def convert_md_to_html(md_text, title):
    """将 Markdown 文本转换为内联 HTML"""
    lines = md_text.split('\n')
    html_parts = []
    in_code_block = False
    code_buffer = []
    in_table = False
    table_buffer = []
    in_blockquote = False
    blockquote_buffer = []
    in_list = False
    list_type = None
    list_buffer = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 代码块
        if line.strip().startswith('```'):
            if in_code_block:
                html_parts.append(f'<pre><code>{"".join(code_buffer)}</code></pre>\n')
                code_buffer = []
                in_code_block = False
                i += 1
                continue
            else:
                in_code_block = True
                i += 1
                continue
        if in_code_block:
            code_buffer.append(escape(line) + '\n')
            i += 1
            continue
        
        # 空行
        if not line.strip():
            # 结束 blockquote
            if in_blockquote:
                html_parts.append(f'<div class="context-box">{"<br>".join(blockquote_buffer)}</div>\n')
                blockquote_buffer = []
                in_blockquote = False
            # 结束 table
            if in_table and table_buffer:
                html_parts.append(_render_table(table_buffer))
                table_buffer = []
                in_table = False
            # 结束 list
            if in_list and list_buffer:
                html_parts.append(_render_list(list_type, list_buffer))
                list_buffer = []
                in_list = False
                list_type = None
            i += 1
            continue
        
        # 分隔线
        if line.strip() == '---':
            i += 1
            continue
        
        # 标题
        h_match = re.match(r'^(#{1,4})\s+(.+)$', line)
        if h_match:
            level = len(h_match.group(1))
            text = h_match.group(2).strip()
            html_parts.append(f'<h{level}>{text}</h{level}>\n')
            i += 1
            continue
        
        # 引用块
        bq_match = re.match(r'^>\s*(.*)$', line)
        if bq_match:
            in_blockquote = True
            blockquote_buffer.append(bq_match.group(1))
            i += 1
            continue
        
        # 表格
        if line.strip().startswith('|') and line.strip().endswith('|'):
            in_table = True
            table_buffer.append(line)
            i += 1
            continue
        
        # 无序列表
        ul_match = re.match(r'^(\s*)[-*]\s+(.+)$', line)
        if ul_match:
            if not in_list:
                in_list = True
                list_type = 'ul'
            indent = len(ul_match.group(1))
            text = ul_match.group(2)
            list_buffer.append((indent, text))
            i += 1
            continue
        
        # 有序列表
        ol_match = re.match(r'^(\s*)\d+\.\s+(.+)$', line)
        if ol_match:
            if not in_list:
                in_list = True
                list_type = 'ol'
            indent = len(ol_match.group(1))
            text = ol_match.group(2)
            list_buffer.append((indent, text))
            i += 1
            continue
        
        # 段落（普通行）
        # 先 flush pending items
        if in_table and table_buffer:
            html_parts.append(_render_table(table_buffer))
            table_buffer = []
            in_table = False
        if in_list and list_buffer:
            html_parts.append(_render_list(list_type, list_buffer))
            list_buffer = []
            in_list = False
            list_type = None
        if in_blockquote:
            html_parts.append(f'<div class="context-box">{"<br>".join(blockquote_buffer)}</div>\n')
            blockquote_buffer = []
            in_blockquote = False
        
        # 处理内联格式
        processed = _process_inline(line)
        if processed.strip():
            html_parts.append(f'<p>{processed}</p>\n')
        i += 1
    
    # flush remaining
    if in_code_block and code_buffer:
        html_parts.append(f'<pre><code>{"".join(code_buffer)}</code></pre>\n')
    if in_blockquote and blockquote_buffer:
        html_parts.append(f'<div class="context-box">{"<br>".join(blockquote_buffer)}</div>\n')
    if in_table and table_buffer:
        html_parts.append(_render_table(table_buffer))
    if in_list and list_buffer:
        html_parts.append(_render_list(list_type, list_buffer))
    
    return ''.join(html_parts)

def _process_inline(text):
    """处理行内格式：加粗、代码、图片"""
    text = escape(text)
    # 代码 `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # 加粗 **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return text

def _render_table(rows):
    """渲染 Markdown 表格为 HTML 表格"""
    if len(rows) < 2:
        return ''
    # 过滤分隔行（|---|...|）
    data_rows = [r for r in rows if not re.match(r'^\|[\s\-:]+\|', r)]
    if not data_rows:
        return ''
    
    header = data_rows[0]
    headers = [h.strip().strip('-').strip(':') for h in header.split('|') if h.strip()]
    
    html = '<table class="data-table">\n<thead><tr>'
    for h in headers:
        html += f'<th>{h}</th>'
    html += '</tr></thead>\n<tbody>\n'
    
    for row in data_rows[1:]:
        cells = [c.strip() for c in row.split('|') if c.strip() or row.split('|').index(c) > 0]
        # 更安全的解析
        parts = row.split('|')
        cells = []
        for p in parts:
            stripped = p.strip()
            if stripped or len(parts) > 2:
                cells.append(stripped)
        if len(cells) <= 2:
            cells = [c.strip() for c in row.split('|') if c.strip()]
        if len(cells) <= 1:
            continue
        html += '<tr>'
        for c in cells:
            if c and c.startswith('**') and c.endswith('**'):
                c = f'<strong>{c[2:-2]}</strong>'
            html += f'<td>{c}</td>'
        html += '</tr>\n'
    
    html += '</tbody>\n</table>\n'
    return html

def _render_list(list_type, items):
    """渲染列表"""
    html = f'<{list_type}>\n'
    for indent, text in items:
        bullet = '*' if list_type == 'ul' else '1.'
        processed = text
        if '—' in processed or '→' in processed:
            processed = _process_inline(processed)
        html += f'<li>{processed}</li>\n'
    html += f'</{list_type}>\n'
    return html

def make_html(title, body_content):
    """组装完整 HTML 文档"""
    body_content = body_content.replace('class="q-item"', 'class="q-item" onclick="this.classList.toggle(\'show\')"')
    script = '<script>document.querySelectorAll(\'.q-item\').forEach(function(el){el.addEventListener(\'click\',function(){this.classList.toggle(\'show\')})})</script>'
    return f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<style>{CSS_TEMPLATE}</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>{escape(title)}</h1>
<div class="sub">F2 Science 复习资料</div>
</div>
{body_content}
</div>
{script}
</body>
</html>'''

# === 转换映射 ===
CONVERSIONS = [
    # from_CHN_His
    ("from_CHN_His/技能框架_史料分析.md", "from_CHN_His/技能框架_史料分析.html", "史料分析框架"),
    ("from_CHN_His/技能框架_因果鏈分析.md", "from_CHN_His/技能框架_因果鏈分析.html", "因果鏈分析框架"),
    ("from_CHN_His/技能框架_對比分析.md", "from_CHN_His/技能框架_對比分析.html", "對比分析框架"),
    ("from_CHN_His/技能框架_評價分析.md", "from_CHN_His/技能框架_評價分析.html", "評價分析框架"),
    ("from_CHN_His/認知深度索引圖.md", "from_CHN_His/認知深度索引圖.html", "認知深度索引圖"),
    ("from_CHN_His/agent_handoff_deliverable.md", "from_CHN_His/agent_handoff_deliverable.html", "從地理到歷史：答題方法框架的遷移經驗總結"),
    # from_geo
    ("from_geo/agent_handoff_history_methodology.md", "from_geo/agent_handoff_history_methodology.html", "给中国历史复习 Agent 的沟通文档"),
    # root
    ("F2_Science_复习计划.md", "F2_Science_复习计划.html", "F2 Science 复习计划"),
    ("F2_Science_Book2A_OCR_extracted.md", "F2_Science_Book2A_OCR_extracted.html", "Book 2A OCR 提取内容"),
    ("F2_Science_Book2B_OCR_extracted.md", "F2_Science_Book2B_OCR_extracted.html", "Book 2B OCR 提取内容"),
    ("F2_Science_Assignment_Book_2A_提取.md", "F2_Science_Assignment_Book_2A_提取.html", "Assignment Book 2A 提取"),
    ("F2_Science_Assignment_Book_2B_提取.md", "F2_Science_Assignment_Book_2B_提取.html", "Assignment Book 2B 提取"),
]

def main():
    for src_rel, dst_rel, title in CONVERSIONS:
        src = os.path.join(BASE, src_rel)
        dst = os.path.join(BASE, dst_rel)
        if not os.path.exists(src):
            print(f"⚠ SKIP: {src_rel} not found")
            continue
        with open(src, 'r', encoding='utf-8') as f:
            md_text = f.read()
        body = convert_md_to_html(md_text, title)
        html = make_html(title, body)
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ {src_rel} → {dst_rel}")
    print(f"\n🎉 全部转换完成！共 {len(CONVERSIONS)} 个文件")

if __name__ == '__main__':
    main()
