#!/usr/bin/env python3
"""
量子电路图绘制工具
支持量子电路、量子网络、量子态等可视化
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector, Operator
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import json

class QuantumCircuitDrawer:
    """量子电路图绘制器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def draw_quantum_circuit(self, circuit: QuantumCircuit,
                           filename: str = "quantum_circuit.png",
                           style: str = "default"):
        """绘制量子电路图"""
        # 使用Qiskit的绘图功能
        fig = circuit.draw(output='mpl', style=style)
        
        # 保存图片
        output_path = self.output_dir / filename
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return str(output_path)
    
    def visualize_quantum_state(self, state: Statevector,
                              filename: str = "quantum_state.png"):
        """可视化量子态"""
        # 绘制Bloch球表示
        fig = plot_bloch_multivector(state)
        
        # 保存图片
        output_path = self.output_dir / filename
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return str(output_path)
    
    def plot_measurement_histogram(self, counts: Dict[str, int],
                                 filename: str = "measurement_histogram.png"):
        """绘制测量结果直方图"""
        # 使用Qiskit的直方图功能
        fig = plot_histogram(counts)
        
        # 保存图片
        output_path = self.output_dir / filename
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return str(output_path)
    
    def create_bb84_circuit_diagram(self, filename: str = "bb84_circuit.md"):
        """创建BB84协议的电路图"""
        # 创建BB84协议的Mermaid图
        mermaid_code = """
```mermaid
sequenceDiagram
    participant Alice as Alice
    participant Channel as 量子信道
    participant Bob as Bob
    participant Eve as Eve (窃听者)
    
    Note over Alice,Bob: BB84量子密钥分发协议
    
    Alice->>Alice: 随机生成比特串
    Alice->>Alice: 随机选择测量基
    Alice->>Channel: 发送量子态
    Note over Channel: 量子信道传输
    Eve->>Channel: 窃听量子态
    Channel->>Bob: 接收量子态
    Bob->>Bob: 随机选择测量基
    Bob->>Bob: 测量量子态
    
    Alice->>Bob: 经典信道：公布测量基
    Bob->>Alice: 经典信道：公布测量基
    
    Note over Alice,Bob: 基匹配筛选
    Alice->>Bob: 经典信道：公布部分比特
    Bob->>Alice: 经典信道：公布部分比特
    
    Note over Alice,Bob: 错误率估计
    Note over Alice,Bob: 隐私放大
    Note over Alice,Bob: 生成最终密钥
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def visualize_quantum_network(self, nodes: List[str],
                                edges: List[Tuple[str, str]],
                                filename: str = "quantum_network.png"):
        """可视化量子网络拓扑"""
        import networkx as nx
        
        # 创建网络图
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        
        plt.figure(figsize=(12, 8))
        
        # 使用spring布局
        pos = nx.spring_layout(G)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, 
                              node_color='lightgreen',
                              node_size=1000,
                              alpha=0.8)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, 
                              edge_color='blue',
                              alpha=0.6,
                              width=3)
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, 
                               font_size=12,
                               font_weight='bold')
        
        plt.title("量子网络拓扑", fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def create_quantum_gate_visualization(self, gate_name: str,
                                        matrix: np.ndarray,
                                        filename: str = "quantum_gate.png"):
        """可视化量子门"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 绘制矩阵的实部
        im1 = ax1.imshow(matrix.real, cmap='RdBu_r', aspect='equal')
        ax1.set_title(f'{gate_name} - 实部')
        ax1.set_xlabel('列')
        ax1.set_ylabel('行')
        plt.colorbar(im1, ax=ax1)
        
        # 绘制矩阵的虚部
        im2 = ax2.imshow(matrix.imag, cmap='RdBu_r', aspect='equal')
        ax2.set_title(f'{gate_name} - 虚部')
        ax2.set_xlabel('列')
        ax2.set_ylabel('行')
        plt.colorbar(im2, ax=ax2)
        
        plt.tight_layout()
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def generate_quantum_protocol_sequence(self, protocol_name: str,
                                         steps: List[Dict],
                                         filename: str = "protocol_sequence.md"):
        """生成量子协议时序图"""
        mermaid_code = f"```mermaid\nsequenceDiagram\n"
        mermaid_code += f"    title {protocol_name}协议时序图\n\n"
        
        for step in steps:
            actor1 = step.get('from', 'Alice')
            actor2 = step.get('to', 'Bob')
            message = step.get('message', '量子态')
            note = step.get('note', '')
            
            mermaid_code += f"    {actor1}->>{actor2}: {message}\n"
            if note:
                mermaid_code += f"    Note over {actor1},{actor2}: {note}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)

def main():
    """主函数 - 示例用法"""
    # 创建BB84协议电路
    qc = QuantumCircuit(2, 2)
    qc.h(0)  # Hadamard门
    qc.cx(0, 1)  # CNOT门
    qc.measure([0, 1], [0, 1])
    
    # 初始化绘制器
    drawer = QuantumCircuitDrawer()
    
    # 绘制量子电路
    drawer.draw_quantum_circuit(qc, "bb84_circuit.png")
    
    # 创建BB84协议时序图
    drawer.create_bb84_circuit_diagram()
    
    # 可视化量子网络
    nodes = ['Alice', 'Bob', 'Charlie', 'David']
    edges = [('Alice', 'Bob'), ('Bob', 'Charlie'), ('Charlie', 'David')]
    drawer.visualize_quantum_network(nodes, edges)
    
    # 可视化量子门
    hadamard_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    drawer.create_quantum_gate_visualization("Hadamard", hadamard_matrix)
    
    print("量子电路可视化完成！输出文件保存在 output/ 目录中。")

if __name__ == "__main__":
    main()
