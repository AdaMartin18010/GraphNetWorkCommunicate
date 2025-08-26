#!/usr/bin/env python3
"""
社会网络社区动画工具
支持社会网络社区演化、影响力传播等可视化
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
import matplotlib.animation as animation
from pathlib import Path
import json

class SocialCommunityAnimator:
    """社会网络社区动画器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def animate_community_evolution(self, evolution_steps: List[nx.Graph],
                                 communities: List[Dict],
                                 filename: str = "community_evolution.gif"):
        """动画展示社区演化过程"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def animate(frame):
            ax.clear()
            graph = evolution_steps[frame]
            community_info = communities[frame]
            
            # 计算布局
            pos = nx.spring_layout(graph)
            
            # 根据社区着色节点
            node_colors = []
            for node in graph.nodes():
                community_id = community_info.get(node, 0)
                node_colors.append(plt.cm.tab10(community_id % 10))
            
            # 绘制节点
            nx.draw_networkx_nodes(graph, pos, 
                                  node_color=node_colors,
                                  node_size=500,
                                  alpha=0.8)
            
            # 绘制边
            nx.draw_networkx_edges(graph, pos, 
                                  edge_color='gray',
                                  alpha=0.4,
                                  width=1)
            
            # 绘制标签
            nx.draw_networkx_labels(graph, pos, font_size=8)
            
            ax.set_title(f'社区演化 - 步骤 {frame + 1}', 
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
    
    def visualize_influence_spread(self, graph: nx.Graph,
                                initial_influencers: List[str],
                                spread_steps: List[Dict],
                                filename: str = "influence_spread.gif"):
        """可视化影响力传播过程"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def animate(frame):
            ax.clear()
            step_info = spread_steps[frame]
            
            # 计算布局
            pos = nx.spring_layout(graph)
            
            # 根据影响力状态着色节点
            node_colors = []
            for node in graph.nodes():
                if node in step_info.get('influenced', []):
                    node_colors.append('red')  # 已受影响
                elif node in step_info.get('influencers', []):
                    node_colors.append('blue')  # 影响者
                else:
                    node_colors.append('lightgray')  # 未受影响
            
            # 绘制节点
            nx.draw_networkx_nodes(graph, pos, 
                                  node_color=node_colors,
                                  node_size=500,
                                  alpha=0.8)
            
            # 绘制边
            nx.draw_networkx_edges(graph, pos, 
                                  edge_color='gray',
                                  alpha=0.4,
                                  width=1)
            
            # 绘制标签
            nx.draw_networkx_labels(graph, pos, font_size=8)
            
            ax.set_title(f'影响力传播 - 步骤 {frame + 1}', 
                        fontsize=14, fontweight='bold')
            ax.axis('off')
        
        # 创建动画
        anim = animation.FuncAnimation(fig, animate, 
                                     frames=len(spread_steps),
                                     interval=1000, 
                                     repeat=True)
        
        # 保存动画
        output_path = self.output_dir / filename
        anim.save(output_path, writer='pillow')
        plt.close()
        
        return str(output_path)
    
    def create_social_network_diagram(self, nodes: List[str],
                                   edges: List[Tuple[str, str]],
                                   communities: Dict[str, int],
                                   filename: str = "social_network.md"):
        """创建社会网络Mermaid图"""
        mermaid_code = "```mermaid\ngraph TD\n"
        mermaid_code += "    title 社会网络结构\n\n"
        
        # 按社区分组节点
        community_groups = {}
        for node, community_id in communities.items():
            if community_id not in community_groups:
                community_groups[community_id] = []
            community_groups[community_id].append(node)
        
        # 添加社区子图
        for community_id, nodes_in_community in community_groups.items():
            mermaid_code += f"    subgraph Community{community_id}\n"
            for node in nodes_in_community:
                mermaid_code += f"        {node}[{node}]\n"
            mermaid_code += "    end\n"
        
        # 添加跨社区边
        for edge in edges:
            mermaid_code += f"    {edge[0]} --> {edge[1]}\n"
        
        mermaid_code += "```\n"
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def analyze_social_metrics(self, graph: nx.Graph,
                             filename: str = "social_metrics.png"):
        """分析社会网络指标"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. 度中心性分布
        degree_centrality = nx.degree_centrality(graph)
        centrality_values = list(degree_centrality.values())
        axes[0, 0].hist(centrality_values, bins=20, alpha=0.7, color='blue')
        axes[0, 0].set_title('度中心性分布')
        axes[0, 0].set_xlabel('度中心性')
        axes[0, 0].set_ylabel('频次')
        
        # 2. 介数中心性分布
        betweenness_centrality = nx.betweenness_centrality(graph)
        betweenness_values = list(betweenness_centrality.values())
        axes[0, 1].hist(betweenness_values, bins=20, alpha=0.7, color='green')
        axes[0, 1].set_title('介数中心性分布')
        axes[0, 1].set_xlabel('介数中心性')
        axes[0, 1].set_ylabel('频次')
        
        # 3. 接近中心性分布
        closeness_centrality = nx.closeness_centrality(graph)
        closeness_values = list(closeness_centrality.values())
        axes[1, 0].hist(closeness_values, bins=20, alpha=0.7, color='red')
        axes[1, 0].set_title('接近中心性分布')
        axes[1, 0].set_xlabel('接近中心性')
        axes[1, 0].set_ylabel('频次')
        
        # 4. 网络统计信息
        stats = {
            '节点数': graph.number_of_nodes(),
            '边数': graph.number_of_edges(),
            '平均度数': np.mean([d for n, d in graph.degree()]),
            '平均聚类系数': nx.average_clustering(graph),
            '平均路径长度': nx.average_shortest_path_length(graph),
            '网络密度': nx.density(graph)
        }
        
        y_pos = np.arange(len(stats))
        values = list(stats.values())
        axes[1, 1].barh(y_pos, values, alpha=0.7, color='purple')
        axes[1, 1].set_yticks(y_pos)
        axes[1, 1].set_yticklabels(list(stats.keys()))
        axes[1, 1].set_title('社会网络统计')
        axes[1, 1].set_xlabel('数值')
        
        plt.tight_layout()
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def create_opinion_diffusion_diagram(self, filename: str = "opinion_diffusion.md"):
        """创建意见传播图"""
        mermaid_code = """
