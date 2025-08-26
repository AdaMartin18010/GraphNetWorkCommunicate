#!/usr/bin/env python3
"""
分布式事件图工具
支持分布式系统事件可视化、因果关系和时序分析
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json
from datetime import datetime

class DistributedEventGraph:
    """分布式事件图生成器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_event_graph(self, events: List[Dict],
                          filename: str = "distributed_events.png"):
        """创建分布式事件图"""
        G = nx.DiGraph()
        
        # 添加事件节点
        for event in events:
            event_id = event['id']
            G.add_node(event_id, **event)
        
        # 添加因果关系边
        for event in events:
            event_id = event['id']
            if 'causes' in event:
                for cause_id in event['causes']:
                    G.add_edge(cause_id, event_id)
        
        # 绘制事件图
        plt.figure(figsize=(15, 10))
        
        # 使用层次布局
        pos = nx.spring_layout(G)
        
        # 根据事件类型着色
        node_colors = []
        for node in G.nodes():
            event_type = G.nodes[node].get('type', 'unknown')
            if event_type == 'send':
                node_colors.append('lightblue')
            elif event_type == 'receive':
                node_colors.append('lightgreen')
            elif event_type == 'internal':
                node_colors.append('lightyellow')
            else:
                node_colors.append('lightgray')
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, 
                              node_color=node_colors,
                              node_size=1000,
                              alpha=0.8)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, 
                              edge_color='red',
                              alpha=0.6,
                              width=2,
                              arrows=True,
                              arrowsize=20)
        
        # 绘制标签
        labels = {node: f"{node}\n{G.nodes[node].get('type', '')}" 
                 for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title("分布式事件因果关系图", fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def create_timeline_diagram(self, events: List[Dict],
                              filename: str = "event_timeline.md"):
        """创建事件时间线图"""
        mermaid_code = "```mermaid\ngantt\n"
        mermaid_code += "    title 分布式事件时间线\n"
        mermaid_code += "    dateFormat  YYYY-MM-DD HH:mm:ss\n"
        mermaid_code += "    section 节点A\n"
        
        # 按节点分组事件
        nodes = {}
        for event in events:
            node = event.get('node', 'unknown')
            if node not in nodes:
                nodes[node] = []
            nodes[node].append(event)
        
        # 为每个节点创建时间线
        for node, node_events in nodes.items():
            mermaid_code += f"    section {node}\n"
            for event in node_events:
                event_id = event['id']
                event_type = event.get('type', 'event')
                start_time = event.get('start_time', '2024-01-01 00:00:00')
                end_time = event.get('end_time', '2024-01-01 00:01:00')
                
                mermaid_code += f"    {event_type} {event_id} :{event_id}, {start_time}, {end_time}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_causality_diagram(self, events: List[Dict],
                               filename: str = "causality_diagram.md"):
        """创建因果关系图"""
        mermaid_code = "```mermaid\ngraph TD\n"
        
        # 添加事件节点
        for event in events:
            event_id = event['id']
            event_type = event.get('type', 'event')
            mermaid_code += f"    {event_id}[{event_id}<br/>{event_type}]\n"
        
        # 添加因果关系边
        for event in events:
            event_id = event['id']
            if 'causes' in event:
                for cause_id in event['causes']:
                    mermaid_code += f"    {cause_id} --> {event_id}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_raft_events_diagram(self, filename: str = "raft_events.md"):
        """创建Raft共识事件图"""
        mermaid_code = """
```mermaid
sequenceDiagram
    participant Node1 as 节点1
    participant Node2 as 节点2
    participant Node3 as 节点3
    
    Note over Node1,Node3: Raft共识事件序列
    
    Node1->>Node1: 开始选举
    Note right of Node1: 任期增加，状态变为Candidate
    
    Node1->>Node2: RequestVote RPC
    Note right of Node1: 请求投票
    
    Node1->>Node3: RequestVote RPC
    Note right of Node1: 请求投票
    
    Node2->>Node1: Vote Granted
    Note left of Node2: 投票给节点1
    
    Node3->>Node1: Vote Granted
    Note left of Node3: 投票给节点1
    
    Note over Node1,Node3: 节点1成为Leader
    
    Node1->>Node2: AppendEntries RPC
    Note right of Node1: 发送心跳
    
    Node1->>Node3: AppendEntries RPC
    Note right of Node1: 发送心跳
    
    Node2->>Node1: AppendEntries Response
    Note left of Node2: 确认心跳
    
    Node3->>Node1: AppendEntries Response
    Note left of Node3: 确认心跳
    
    Note over Node1,Node3: Leader选举完成
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_byzantine_fault_diagram(self, filename: str = "byzantine_fault.md"):
        """创建拜占庭故障图"""
        mermaid_code = """
```mermaid
graph TD
    subgraph 正常节点
        A[节点A - 正常]
        B[节点B - 正常]
        C[节点C - 正常]
    end
    
    subgraph 拜占庭节点
        D[节点D - 拜占庭]
    end
    
    subgraph 消息传递
        A -->|"Attack"| D
        B -->|"Attack"| D
        C -->|"Attack"| D
        D -->|"Attack"| A
        D -->|"Retreat"| B
        D -->|"Attack"| C
    end
    
    subgraph 决策结果
        A -->|"Attack"| Result[结果: 攻击]
        B -->|"Retreat"| Result
        C -->|"Attack"| Result
        D -->|"不一致"| Result
    end
    
    style D fill:#ff9999
    style Result fill:#ffcc99
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_consensus_visualization(self, consensus_rounds: List[Dict],
                                     filename: str = "consensus_rounds.png"):
        """可视化共识轮次"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. 共识轮次时间线
        rounds = [r['round'] for r in consensus_rounds]
        durations = [r['duration'] for r in consensus_rounds]
        axes[0, 0].plot(rounds, durations, 'b-o')
        axes[0, 0].set_title('共识轮次持续时间')
        axes[0, 0].set_xlabel('轮次')
        axes[0, 0].set_ylabel('持续时间 (ms)')
        axes[0, 0].grid(True)
        
        # 2. 参与节点数量
        participants = [r['participants'] for r in consensus_rounds]
        axes[0, 1].bar(rounds, participants, alpha=0.7, color='green')
        axes[0, 1].set_title('参与节点数量')
        axes[0, 1].set_xlabel('轮次')
        axes[0, 1].set_ylabel('节点数量')
        axes[0, 1].grid(True)
        
        # 3. 共识成功率
        success_rates = [r['success_rate'] for r in consensus_rounds]
        axes[1, 0].plot(rounds, success_rates, 'r-s')
        axes[1, 0].set_title('共识成功率')
        axes[1, 0].set_xlabel('轮次')
        axes[1, 0].set_ylabel('成功率 (%)')
        axes[1, 0].grid(True)
        
        # 4. 网络延迟分布
        latencies = []
        for r in consensus_rounds:
            latencies.extend(r.get('latencies', []))
        
        axes[1, 1].hist(latencies, bins=20, alpha=0.7, color='purple')
        axes[1, 1].set_title('网络延迟分布')
        axes[1, 1].set_xlabel('延迟 (ms)')
        axes[1, 1].set_ylabel('频次')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def create_fault_detection_diagram(self, filename: str = "fault_detection.md"):
        """创建故障检测图"""
        mermaid_code = """
```mermaid
stateDiagram-v2
    [*] --> Normal
    Normal --> Suspect : 超时/异常
    Suspect --> Failed : 确认故障
    Suspect --> Normal : 恢复
    Failed --> [*] : 移除节点
    
    state Suspect {
        [*] --> Timeout
        Timeout --> Retry : 重试
        Retry --> Timeout : 继续超时
        Retry --> [*] : 恢复
    }
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)

