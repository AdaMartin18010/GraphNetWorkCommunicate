#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新交叉引用脚本
修正所有文档中的交叉引用路径
"""

import os
import re
from pathlib import Path

# 模块映射
MODULE_MAP = {
    "01-图论基础": "01-图论基础",
    "02-网络拓扑": "02-网络拓扑",
    "03-通信协议": "03-通信协议",
    "04-分布式系统": "04-分布式系统",
}

def fix_cross_references(content, file_path):
    """修复文件中的交叉引用"""
    original_content = content
    
    # 确定当前文件所在的模块
    current_module = None
    for module in MODULE_MAP.keys():
        if module in file_path:
            current_module = module
            break
    
    # 模式1: 同模块内的引用 (05-高级理论/XXX-深度改进版-2025.md)
    # 应该改为: XXX-深度改进版-2025.md (因为已经在05-高级理论文件夹内)
    pattern1 = re.compile(r'\]\(05-高级理论/([^)]+-深度改进版-2025\.md)\)')
    def replace1(match):
        return f']({match.group(1)})'
    content = pattern1.sub(replace1, content)
    
    # 模式2: 跨模块引用 (../XX-模块/05-高级理论/XXX-深度改进版-2025.md)
    # 应该改为: ../XX-模块/05-高级理论/XXX-深度改进版-2025.md (保持相对路径)
    pattern2 = re.compile(r'\]\(\.\./([^/]+)/05-高级理论/([^)]+-深度改进版-2025\.md)\)')
    def replace2(match):
        module = match.group(1)
        filename = match.group(2)
        return f'](../{module}/05-高级理论/{filename})'
    content = pattern2.sub(replace2, content)
    
    # 模式3: 旧格式引用 (05-高级理论-XXX-深度改进版-2025.md)
    # 应该改为: XXX-深度改进版-2025.md (同模块) 或 ../XX-模块/05-高级理论/XXX-深度改进版-2025.md (跨模块)
    pattern3 = re.compile(r'\]\(05-高级理论-([^)]+-深度改进版-2025\.md)\)')
    def replace3(match):
        filename = match.group(1)
        # 如果当前文件在05-高级理论文件夹内，使用相对路径
        if '05-高级理论' in file_path:
            return f']({filename})'
        else:
            # 否则需要添加路径
            if current_module:
                return f'](05-高级理论/{filename})'
            return f'](05-高级理论/{filename})'
    content = pattern3.sub(replace3, content)
    
    # 模式4: 跨模块旧格式 (../XX-模块/05-高级理论-XXX-深度改进版-2025.md)
    pattern4 = re.compile(r'\]\(\.\./([^/]+)/05-高级理论-([^)]+-深度改进版-2025\.md)\)')
    def replace4(match):
        module = match.group(1)
        filename = match.group(2)
        return f'](../{module}/05-高级理论/{filename})'
    content = pattern4.sub(replace4, content)
    
    return content, content != original_content

def update_all_files(docs_path):
    """更新所有文件的交叉引用"""
    updated_files = []
    
    for root, dirs, files in os.walk(docs_path):
        # 跳过.git目录
        if '.git' in root:
            continue
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content, changed = fix_cross_references(content, file_path)
                    
                    if changed:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        updated_files.append(file_path)
                        print(f"✅ 更新: {file_path}")
                        
                except Exception as e:
                    print(f"❌ 错误 {file_path}: {e}")
    
    return updated_files

def main():
    """主函数"""
    base_path = Path(__file__).parent
    docs_path = base_path / "docs"
    
    print("=" * 60)
    print("更新交叉引用脚本")
    print("=" * 60)
    print()
    
    updated_files = update_all_files(docs_path)
    
    print()
    print("=" * 60)
    print(f"✅ 更新了 {len(updated_files)} 个文件的交叉引用")
    print("=" * 60)

if __name__ == "__main__":
    main()
