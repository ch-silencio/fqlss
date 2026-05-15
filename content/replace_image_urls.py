#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

def replace_all_img_urls(content):
    """同时替换 Markdown 和 HTML 格式的图片地址"""
    
    # 1. 替换 Markdown 格式: ![](/images/xxx)
    content = re.sub(
        r'(!\[.*?\]\()(?:/)?images/(.*?)(\))',
        r'\1https://img.fqlss.com/images/\2\3',
        content
    )
    
    # 2. 替换 HTML 格式: <img src="/images/xxx">
    content = re.sub(
        r'(<img\s+[^>]*src=")(?:/)?images/([^"]+)"',
        r'\1https://img.fqlss.com/images/\2"',
        content
    )
    
    return content

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '/images/' not in content and 'images/' not in content:
        return False
    
    new_content = replace_all_img_urls(content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    post_dir = Path("post")
    if not post_dir.exists():
        print(f"错误：目录 '{post_dir}' 不存在")
        return
    
    md_files = list(post_dir.rglob("*.md"))
    if not md_files:
        print(f"在 '{post_dir}' 下未找到 .md 文件")
        return
    
    modified = 0
    for md_file in md_files:
        if process_file(md_file):
            print(f"✅ 已修改: {md_file}")
            modified += 1
    
    print(f"\n处理完成，共修改 {modified} 个文件。")

if __name__ == "__main__":
    main()
