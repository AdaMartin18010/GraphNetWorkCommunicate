#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图论基础目录思维表征工具文件归类脚本
"""

import os
import shutil
from pathlib import Path

# 获取项目根目录
project_root = Path(__file__).parent.parent
base_dir = project_root / "docs" / "01-图论基础"

# 目标目录
mind_tools_dir = base_dir / "06-思维表征工具"
mind_tools_collection_dir = mind_tools_dir / "思维表征工具集合"

# 创建目录
mind_tools_collection_dir.mkdir(parents=True, exist_ok=True)
print(f"✓ 创建目录: {mind_tools_dir.relative_to(project_root)}")

# 需要移动的文件
files_to_move = []

# 查找思维表征工具集合文件（完整版）
for file in base_dir.glob("思维表征工具集合-*-完整版-2025.md"):
    if file.is_file():
        target = mind_tools_collection_dir / file.name
        files_to_move.append((file, target))

# 查找思维表征工具主文件
main_file = base_dir / "思维表征工具-图论基础.md"
if main_file.exists():
    target = mind_tools_dir / main_file.name
    files_to_move.append((main_file, target))

# 移动文件
moved_count = 0
for source, target in files_to_move:
    if source.exists():
        try:
            shutil.move(str(source), str(target))
            print(f"✓ 已移动: {source.name} -> {target.relative_to(base_dir)}")
            moved_count += 1
        except Exception as e:
            print(f"✗ 移动失败 {source.name}: {e}")

print(f"\n完成！共移动 {moved_count} 个文件")