```mermaid
graph TD
    subgraph 初始状态
        A1[用户A - 支持]
        B1[用户B - 中立]
        C1[用户C - 反对]
        D1[用户D - 中立]
    end
    
    subgraph 传播过程
        A2[用户A - 支持]
        B2[用户B - 支持]
        C2[用户C - 反对]
        D2[用户D - 支持]
    end
    
    subgraph 最终状态
        A3[用户A - 支持]
        B3[用户B - 支持]
        C3[用户C - 支持]
        D3[用户D - 支持]
    end
    
    A1 --> A2
    B1 --> B2
    C1 --> C2
    D1 --> D2
    
    A2 --> A3
    B2 --> B3
    C2 --> C3
    D2 --> D3
    
    style A1 fill:#90EE90
    style A2 fill:#90EE90
    style A3 fill:#90EE90
    style B1 fill:#FFE4B5
    style B2 fill:#90EE90
    style B3 fill:#90EE90
    style C1 fill:#FFB6C1
    style C2 fill:#FFB6C1
    style C3 fill:#90EE90
    style D1 fill:#FFE4B5
    style D2 fill:#90EE90
    style D3 fill:#90EE90
```
"""
        
        # 保存Mermaid代码
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        return str(output_path)
    
    def create_community_detection_visualization(self, graph: nx.Graph,
                                              communities: Dict[str, int],
                                              filename: str = "community_detection.png"):
        """可视化社区检测结果"""
        plt.figure(figsize=(15, 10))
        
        # 计算布局
        pos = nx.spring_layout(graph)
        
        # 根据社区着色节点
        node_colors = []
        for node in graph.nodes():
            community_id = communities.get(node, 0)
            node_colors.append(plt.cm.tab10(community_id % 10))
        
        # 绘制节点
        nx.draw_networkx_nodes(graph, pos, 
                              node_color=node_colors,
                              node_size=800,
                              alpha=0.8)
        
        # 绘制边
        nx.draw_networkx_edges(graph, pos, 
                              edge_color='gray',
                              alpha=0.4,
                              width=1)
        
        # 绘制标签
        nx.draw_networkx_labels(graph, pos, font_size=10)
        
        plt.title("社区检测结果", fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # 添加图例
        unique_communities = set(communities.values())
        legend_elements = []
        for community_id in unique_communities:
            color = plt.cm.tab10(community_id % 10)
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=color, markersize=10, 
                                            label=f'社区 {community_id}'))
        plt.legend(handles=legend_elements, loc='upper right')
        
        # 保存图片
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)

def main():
    """主函数 - 示例用法"""
    # 初始化社会网络社区动画器
    animator = SocialCommunityAnimator()
    
    # 创建示例社会网络
    G = nx.karate_club_graph()
    
    # 创建社区演化步骤
    evolution_steps = []
    communities = []
    
    # 模拟社区演化过程
    for step in range(5):
        # 复制图并添加一些随机边
        step_graph = G.copy()
        if step > 0:
            # 添加一些新连接
            for _ in range(step * 2):
                nodes = list(step_graph.nodes())
                if len(nodes) >= 2:
                    n1, n2 = np.random.choice(nodes, 2, replace=False)
                    if not step_graph.has_edge(n1, n2):
                        step_graph.add_edge(n1, n2)
        
        evolution_steps.append(step_graph)
        
        # 模拟社区分配
        community_assignments = {}
        for node in step_graph.nodes():
            # 简单的社区分配逻辑
            if node < 10:
                community_assignments[node] = 0
            elif node < 20:
                community_assignments[node] = 1
            else:
                community_assignments[node] = 2
        communities.append(community_assignments)
    
    # 创建社区演化动画
    animator.animate_community_evolution(evolution_steps, communities)
    
    # 创建影响力传播动画
    initial_influencers = [0, 5]
    spread_steps = []
    
    for step in range(5):
        step_info = {
            'influencers': initial_influencers,
            'influenced': list(range(step * 3, min(step * 3 + 3, len(G.nodes()))))
        }
        spread_steps.append(step_info)
    
    animator.visualize_influence_spread(G, initial_influencers, spread_steps)
    
    # 创建社会网络图
    nodes = [str(i) for i in range(len(G.nodes()))]
    edges = [(str(u), str(v)) for u, v in G.edges()]
    communities_dict = {str(i): i // 10 for i in range(len(G.nodes()))}
    animator.create_social_network_diagram(nodes, edges, communities_dict)
    
    # 分析社会网络指标
    animator.analyze_social_metrics(G)
    
    # 创建意见传播图
    animator.create_opinion_diffusion_diagram()
    
    # 创建社区检测可视化
    animator.create_community_detection_visualization(G, communities_dict)
    
    print("社会网络社区动画完成！输出文件保存在 output/ 目录中。")

if __name__ == "__main__":
    main()
