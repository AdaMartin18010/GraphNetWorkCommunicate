#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件归档执行脚本
用于批量归档项目根目录中的重复报告文件
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# 项目根目录
ROOT_DIR = Path(".")

# 归档目标目录
ARCHIVE_DIR = Path("archive/project-reports")

# 文件映射规则
FILE_MAPPING = {
    # 项目推进报告 -> completion-reports/2025-01/project-advancement/
    "project-advancement": {
        "pattern": "项目推进*.md",
        "dest": "completion-reports/2025-01/project-advancement/",
        "exclude": ["项目推进完成确认书-2025-01.md"]  # 保留关键文件
    },
    
    # 项目持续推进报告 -> completion-reports/2025-01/project-continuation/
    "project-continuation": {
        "pattern": "项目持续推进*.md",
        "dest": "completion-reports/2025-01/project-continuation/",
        "exclude": []
    },
    
    # 项目总结报告 -> completion-reports/2025-01/project-summary/
    "project-summary": {
        "pattern": ["项目最终*.md", "项目完整*.md", "项目全面*.md", "项目100%*.md", "项目当前状态*.md", "项目质量评估*.md"],
        "dest": "completion-reports/2025-01/project-summary/",
        "exclude": ["项目全面对标评估与改进计划-2025-最终版.md", "项目全面评估与改进计划-2025-01-最终版.md"]  # 保留核心文档
    },
    
    # P0任务报告 -> task-reports/2025-01/P0-tasks/
    "P0-tasks": {
        "pattern": "P0任务*.md",
        "dest": "task-reports/2025-01/P0-tasks/",
        "exclude": []
    },
    
    # P1任务报告 -> task-reports/2025-01/P1-tasks/
    "P1-tasks": {
        "pattern": "P1任务*.md",
        "dest": "task-reports/2025-01/P1-tasks/",
        "exclude": []
    },
    
    # P2任务报告 -> task-reports/2025-01/P2-tasks/
    "P2-tasks": {
        "pattern": "P2任务*.md",
        "dest": "task-reports/2025-01/P2-tasks/",
        "exclude": []
    },
    
    # P4任务报告 -> task-reports/2025-01/P4-tasks/
    "P4-tasks": {
        "pattern": "P4任务*.md",
        "dest": "task-reports/2025-01/P4-tasks/",
        "exclude": []
    },
    
    # P5任务报告 -> task-reports/2025-01/P5-tasks/
    "P5-tasks": {
        "pattern": "P5任务*.md",
        "dest": "task-reports/2025-01/P5-tasks/",
        "exclude": []
    },
    
    # 2025-12报告 -> progress-reports/2025-12/
    "2025-12-reports": {
        "pattern": "*2025-12-05.md",
        "dest": "progress-reports/2025-12/",
        "exclude": []
    },
    
    # 任务推进报告 -> progress-reports/2025/
    "task-progress": {
        "pattern": ["任务推进*.md", "阶段*.md", "项目文件梳理*.md", "项目文件清理*.md", "项目核心任务*.md"],
        "dest": "progress-reports/2025/",
        "exclude": ["任务执行框架-2025.md", "项目任务编排与推进计划-2025.md", "项目结构与任务框架-2025.md"]  # 保留核心文档
    },
    
    # 应用案例报告 -> application-reports/2025-01/
    "application-reports": {
        "pattern": ["应用案例*.md", "测试用例*.md"],
        "dest": "application-reports/2025-01/",
        "exclude": []
    },
    
    # 思维工具报告 -> mind-tools-reports/2025-01/
    "mind-tools-reports": {
        "pattern": ["思维工具*.md", "跨模块关联*.md"],
        "dest": "mind-tools-reports/2025-01/",
        "exclude": ["跨模块概念关系映射表-增强版-2025-01.md"]  # 保留核心文档
    },
    
    # 计划报告 -> planning-reports/2025/
    "planning-reports": {
        "pattern": ["*计划*.md", "*报告*.md", "*总结*.md", "*进展*.md", "*评估*.md", "*检查*.md", "*扩展*.md", "*深化*.md", "*优化*.md", "*梳理*.md", "*标记*.md", "*矩阵*.md", "*标准*.md", "*规范*.md", "*清单*.md", "*说明*.md", "*对照*.md", "*概念*.md", "*文件*.md", "*内容*.md", "*数据*.md", "*格式*.md", "*术语*.md", "*多维*.md", "*已扩展*.md", "*待完善*.md", "*待扩展*.md", "*A级*.md", "*B级*.md", "*P0文件*.md", "*P1文件*.md"],
        "dest": "planning-reports/2025/",
        "exclude": [
            "项目全面对标评估与改进计划-2025-最终版.md",
            "项目全面评估与改进计划-2025-01-最终版.md",
            "项目任务编排与推进计划-2025.md",
            "项目结构与任务框架-2025.md",
            "任务执行框架-2025.md",
            "跨模块概念关系映射表-增强版-2025-01.md",
            "文件归档执行计划-2025-01.md",
            "项目内容批判性评价与改进建议-2025-01.md"
        ]  # 保留核心文档
    }
}

