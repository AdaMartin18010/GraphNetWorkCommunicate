#!/usr/bin/env python3
"""
生物网络可视化工具
支持神经网络、基因调控网络、蛋白质相互作用网络等可视化
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json

class BiologicalNetworkVisualizer:
    """生物网络可视化器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def visualize_neural_network(self, layers: List[int],
                               connections: List[Tuple[int, int, float]],
                               filename: str = "neural_network.png"):
        """可视化神经网络结构"""
        G = nx.DiGraph()
        
        # 添加节点（神经元）
        node_id = 0
        layer_positions = {}
        for layer_idx, layer_size in enumerate(layers):
            layer_positions[layer_idx] = []
            for i in range(layer_size):
                G.add_node(node_id, layer=layer_idx, position=(layer_idx, i))
                layer_positions[layer_idx].append(node_id)
                node_id += 1
        
        # 添加连接（突触）
        for from_node, to_node, weight in connections:
            G.add_edge(from_node, to_node, weight=weight)
        
        # 绘制网络
        plt.figure(figsize=(15, 10))
        
        # 计算节点位置
        pos = {}
        for layer_idx, nodes in layer_positions.items():
            for i, node in enumerate(nodes):
                pos[node] = (layer_idx, i)
        
        # 根据权重着色边
        edge_colors = []
        edge_weights = []
        for edge in G.edges():
            weight = G.edges[edge]['weight']
            edge_weights.append(abs(weight))
            if weight > 0:
                edge_colors.append('blue')
            else:
                edge_colors.append('red')
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, 
                              edge_color=edge_colors,
                              width=edge_weights,
                              alpha=0.6,
                              arrows=True,
                              arrowsize=10)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, 
                              node_color='lightblue',
                              node_size=500,
                              alpha=0.8)
        
        # 绘制标签
        labels = {node: f"N{node}" for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title("神经网络结构", fontsize=16, fontweight='bold')
        plt.xlabel("层")
        plt.ylabel("神经元")
        plt.grid(True)
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def visualize_gene_regulatory_network(self, genes: List[str],
                                        interactions: List[Tuple[str, str, str]],
                                        filename: str = "gene_regulatory_network.png"):
        """可视化基因调控网络"""
        G = nx.DiGraph()
        
        # 添加基因节点
        for gene in genes:
            G.add_node(gene)
        
        # 添加调控关系
        for source, target, interaction_type in interactions:
            G.add_edge(source, target, type=interaction_type)
        
        # 绘制网络
        plt.figure(figsize=(15, 10))
        
        # 计算布局
        pos = nx.spring_layout(G)
        
        # 根据调控类型着色边
        edge_colors = []
        for edge in G.edges():
            interaction_type = G.edges[edge]['type']
            if interaction_type == 'activation':
                edge_colors.append('green')
            elif interaction_type == 'inhibition':
                edge_colors.append('red')
            else:
                edge_colors.append('gray')
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, 
                              edge_color=edge_colors,
                              width=2,
                              alpha=0.6,
                              arrows=True,
                              arrowsize=20)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, 
                              node_color='lightyellow',
                              node_size=1000,
                              alpha=0.8)
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        plt.title("基因调控网络", fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', label='激活'),
            Patch(facecolor='red', label='抑制'),
            Patch(facecolor='gray', label='其他')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def visualize_protein_interaction_network(self, proteins: List[str],
                                            interactions: List[Tuple[str, str, float]],
                                            filename: str = "protein_interaction_network.png"):
        """可视化蛋白质相互作用网络"""
        G = nx.Graph()
        
        # 添加蛋白质节点
        for protein in proteins:
            G.add_node(protein)
        
        # 添加相互作用
        for protein1, protein2, confidence in interactions:
            G.add_edge(protein1, protein2, confidence=confidence)
        
        # 绘制网络
        plt.figure(figsize=(15, 10))
        
        # 计算布局
        pos = nx.spring_layout(G)
        
        # 根据置信度着色边
        edge_colors = []
        edge_weights = []
        for edge in G.edges():
            confidence = G.edges[edge]['confidence']
            edge_weights.append(confidence * 5)
            if confidence > 0.8:
                edge_colors.append('red')
            elif confidence > 0.6:
                edge_colors.append('orange')
            else:
                edge_colors.append('yellow')
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, 
                              edge_color=edge_colors,
                              width=edge_weights,
                              alpha=0.6)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, 
                              node_color='lightblue',
                              node_size=800,
                              alpha=0.8)
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        plt.title("蛋白质相互作用网络", fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', label='高置信度 (>0.8)'),
            Patch(facecolor='orange', label='中置信度 (0.6-0.8)'),
            Patch(facecolor='yellow', label='低置信度 (<0.6)')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def create_biological_network_mermaid(self, network_type: str,
                                        nodes: List[str],
                                        edges: List[Tuple[str, str]],
                                        filename: str = "biological_network.md"):
        """创建生物网络的Mermaid图"""
        mermaid_code = f"```mermaid\ngraph TD\n"
        mermaid_code += f"    title {network_type}\n\n"
        
        # 添加节点
        for node in nodes:
            mermaid_code += f"    {node}[{node}]\n"
        
        # 添加边
        for edge in edges:
            mermaid_code += f"    {edge[0]} --> {edge[1]}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def analyze_network_properties(self, graph: nx.Graph,
                                 network_type: str,
                                 filename: str = "network_properties.png"):
        """分析网络属性"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. 度分布
        degrees = [d for n, d in graph.degree()]
        axes[0, 0].hist(degrees, bins=20, alpha=0.7, color='blue')
        axes[0, 0].set_title(f'{network_type} - 度分布')
        axes[0, 0].set_xlabel('度数')
        axes[0, 0].set_ylabel('频次')
        
        # 2. 聚类系数分布
        clustering_coeffs = list(nx.clustering(graph).values())
        axes[0, 1].hist(clustering_coeffs, bins=20, alpha=0.7, color='green')
        axes[0, 1].set_title(f'{network_type} - 聚类系数分布')
        axes[0, 1].set_xlabel('聚类系数')
        axes[0, 1].set_ylabel('频次')
        
        # 3. 最短路径长度分布
        path_lengths = []
        for source in graph.nodes():
            for target in graph.nodes():
                if source != target:
                    try:
                        path_length = nx.shortest_path_length(graph, source, target)
                        path_lengths.append(path_length)
                    except nx.NetworkXNoPath:
                        continue
        
        axes[1, 0].hist(path_lengths, bins=20, alpha=0.7, color='red')
        axes[1, 0].set_title(f'{network_type} - 最短路径长度分布')
        axes[1, 0].set_xlabel('路径长度')
        axes[1, 0].set_ylabel('频次')
        
        # 4. 网络统计信息
        stats = {
            '节点数': graph.number_of_nodes(),
            '边数': graph.number_of_edges(),
            '平均度数': np.mean(degrees),
            '平均聚类系数': nx.average_clustering(graph),
            '平均路径长度': nx.average_shortest_path_length(graph),
            '网络密度': nx.density(graph)
        }
        
        y_pos = np.arange(len(stats))
        values = list(stats.values())
        axes[1, 1].barh(y_pos, values, alpha=0.7, color='purple')
        axes[1, 1].set_yticks(y_pos)
        axes[1, 1].set_yticklabels(list(stats.keys()))
        axes[1, 1].set_title(f'{network_type} - 网络统计')
        axes[1, 1].set_xlabel('数值')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def create_network_evolution_animation(self, evolution_steps: List[nx.Graph],
                                         filename: str = "network_evolution.gif"):
        """创建网络演化动画"""
        import matplotlib.animation as animation
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def animate(frame):
            ax.clear()
            graph = evolution_steps[frame]
            
            # 计算布局
            pos = nx.spring_layout(graph)
            
            # 绘制网络
            nx.draw_networkx_nodes(graph, pos, 
                                  node_color='lightblue',
                                  node_size=500,
                                  alpha=0.8)
            nx.draw_networkx_edges(graph, pos, 
                                  edge_color='gray',
                                  alpha=0.6,
                                  width=2)
            nx.draw_networkx_labels(graph, pos, font_size=8)
            
            ax.set_title(f'网络演化 - 步骤 {frame + 1}', 
                        fontsize=14, fontweight='bold')
            ax.axis('off')
        
        # 创建动画
        anim = animation.FuncAnimation(fig, animate, 
                                     frames=len(evolution_steps),
                                     interval=1000, 
                                     repeat=True)
        
        # 保存动画
        output_path = self.output_dir / filename
        anim.save(output_path, writer='pillow')
        plt.close()
        
        return str(output_path)

def main():
    """主函数 - 示例用法"""
    # 初始化生物网络可视化器
    visualizer = BiologicalNetworkVisualizer()
    
    # 创建神经网络可视化
    layers = [3, 4, 4, 2]  # 输入层、隐藏层1、隐藏层2、输出层
    connections = [
        (0, 3, 0.5), (0, 4, -0.3), (0, 5, 0.2), (0, 6, 0.1),
        (1, 3, 0.1), (1, 4, 0.7), (1, 5, -0.2), (1, 6, 0.4),
        (2, 3, -0.2), (2, 4, 0.3), (2, 5, 0.6), (2, 6, -0.1),
        (3, 7, 0.8), (3, 8, -0.3), (4, 7, 0.2), (4, 8, 0.9),
        (5, 7, -0.1), (5, 8, 0.4), (6, 7, 0.6), (6, 8, 0.1)
    ]
    visualizer.visualize_neural_network(layers, connections)
    
    # 创建基因调控网络可视化
    genes = ['GeneA', 'GeneB', 'GeneC', 'GeneD', 'GeneE']
    interactions = [
        ('GeneA', 'GeneB', 'activation'),
        ('GeneA', 'GeneC', 'inhibition'),
        ('GeneB', 'GeneD', 'activation'),
        ('GeneC', 'GeneD', 'inhibition'),
        ('GeneD', 'GeneE', 'activation'),
        ('GeneE', 'GeneA', 'inhibition')
    ]
    visualizer.visualize_gene_regulatory_network(genes, interactions)
    
    # 创建蛋白质相互作用网络可视化
    proteins = ['Protein1', 'Protein2', 'Protein3', 'Protein4', 'Protein5']
    interactions = [
        ('Protein1', 'Protein2', 0.9),
        ('Protein1', 'Protein3', 0.7),
        ('Protein2', 'Protein4', 0.8),
        ('Protein3', 'Protein4', 0.5),
        ('Protein4', 'Protein5', 0.9),
        ('Protein1', 'Protein5', 0.6)
    ]
    visualizer.visualize_protein_interaction_network(proteins, interactions)
    
    # 创建Mermaid图
    visualizer.create_biological_network_mermaid("基因调控网络", genes, 
                                               [(g1, g2) for g1, g2, _ in interactions])
    
    # 分析网络属性
    G = nx.Graph()
    for protein in proteins:
        G.add_node(protein)
    for p1, p2, conf in interactions:
        G.add_edge(p1, p2)
    visualizer.analyze_network_properties(G, "蛋白质相互作用网络")
    
    print("生物网络可视化完成！输出文件保存在 output/ 目录中。")

if __name__ == "__main__":
    main()
