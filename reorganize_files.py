#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件结构重组脚本
将所有"05-高级理论-XXX"文件移动到"05-高级理论"文件夹并重命名
"""

import os
import re
import shutil
from pathlib import Path

# 需要处理的模块
MODULES = [
    "01-图论基础",
    "02-网络拓扑",
    "03-通信协议",
    "04-分布式系统",
    "05-量子通信",
    "06-生物网络",
]

def find_files_to_move(module_path):
    """查找需要移动的文件"""
    files_to_move = []
    pattern = re.compile(r'^05-高级理论-(.+)-深度改进版-2025\.md$')
    
    for file in os.listdir(module_path):
        if pattern.match(file):
            old_path = os.path.join(module_path, file)
            match = pattern.match(file)
            if match:
                new_name = f"{match.group(1)}-深度改进版-2025.md"
                target_dir = os.path.join(module_path, "05-高级理论")
                new_path = os.path.join(target_dir, new_name)
                files_to_move.append({
                    'old_path': old_path,
                    'new_path': new_path,
                    'old_name': file,
                    'new_name': new_name
                })
    
    return files_to_move

def move_file(file_info):
    """移动并重命名文件"""
    old_path = file_info['old_path']
    new_path = file_info['new_path']
    
    # 确保目标目录存在
    os.makedirs(os.path.dirname(new_path), exist_ok=True)
    
    # 如果目标文件已存在，先检查是否相同
    if os.path.exists(new_path):
        print(f"⚠️  目标文件已存在: {new_path}")
        # 可以选择跳过或覆盖
        return False
    
    # 移动文件
    try:
        shutil.move(old_path, new_path)
        print(f"✅ 移动: {file_info['old_name']} → {file_info['new_name']}")
        return True
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def update_cross_references(docs_path):
    """更新所有文档中的交叉引用"""
    pattern_old = re.compile(r'05-高级理论-([^-]+)-深度改进版-2025\.md')
    
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
                    
                    original_content = content
                    
                    # 替换交叉引用
                    def replace_link(match):
                        topic = match.group(1)
                        # 确定模块路径
                        relative_path = os.path.relpath(file_path, docs_path)
                        if relative_path.startswith('01-图论基础'):
                            return f'05-高级理论/{topic}-深度改进版-2025.md'
                        elif relative_path.startswith('02-网络拓扑'):
                            return f'05-高级理论/{topic}-深度改进版-2025.md'
                        elif relative_path.startswith('03-通信协议'):
                            return f'05-高级理论/{topic}-深度改进版-2025.md'
                        elif relative_path.startswith('04-分布式系统'):
                            return f'05-高级理论/{topic}-深度改进版-2025.md'
                        else:
                            # 跨模块引用需要完整路径
                            return match.group(0)  # 保持原样，稍后处理
                    
                    content = pattern_old.sub(replace_link, content)
                    
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        updated_files.append(file_path)
                        print(f"✅ 更新引用: {file_path}")
                        
                except Exception as e:
                    print(f"❌ 处理文件错误 {file_path}: {e}")
    
    return updated_files

def main():
    """主函数"""
    base_path = Path(__file__).parent
    docs_path = base_path / "docs"
    
    print("=" * 60)
    print("文件结构重组脚本")
    print("=" * 60)
    print()
    
    # 步骤1: 移动文件
    print("步骤1: 移动和重命名文件")
    print("-" * 60)
    
    total_moved = 0
    for module in MODULES:
        module_path = docs_path / module
        if not module_path.exists():
            print(f"⚠️  模块不存在: {module}")
            continue
        
        files_to_move = find_files_to_move(module_path)
        print(f"\n📁 {module}: 找到 {len(files_to_move)} 个文件")
        
        for file_info in files_to_move:
            if move_file(file_info):
                total_moved += 1
    
    print(f"\n✅ 总共移动了 {total_moved} 个文件")
    print()
    
    # 步骤2: 更新交叉引用
    print("步骤2: 更新交叉引用")
    print("-" * 60)
    
    updated_files = update_cross_references(docs_path)
    print(f"\n✅ 更新了 {len(updated_files)} 个文件的交叉引用")
    print()
    
    print("=" * 60)
    print("重组完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
