#!/usr/bin/env python3
"""
形式化证明图工具
支持形式化证明推理链路、交换图等可视化
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json

class FormalProofDiagram:
    """形式化证明图生成器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_proof_tree(self, proof_steps: List[Dict],
                         filename: str = "proof_tree.md"):
        """创建证明树图"""
        mermaid_code = "```mermaid\ngraph TD\n"
        mermaid_code += "    title 形式化证明树\n\n"
        
        # 添加证明步骤节点
        for i, step in enumerate(proof_steps):
            step_id = f"Step{i+1}"
            step_name = step.get('name', f'步骤{i+1}')
            step_type = step.get('type', 'inference')
            
            if step_type == 'axiom':
                mermaid_code += f"    {step_id}[{step_name}<br/>公理]\n"
            elif step_type == 'theorem':
                mermaid_code += f"    {step_id}[{step_name}<br/>定理]\n"
            elif step_type == 'inference':
                mermaid_code += f"    {step_id}[{step_name}<br/>推理]\n"
            else:
                mermaid_code += f"    {step_id}[{step_name}]\n"
        
        # 添加推理关系边
        for i, step in enumerate(proof_steps):
            step_id = f"Step{i+1}"
            if 'premises' in step:
                for premise in step['premises']:
                    mermaid_code += f"    {premise} --> {step_id}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_category_diagram(self, objects: List[str],
                              morphisms: List[Tuple[str, str, str]],
                              filename: str = "category_diagram.md"):
        """创建范畴交换图"""
        mermaid_code = "```mermaid\ngraph LR\n"
        mermaid_code += "    title 范畴交换图\n\n"
        
        # 添加对象节点
        for obj in objects:
            mermaid_code += f"    {obj}[{obj}]\n"
        
        # 添加态射边
        for source, target, morphism in morphisms:
            mermaid_code += f"    {source} -->|{morphism}| {target}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_logic_diagram(self, premises: List[str],
                           conclusion: str,
                           inference_rules: List[str],
                           filename: str = "logic_diagram.md"):
        """创建逻辑推理图"""
        mermaid_code = "```mermaid\ngraph TD\n"
        mermaid_code += "    title 逻辑推理图\n\n"
        
        # 添加前提
        for i, premise in enumerate(premises):
            premise_id = f"P{i+1}"
            mermaid_code += f"    {premise_id}[{premise}]\n"
        
        # 添加推理规则
        for i, rule in enumerate(inference_rules):
            rule_id = f"R{i+1}"
            mermaid_code += f"    {rule_id}[{rule}]\n"
        
        # 添加结论
        mermaid_code += f"    C[{conclusion}]\n"
        
        # 添加推理关系
        for i, rule in enumerate(inference_rules):
            rule_id = f"R{i+1}"
            if i < len(premises):
                premise_id = f"P{i+1}"
                mermaid_code += f"    {premise_id} --> {rule_id}\n"
            if i == len(inference_rules) - 1:
                mermaid_code += f"    {rule_id} --> C\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_type_theory_diagram(self, types: List[str],
                                 terms: List[str],
                                 type_assignments: List[Tuple[str, str]],
                                 filename: str = "type_theory.md"):
        """创建类型论图"""
        mermaid_code = "```mermaid\ngraph TD\n"
        mermaid_code += "    title 类型论图\n\n"
        
        # 添加类型节点
        for type_name in types:
            mermaid_code += f"    {type_name}[{type_name}<br/>类型]\n"
        
        # 添加项节点
        for term in terms:
            mermaid_code += f"    {term}[{term}<br/>项]\n"
        
        # 添加类型指派关系
        for term, type_name in type_assignments:
            mermaid_code += f"    {term} -->|: {type_name}| {type_name}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_model_checking_diagram(self, states: List[str],
                                    transitions: List[Tuple[str, str, str]],
                                    properties: List[str],
                                    filename: str = "model_checking.md"):
        """创建模型检测图"""
        mermaid_code = "```mermaid\nstateDiagram-v2\n"
        mermaid_code += "    title 模型检测状态图\n\n"
        
        # 添加状态
        for state in states:
            mermaid_code += f"    {state}\n"
        
        # 添加状态转换
        for from_state, to_state, condition in transitions:
            mermaid_code += f"    {from_state} --> {to_state} : {condition}\n"
        
        # 添加性质验证
        mermaid_code += "\n    note right of " + states[0] + " : 性质验证\n"
        for i, prop in enumerate(properties):
            mermaid_code += f"    note right of {states[0]} : {prop}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_automated_theorem_proving_diagram(self, filename: str = "automated_theorem_proving.md"):
        """创建自动定理证明图"""
        mermaid_code = """
```mermaid
graph TD
    subgraph 输入
        A[问题陈述]
        B[公理集合]
        C[推理规则]
    end
    
    subgraph 证明搜索
        D[搜索策略]
        E[启发式函数]
        F[剪枝算法]
    end
    
    subgraph 证明生成
        G[证明树构建]
        H[证明验证]
        I[证明优化]
    end
    
    subgraph 输出
        J[证明结果]
        K[反例构造]
        L[证明统计]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    D --> F
    E --> G
    F --> G
    G --> H
    H --> I
    I --> J
    H --> K
    I --> L
    
    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#e1f5fe
    style J fill:#c8e6c9
    style K fill:#ffcdd2
    style L fill:#fff3e0
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_formal_verification_workflow(self, filename: str = "formal_verification_workflow.md"):
        """创建形式化验证工作流图"""
        mermaid_code = """
