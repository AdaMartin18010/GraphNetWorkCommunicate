#!/usr/bin/env python3
"""
图论基础可视化工具
支持图结构、算法过程、谱分析等可视化
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
import seaborn as sns
from pathlib import Path
import json

class GraphVisualizer:
    """图论基础可视化器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def visualize_graph_structure(self, graph: nx.Graph, 
                                layout: str = 'spring',
                                title: str = "图结构可视化",
                                filename: str = "graph_structure.png"):
        """可视化图结构"""
        plt.figure(figsize=(12, 8))
        
        # 选择布局算法
        if layout == 'spring':
            pos = nx.spring_layout(graph)
        elif layout == 'circular':
            pos = nx.circular_layout(graph)
        elif layout == 'random':
            pos = nx.random_layout(graph)
        elif layout == 'shell':
            pos = nx.shell_layout(graph)
        else:
            pos = nx.spring_layout(graph)
        
        # 绘制节点
        nx.draw_networkx_nodes(graph, pos, 
                              node_color='lightblue',
                              node_size=500,
                              alpha=0.8)
        
        # 绘制边
        nx.draw_networkx_edges(graph, pos, 
                              edge_color='gray',
                              alpha=0.6,
                              width=2)
        
        # 绘制标签
        nx.draw_networkx_labels(graph, pos, 
                               font_size=10,
                               font_weight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def visualize_algorithm_process(self, graph: nx.Graph, 
                                  algorithm: str,
                                  steps: List[Dict],
                                  filename: str = "algorithm_process.gif"):
        """可视化算法执行过程"""
        import matplotlib.animation as animation
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def animate(frame):
            ax.clear()
            step = steps[frame]
            
            # 绘制图结构
            pos = nx.spring_layout(graph)
            
            # 根据步骤状态着色
            node_colors = []
            for node in graph.nodes():
                if node in step.get('visited', []):
                    node_colors.append('red')
                elif node in step.get('current', []):
                    node_colors.append('yellow')
                else:
                    node_colors.append('lightblue')
            
            nx.draw_networkx_nodes(graph, pos, 
                                  node_color=node_colors,
                                  node_size=500)
            nx.draw_networkx_edges(graph, pos, alpha=0.6)
            nx.draw_networkx_labels(graph, pos)
            
            ax.set_title(f"{algorithm} - 步骤 {frame + 1}", 
                        fontsize=14, fontweight='bold')
            ax.axis('off')
        
        # 创建动画
        anim = animation.FuncAnimation(fig, animate, 
                                     frames=len(steps),
                                     interval=1000, 
                                     repeat=True)
        
        # 保存动画
        output_path = self.output_dir / filename
        anim.save(output_path, writer='pillow')
        plt.close()
        
        return str(output_path)
    
    def visualize_spectral_analysis(self, graph: nx.Graph,
                                  filename: str = "spectral_analysis.png"):
        """可视化谱分析"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 计算拉普拉斯矩阵
        L = nx.laplacian_matrix(graph).toarray()
        eigenvalues = np.linalg.eigvals(L)
        
        # 1. 特征值分布
        axes[0, 0].hist(eigenvalues.real, bins=20, alpha=0.7, color='blue')
        axes[0, 0].set_title('拉普拉斯矩阵特征值分布')
        axes[0, 0].set_xlabel('特征值')
        axes[0, 0].set_ylabel('频次')
        
        # 2. 度分布
        degrees = [d for n, d in graph.degree()]
        axes[0, 1].hist(degrees, bins=20, alpha=0.7, color='green')
        axes[0, 1].set_title('节点度分布')
        axes[0, 1].set_xlabel('度数')
        axes[0, 1].set_ylabel('频次')
        
        # 3. 聚类系数分布
        clustering_coeffs = list(nx.clustering(graph).values())
        axes[1, 0].hist(clustering_coeffs, bins=20, alpha=0.7, color='red')
        axes[1, 0].set_title('聚类系数分布')
        axes[1, 0].set_xlabel('聚类系数')
        axes[1, 0].set_ylabel('频次')
        
        # 4. 特征向量可视化
        eigenvector = nx.fiedler_vector(graph)
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, 
                              node_color=eigenvector,
                              cmap=plt.cm.RdYlBu,
                              node_size=300,
                              ax=axes[1, 1])
        nx.draw_networkx_edges(graph, pos, alpha=0.6, ax=axes[1, 1])
        axes[1, 1].set_title('Fiedler向量可视化')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def generate_mermaid_diagram(self, graph: nx.Graph,
                               diagram_type: str = "graph",
                               filename: str = "graph_diagram.md"):
        """生成Mermaid图表"""
        mermaid_code = ""
        
        if diagram_type == "graph":
            mermaid_code = "graph TD\n"
            for edge in graph.edges():
                mermaid_code += f"    {edge[0]} --> {edge[1]}\n"
        
        elif diagram_type == "flowchart":
            mermaid_code = "flowchart TD\n"
            for node in graph.nodes():
                mermaid_code += f"    {node}[{node}]\n"
            for edge in graph.edges():
                mermaid_code += f"    {edge[0]} --> {edge[1]}\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"```mermaid\n{mermaid_code}```\n")
        
        return str(output_path)
    
    def create_heatmap(self, matrix: np.ndarray,
                      title: str = "邻接矩阵热力图",
                      filename: str = "adjacency_heatmap.png"):
        """创建热力图"""
        plt.figure(figsize=(10, 8))
        
        sns.heatmap(matrix, 
                   annot=True, 
                   cmap='Blues',
                   square=True,
                   cbar_kws={'label': '权重'})
        
        plt.title(title, fontsize=16, fontweight='bold')
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)

def main():
    """主函数 - 示例用法"""
    # 创建示例图
    G = nx.karate_club_graph()
    
    # 初始化可视化器
    visualizer = GraphVisualizer()
    
    # 可视化图结构
    visualizer.visualize_graph_structure(G, title="Karate Club网络")
    
    # 可视化谱分析
    visualizer.visualize_spectral_analysis(G)
    
    # 生成Mermaid图表
    visualizer.generate_mermaid_diagram(G)
    
    # 创建邻接矩阵热力图
    adj_matrix = nx.adjacency_matrix(G).toarray()
    visualizer.create_heatmap(adj_matrix)
    
    print("图论可视化完成！输出文件保存在 output/ 目录中。")

if __name__ == "__main__":
    main()
