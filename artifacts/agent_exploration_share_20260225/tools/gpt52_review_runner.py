#!/usr/bin/env python3
"""Run optional external GPT-5.2 review on generated markdown files.

Usage:
  OPENAI_API_KEY=... python gpt52_review_runner.py

Outputs:
  review_gpt52_public.md
  review_gpt52_internal.md
"""
import os
import json
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / '01_公开版_汇报文档.md',
    ROOT / '02_内部详版_汇报文档.md',
]

API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    raise SystemExit('OPENAI_API_KEY is required.')

API_URL = 'https://api.openai.com/v1/responses'
MODEL = 'gpt-5.2'

PROMPT_PREFIX = (
    '请作为严格编辑审阅者，检查文档的一致性、事实自洽性、图表引用准确性、语义重复和表达清晰度。'
    '输出中文审阅意见，分为：关键问题、建议修改、可选优化。'
)

for fp in FILES:
    text = fp.read_text(encoding='utf-8', errors='ignore')
    payload = {
        'model': MODEL,
        'input': f"{PROMPT_PREFIX}\n\n文档路径: {fp.name}\n\n文档内容:\n{text}",
    }
    data = json.dumps(payload).encode('utf-8')
    req = request.Request(
        API_URL,
        data=data,
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    with request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode('utf-8', errors='ignore'))
    out_text = ''
    for item in result.get('output', []):
        for c in item.get('content', []):
            if c.get('type') == 'output_text':
                out_text += c.get('text', '')
    out_file = ROOT / f"review_gpt52_{'public' if '公开版' in fp.name else 'internal'}.md"
    out_file.write_text(out_text or '(empty response)', encoding='utf-8')
    print(f'written: {out_file}')