def main():
    """主函数 - 示例用法"""
    # 初始化分布式事件图生成器
    generator = DistributedEventGraph()
    
    # 创建示例事件
    events = [
        {
            'id': 'E1',
            'type': 'send',
            'node': 'Node1',
            'message': 'Hello',
            'timestamp': '2024-01-01 10:00:00',
            'causes': []
        },
        {
            'id': 'E2',
            'type': 'receive',
            'node': 'Node2',
            'message': 'Hello',
            'timestamp': '2024-01-01 10:00:01',
            'causes': ['E1']
        },
        {
            'id': 'E3',
            'type': 'send',
            'node': 'Node2',
            'message': 'Hi',
            'timestamp': '2024-01-01 10:00:02',
            'causes': ['E2']
        },
        {
            'id': 'E4',
            'type': 'receive',
            'node': 'Node1',
            'message': 'Hi',
            'timestamp': '2024-01-01 10:00:03',
            'causes': ['E3']
        }
    ]
    
    # 创建事件图
    generator.create_event_graph(events)
    
    # 创建时间线图
    generator.create_timeline_diagram(events)
    
    # 创建因果关系图
    generator.create_causality_diagram(events)
    
    # 创建Raft事件图
    generator.create_raft_events_diagram()
    
    # 创建拜占庭故障图
    generator.create_byzantine_fault_diagram()
    
    # 创建故障检测图
    generator.create_fault_detection_diagram()
    
    # 创建共识可视化
    consensus_rounds = [
        {'round': 1, 'duration': 100, 'participants': 5, 'success_rate': 100, 'latencies': [10, 15, 12, 18, 20]},
        {'round': 2, 'duration': 120, 'participants': 4, 'success_rate': 80, 'latencies': [12, 16, 14, 22]},
        {'round': 3, 'duration': 90, 'participants': 5, 'success_rate': 100, 'latencies': [11, 13, 15, 17, 19]},
        {'round': 4, 'duration': 150, 'participants': 3, 'success_rate': 60, 'latencies': [20, 25, 30]}
    ]
    generator.create_consensus_visualization(consensus_rounds)
    
    print("分布式事件图生成完成！输出文件保存在 output/ 目录中。")

if __name__ == "__main__":
    main()