```mermaid
flowchart TD
    A[系统规范] --> B[形式化建模]
    B --> C[性质定义]
    C --> D[验证方法选择]
    
    D --> E{验证类型}
    E -->|定理证明| F[自动定理证明]
    E -->|模型检测| G[状态空间搜索]
    E -->|抽象解释| H[抽象域分析]
    
    F --> I[证明生成]
    G --> J[反例构造]
    H --> K[抽象验证]
    
    I --> L[结果分析]
    J --> L
    K --> L
    
    L --> M{验证结果}
    M -->|成功| N[系统正确]
    M -->|失败| O[错误修复]
    M -->|未知| P[进一步分析]
    
    O --> B
    P --> D
    
    style A fill:#e3f2fd
    style N fill:#c8e6c9
    style O fill:#ffcdd2
    style P fill:#fff3e0
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_proof_complexity_analysis(self, proof_lengths: List[int],
                                       proof_times: List[float],
                                       filename: str = "proof_complexity.png"):
        """创建证明复杂度分析图"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. 证明长度分布
        axes[0, 0].hist(proof_lengths, bins=20, alpha=0.7, color='blue')
        axes[0, 0].set_title('证明长度分布')
        axes[0, 0].set_xlabel('证明长度')
        axes[0, 0].set_ylabel('频次')
        
        # 2. 证明时间分布
        axes[0, 1].hist(proof_times, bins=20, alpha=0.7, color='green')
        axes[0, 1].set_title('证明时间分布')
        axes[0, 1].set_xlabel('证明时间 (秒)')
        axes[0, 1].set_ylabel('频次')
        
        # 3. 长度vs时间散点图
        axes[1, 0].scatter(proof_lengths, proof_times, alpha=0.6, color='red')
        axes[1, 0].set_title('证明长度 vs 证明时间')
        axes[1, 0].set_xlabel('证明长度')
        axes[1, 0].set_ylabel('证明时间 (秒)')
        
        # 4. 复杂度统计
        stats = {
            '平均长度': np.mean(proof_lengths),
            '平均时间': np.mean(proof_times),
            '最长证明': max(proof_lengths),
            '最长时间': max(proof_times),
            '最短证明': min(proof_lengths),
            '最短时间': min(proof_times)
        }
        
        y_pos = np.arange(len(stats))
        values = list(stats.values())
        axes[1, 1].barh(y_pos, values, alpha=0.7, color='purple')
        axes[1, 1].set_yticks(y_pos)
        axes[1, 1].set_yticklabels(list(stats.keys()))
        axes[1, 1].set_title('证明复杂度统计')
        axes[1, 1].set_xlabel('数值')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)

def main():
    """主函数 - 示例用法"""
    # 初始化形式化证明图生成器
    generator = FormalProofDiagram()
    
    # 创建证明树
    proof_steps = [
        {'name': '公理1', 'type': 'axiom'},
        {'name': '公理2', 'type': 'axiom'},
        {'name': '推理1', 'type': 'inference', 'premises': ['Step1', 'Step2']},
        {'name': '定理1', 'type': 'theorem', 'premises': ['Step3']}
    ]
    generator.create_proof_tree(proof_steps)
    
    # 创建范畴交换图
    objects = ['A', 'B', 'C']
    morphisms = [
        ('A', 'B', 'f'),
        ('B', 'C', 'g'),
        ('A', 'C', 'g∘f')
    ]
    generator.create_category_diagram(objects, morphisms)
    
    # 创建逻辑推理图
    premises = ['P → Q', 'P']
    conclusion = 'Q'
    inference_rules = ['Modus Ponens']
    generator.create_logic_diagram(premises, conclusion, inference_rules)
    
    # 创建类型论图
    types = ['Nat', 'Bool', 'List Nat']
    terms = ['0', 'true', '[]', 'cons']
    type_assignments = [
        ('0', 'Nat'),
        ('true', 'Bool'),
        ('[]', 'List Nat'),
        ('cons', 'Nat → List Nat → List Nat')
    ]
    generator.create_type_theory_diagram(types, terms, type_assignments)
    
    # 创建模型检测图
    states = ['S0', 'S1', 'S2']
    transitions = [
        ('S0', 'S1', 'a'),
        ('S1', 'S2', 'b'),
        ('S2', 'S0', 'c')
    ]
    properties = ['AG(p)', 'EF(q)']
    generator.create_model_checking_diagram(states, transitions, properties)
    
    # 创建自动定理证明图
    generator.create_automated_theorem_proving_diagram()
    
    # 创建形式化验证工作流图
    generator.create_formal_verification_workflow()
    
    # 创建证明复杂度分析
    proof_lengths = [10, 15, 20, 25, 30, 35, 40, 45, 50]
    proof_times = [1.2, 2.1, 3.5, 5.2, 7.8, 11.3, 15.7, 21.2, 28.9]
    generator.create_proof_complexity_analysis(proof_lengths, proof_times)
    
    print("形式化证明图生成完成！输出文件保存在 output/ 目录中。")

if __name__ == "__main__":
    main()
