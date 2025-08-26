#!/usr/bin/env python3
"""
网络拓扑动态演化工具
支持网络拓扑的动态演化、性能分析和优化可视化
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
import matplotlib.animation as animation
from pathlib import Path
import json

class TopologyAnimator:
    """网络拓扑动态演化器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def animate_topology_evolution(self, evolution_steps: List[nx.Graph],
                                 filename: str = "topology_evolution.gif",
                                 interval: int = 1000):
        """动画展示拓扑演化过程"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def animate(frame):
            ax.clear()
            graph = evolution_steps[frame]
            
            # 计算布局
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
            
            ax.set_title(f'网络拓扑演化 - 步骤 {frame + 1}', 
                        fontsize=14, fontweight='bold')
            ax.axis('off')
        
        # 创建动画
        anim = animation.FuncAnimation(fig, animate, 
                                     frames=len(evolution_steps),
                                     interval=interval, 
                                     repeat=True)
        
        # 保存动画
        output_path = self.output_dir / filename
        anim.save(output_path, writer='pillow')
        plt.close()
        
        return str(output_path)
    
    def visualize_small_world_evolution(self, n: int = 50, k: int = 4,
                                      p_values: List[float] = None,
                                      filename: str = "small_world_evolution.png"):
        """可视化小世界网络演化"""
        if p_values is None:
            p_values = [0, 0.1, 0.3, 0.5, 0.7, 1.0]
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, p in enumerate(p_values):
            # 生成小世界网络
            G = nx.watts_strogatz_graph(n, k, p)
            
            # 计算布局
            pos = nx.spring_layout(G)
            
            # 绘制网络
            nx.draw_networkx_nodes(G, pos, 
                                  node_color='lightblue',
                                  node_size=200,
                                  alpha=0.8,
                                  ax=axes[i])
            nx.draw_networkx_edges(G, pos, 
                                  edge_color='gray',
                                  alpha=0.6,
                                  width=1,
                                  ax=axes[i])
            
            # 计算网络特性
            avg_clustering = nx.average_clustering(G)
            avg_path_length = nx.average_shortest_path_length(G)
            
            axes[i].set_title(f'p = {p}\n聚类系数: {avg_clustering:.3f}\n平均路径长度: {avg_path_length:.3f}')
            axes[i].axis('off')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def visualize_scale_free_evolution(self, n: int = 100, m: int = 3,
                                     steps: int = 10,
                                     filename: str = "scale_free_evolution.gif"):
        """可视化无标度网络演化"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def animate(frame):
            ax.clear()
            
            # 生成当前步骤的网络
            current_n = n // steps * (frame + 1)
            G = nx.barabasi_albert_graph(current_n, m)
            
            # 计算布局
            pos = nx.spring_layout(G)
            
            # 根据度数着色
            degrees = [d for n, d in G.degree()]
            max_degree = max(degrees)
            node_colors = [plt.cm.viridis(d/max_degree) for d in degrees]
            
            # 绘制节点
            nx.draw_networkx_nodes(G, pos, 
                                  node_color=node_colors,
                                  node_size=[d*20 for d in degrees],
                                  alpha=0.8)
            
            # 绘制边
            nx.draw_networkx_edges(G, pos, 
                                  edge_color='gray',
                                  alpha=0.4,
                                  width=1)
            
            ax.set_title(f'无标度网络演化 - 节点数: {current_n}', 
                        fontsize=14, fontweight='bold')
            ax.axis('off')
        
        # 创建动画
        anim = animation.FuncAnimation(fig, animate, 
                                     frames=steps,
                                     interval=1000, 
                                     repeat=True)
        
        # 保存动画
        output_path = self.output_dir / filename
        anim.save(output_path, writer='pillow')
        plt.close()
        
        return str(output_path)
    
    def analyze_topology_performance(self, graph: nx.Graph,
                                   filename: str = "topology_performance.png"):
        """分析拓扑性能"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. 度分布
        degrees = [d for n, d in graph.degree()]
        axes[0, 0].hist(degrees, bins=20, alpha=0.7, color='blue')
        axes[0, 0].set_title('节点度分布')
        axes[0, 0].set_xlabel('度数')
        axes[0, 0].set_ylabel('频次')
        
        # 2. 聚类系数分布
        clustering_coeffs = list(nx.clustering(graph).values())
        axes[0, 1].hist(clustering_coeffs, bins=20, alpha=0.7, color='green')
        axes[0, 1].set_title('聚类系数分布')
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
        axes[1, 0].set_title('最短路径长度分布')
        axes[1, 0].set_xlabel('路径长度')
        axes[1, 0].set_ylabel('频次')
        
        # 4. 网络性能指标
        metrics = {
            '节点数': graph.number_of_nodes(),
            '边数': graph.number_of_edges(),
            '平均度数': np.mean(degrees),
            '平均聚类系数': nx.average_clustering(graph),
            '平均路径长度': nx.average_shortest_path_length(graph),
            '网络密度': nx.density(graph)
        }
        
        y_pos = np.arange(len(metrics))
        values = list(metrics.values())
        axes[1, 1].barh(y_pos, values, alpha=0.7, color='purple')
        axes[1, 1].set_yticks(y_pos)
        axes[1, 1].set_yticklabels(list(metrics.keys()))
        axes[1, 1].set_title('网络性能指标')
        axes[1, 1].set_xlabel('数值')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def create_topology_comparison(self, topologies: Dict[str, nx.Graph],
                                 filename: str = "topology_comparison.png"):
        """创建拓扑结构比较"""
        n_topologies = len(topologies)
        fig, axes = plt.subplots(2, (n_topologies + 1) // 2, figsize=(15, 10))
        axes = axes.flatten()
        
        for i, (name, graph) in enumerate(topologies.items()):
            if i >= len(axes):
                break
                
            # 计算布局
            pos = nx.spring_layout(graph)
            
            # 绘制网络
            nx.draw_networkx_nodes(graph, pos, 
                                  node_color='lightblue',
                                  node_size=300,
                                  alpha=0.8,
                                  ax=axes[i])
            nx.draw_networkx_edges(graph, pos, 
                                  edge_color='gray',
                                  alpha=0.6,
                                  width=1,
                                  ax=axes[i])
            
            # 计算网络特性
            avg_clustering = nx.average_clustering(graph)
            avg_path_length = nx.average_shortest_path_length(graph)
            density = nx.density(graph)
            
            axes[i].set_title(f'{name}\n聚类: {avg_clustering:.3f}\n路径: {avg_path_length:.3f}\n密度: {density:.3f}')
            axes[i].axis('off')
        
        # 隐藏多余的子图
        for i in range(n_topologies, len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def generate_topology_mermaid(self, graph: nx.Graph,
                                topology_type: str = "network",
                                filename: str = "topology_diagram.md"):
        """生成拓扑结构的Mermaid图"""
        mermaid_code = ""
        
        if topology_type == "network":
            mermaid_code = "graph TD\n"
            for edge in graph.edges():
                mermaid_code += f"    {edge[0]} --> {edge[1]}\n"
        
        elif topology_type == "flowchart":
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

def main():
    """主函数 - 示例用法"""
    # 初始化动画器
    animator = TopologyAnimator()
    
    # 创建小世界网络演化
    animator.visualize_small_world_evolution()
    
    # 创建无标度网络演化
    animator.visualize_scale_free_evolution()
    
    # 分析网络性能
    G = nx.watts_strogatz_graph(50, 4, 0.3)
    animator.analyze_topology_performance(G)
    
    # 创建拓扑比较
    topologies = {
        '随机网络': nx.erdos_renyi_graph(20, 0.3),
        '小世界网络': nx.watts_strogatz_graph(20, 4, 0.3),
        '无标度网络': nx.barabasi_albert_graph(20, 2)
    }
    animator.create_topology_comparison(topologies)
    
    # 生成Mermaid图
    animator.generate_topology_mermaid(G)
    
    print("网络拓扑动画完成！输出文件保存在 output/ 目录中。")

if __name__ == "__main__":
    main()