# 必须保留的核心文件
CORE_FILES = {
    "README.md",
    "README_EN.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PROJECT_COMPLETION.md",
    "项目全面对标评估与改进计划-2025-最终版.md",
    "项目全面评估与改进计划-2025-01-最终版.md",
    "项目任务编排与推进计划-2025.md",
    "项目结构与任务框架-2025.md",
    "任务执行框架-2025.md",
    "跨模块概念关系映射表-增强版-2025-01.md",
    "文件归档执行计划-2025-01.md",
    "项目内容批判性评价与改进建议-2025-01.md",
    "归档执行脚本-2025-01.py",
    "pytest.ini",
    "reorganize_files.py",
    "update_cross_references.py"
}

def create_archive_directories():
    """创建归档目录结构"""
    print("创建归档目录结构...")
    for category, config in FILE_MAPPING.items():
        dest_path = ARCHIVE_DIR / config["dest"]
        dest_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {dest_path}")
    print("归档目录结构创建完成！\n")

def match_files(pattern):
    """匹配文件模式"""
    if isinstance(pattern, str):
        return list(ROOT_DIR.glob(pattern))
    elif isinstance(pattern, list):
        files = []
        for p in pattern:
            files.extend(ROOT_DIR.glob(p))
        return files
    return []

def archive_files():
    """执行文件归档"""
    archived_count = 0
    skipped_count = 0
    error_count = 0
    
    print("开始归档文件...\n")
    
    for category, config in FILE_MAPPING.items():
        print(f"处理类别: {category}")
        dest_path = ARCHIVE_DIR / config["dest"]
        exclude_set = set(config.get("exclude", []))
        
        # 匹配文件
        if isinstance(config["pattern"], str):
            files = match_files(config["pattern"])
        elif isinstance(config["pattern"], list):
            files = match_files(config["pattern"])
        else:
            files = []
        
        # 归档文件
        for file_path in files:
            if not file_path.is_file() or file_path.suffix != ".md":
                continue
            
            # 检查是否为核心文件
            if file_path.name in CORE_FILES:
                skipped_count += 1
                print(f"  跳过核心文件: {file_path.name}")
                continue
            
            # 检查是否在排除列表中
            if file_path.name in exclude_set:
                skipped_count += 1
                print(f"  跳过排除文件: {file_path.name}")
                continue
            
            # 移动文件
            try:
                dest_file = dest_path / file_path.name
                if dest_file.exists():
                    # 如果目标文件已存在，添加时间戳
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    dest_file = dest_path / f"{file_path.stem}_{timestamp}{file_path.suffix}"
                
                shutil.move(str(file_path), str(dest_file))
                archived_count += 1
                print(f"  ✓ 归档: {file_path.name} -> {dest_path}")
            except Exception as e:
                error_count += 1
                print(f"  ✗ 错误: {file_path.name} - {e}")
        
        print()
    
    print(f"归档完成！")
    print(f"  归档文件数: {archived_count}")
    print(f"  跳过文件数: {skipped_count}")
    print(f"  错误文件数: {error_count}\n")
    
    return archived_count, skipped_count, error_count

def create_archive_index():
    """创建归档索引"""
    index_content = f"""# 归档索引 / Archive Index 2025-01

## 📋 **归档概览 / Archive Overview**

**归档日期**: {datetime.now().strftime("%Y年%m月%d日")}
**归档文件总数**: 约131个文件
**归档类别**: 7个主要类别

---

## 📁 **归档目录结构 / Archive Directory Structure**

"""
    
    for category, config in FILE_MAPPING.items():
        dest_path = config["dest"]
        index_content += f"### {category}\n\n"
        index_content += f"- **归档位置**: `{dest_path}`\n"
        index_content += f"- **文件模式**: {config['pattern']}\n"
        if config.get("exclude"):
            index_content += f"- **排除文件**: {', '.join(config['exclude'])}\n"
        index_content += "\n"
    
    index_content += """---

## 📝 **归档说明 / Archive Notes**

1. **归档目的**: 清理项目根目录，提升项目整洁度和可维护性
2. **归档原则**: 归档与项目核心主题无关的重复报告文件
3. **保留原则**: 保留核心项目文档和最新关键报告

---

## 🔗 **相关文档 / Related Documents**

- [文件归档执行计划-2025-01.md](../文件归档执行计划-2025-01.md) - 详细归档计划
- [项目全面评估与改进计划-2025-01-最终版.md](../项目全面评估与改进计划-2025-01-最终版.md) - 项目评估和改进计划

---

**索引版本**: v1.0
**创建时间**: 2025年1月
**维护者**: GraphNetWorkCommunicate项目组
"""
    
    index_file = ARCHIVE_DIR / "archive-index.md"
    index_file.write_text(index_content, encoding="utf-8")
    print(f"归档索引已创建: {index_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("文件归档执行脚本")
    print("=" * 60)
    print()
    
    # 创建归档目录
    create_archive_directories()
    
    # 执行归档
    archived_count, skipped_count, error_count = archive_files()
    
    # 创建归档索引
    create_archive_index()
    
    print("=" * 60)
    print("归档执行完成！")
    print("=" * 60)
    print(f"\n统计信息:")
    print(f"  归档文件数: {archived_count}")
    print(f"  跳过文件数: {skipped_count}")
    print(f"  错误文件数: {error_count}")
    print(f"\n请检查归档结果，确认无误后更新README.md")

if __name__ == "__main__":
    main()
