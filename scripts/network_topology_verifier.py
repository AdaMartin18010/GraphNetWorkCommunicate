#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络拓扑性质验证器 / Network Topology Property Verifier

功能 / Features:
- 验证网络拓扑的基本性质
- 计算拓扑性能指标
- 提供形式化验证支持
- 生成验证报告

作者 / Author: GraphNetWorkCommunicate Project
日期 / Date: December 2024
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import json
import time
from pathlib import Path

class NetworkTopologyVerifier:
    """网络拓扑性质验证器 / Network Topology Property Verifier"""
    
    def __init__(self):
        """初始化验证器"""
        self.verification_results = {}
        self.topology_properties = {}
    
    def verify_connectivity(self, G: nx.Graph) -> Dict[str, Any]:
        """
        验证网络连通性 / Verify Network Connectivity
        
        参数 / Parameters:
            G: 网络图 / Network graph
            
        返回 / Returns:
            连通性验证结果 / Connectivity verification result
        """
        # 基本连通性
        is_connected = nx.is_connected(G)
        
        # 连通度（最小割）
        connectivity = nx.node_connectivity(G)
        
        # 边连通度
        edge_connectivity = nx.edge_connectivity(G)
        
        # 连通分量
        connected_components = list(nx.connected_components(G))
        num_components = len(connected_components)
        
        result = {
            'is_connected': is_connected,
            'connectivity': connectivity,
            'edge_connectivity': edge_connectivity,
            'num_components': num_components,
            'components': [list(comp) for comp in connected_components]
        }
        
        return result
    
    def verify_redundancy(self, G: nx.Graph) -> Dict[str, Any]:
        """
        验证网络冗余性 / Verify Network Redundancy
        
        参数 / Parameters:
            G: 网络图 / Network graph
            
        返回 / Returns:
            冗余性验证结果 / Redundancy verification result
        """
        n = G.number_of_nodes()
        m = G.number_of_edges()
        
        # 最小生成树边数
        mst_edges = n - 1
        
        # 冗余性计算
        redundancy = (m - mst_edges) / mst_edges if mst_edges > 0 else 0
        
        # 双连通性
        is_biconnected = nx.is_biconnected(G)
        
        # 割点数量
        cut_vertices = list(nx.articulation_points(G))
        num_cut_vertices = len(cut_vertices)
        
        # 桥的数量
        bridges = list(nx.bridges(G))
        num_bridges = len(bridges)
        
        result = {
            'redundancy_ratio': redundancy,
            'is_biconnected': is_biconnected,
            'num_cut_vertices': num_cut_vertices,
            'cut_vertices': cut_vertices,
            'num_bridges': num_bridges,
            'bridges': bridges
        }
        
        return result
    
    def verify_scalability(self, G: nx.Graph) -> Dict[str, Any]:
        """
        验证网络可扩展性 / Verify Network Scalability
        
        参数 / Parameters:
            G: 网络图 / Network graph
            
        返回 / Returns:
            可扩展性验证结果 / Scalability verification result
        """
        degrees = dict(G.degree())
        
        # 最大度数
        max_degree = max(degrees.values())
        
        # 平均度数
        avg_degree = np.mean(list(degrees.values()))
        
        # 可扩展性指标
        scalability = max_degree / avg_degree if avg_degree > 0 else 0
        
        # 度数分布
        degree_distribution = {}
        for degree in degrees.values():
            degree_distribution[degree] = degree_distribution.get(degree, 0) + 1
        
        # 度数方差
        degree_variance = np.var(list(degrees.values()))
        
        result = {
            'max_degree': max_degree,
            'avg_degree': avg_degree,
            'scalability_index': scalability,
            'degree_variance': degree_variance,
            'degree_distribution': degree_distribution
        }
        
        return result
    
    def verify_efficiency(self, G: nx.Graph) -> Dict[str, Any]:
        """
        验证网络效率性 / Verify Network Efficiency
        
        参数 / Parameters:
            G: 网络图 / Network graph
            
        返回 / Returns:
            效率性验证结果 / Efficiency verification result
        """
        # 平均路径长度
        if nx.is_connected(G):
            avg_path_length = nx.average_shortest_path_length(G)
        else:
            # 对于非连通图，计算连通分量内的平均路径长度
            path_lengths = []
            for component in nx.connected_components(G):
                subgraph = G.subgraph(component)
                if len(component) > 1:
                    path_lengths.append(nx.average_shortest_path_length(subgraph))
            avg_path_length = np.mean(path_lengths) if path_lengths else 0
        
        # 网络直径
        diameter = nx.diameter(G) if nx.is_connected(G) else float('inf')
        
        # 网络半径
        radius = nx.radius(G) if nx.is_connected(G) else float('inf')
        
        # 效率性指标
        efficiency = 1 / avg_path_length if avg_path_length > 0 else 0
        
        # 聚类系数
        clustering_coefficient = nx.average_clustering(G)
        
        result = {
            'avg_path_length': avg_path_length,
            'diameter': diameter,
            'radius': radius,
            'efficiency_index': efficiency,
            'clustering_coefficient': clustering_coefficient
        }
        
        return result
    
    def verify_topology_theorems(self, G: nx.Graph) -> Dict[str, Any]:
        """
        验证拓扑定理 / Verify Topology Theorems
        
        参数 / Parameters:
            G: 网络图 / Network graph
            
        返回 / Returns:
            定理验证结果 / Theorem verification result
        """
        results = {}
        
        # 验证握手定理
        total_degree = sum(dict(G.degree()).values())
        edge_count = G.number_of_edges()
        handshaking_lemma = total_degree == 2 * edge_count
        results['handshaking_lemma'] = {
            'holds': handshaking_lemma,
            'total_degree': total_degree,
            'edge_count': edge_count,
            'expected': 2 * edge_count
        }
        
        # 验证连通性上界
        connectivity = nx.node_connectivity(G)
        min_degree = min(dict(G.degree()).values())
        connectivity_bound = connectivity <= min_degree
        results['connectivity_bound'] = {
            'holds': connectivity_bound,
            'connectivity': connectivity,
            'min_degree': min_degree
        }
        
        # 验证冗余性非负性
        n = G.number_of_nodes()
        m = G.number_of_edges()
        mst_edges = n - 1
        redundancy = (m - mst_edges) / mst_edges if mst_edges > 0 else 0
        redundancy_nonnegative = redundancy >= 0
        results['redundancy_nonnegative'] = {
            'holds': redundancy_nonnegative,
            'redundancy': redundancy
        }
        
        return results
    
    def analyze_topology_type(self, G: nx.Graph) -> Dict[str, Any]:
        """
        分析拓扑类型 / Analyze Topology Type
        
        参数 / Parameters:
            G: 网络图 / Network graph
            
        返回 / Returns:
            拓扑类型分析结果 / Topology type analysis result
        """
        n = G.number_of_nodes()
        m = G.number_of_edges()
        degrees = dict(G.degree())
        
        # 检查是否为星形拓扑
        is_star = False
        if m == n - 1:  # 最小边数
            max_deg = max(degrees.values())
            min_deg = min(degrees.values())
            if max_deg == n - 1 and min_deg == 1:
                is_star = True
        
        # 检查是否为总线拓扑（路径图）
        is_bus = False
        if m == n - 1:
            degree_counts = {}
            for degree in degrees.values():
                degree_counts[degree] = degree_counts.get(degree, 0) + 1
            if degree_counts.get(1, 0) == 2 and degree_counts.get(2, 0) == n - 2:
                is_bus = True
        
        # 检查是否为环形拓扑
        is_ring = False
        if m == n and all(degree == 2 for degree in degrees.values()):
            is_ring = True
        
        # 检查是否为完全图
        is_complete = False
        if m == n * (n - 1) // 2:
            is_complete = True
        
        # 检查是否为树
        is_tree = False
        if m == n - 1 and nx.is_connected(G):
            is_tree = True
        
        result = {
            'is_star': is_star,
            'is_bus': is_bus,
            'is_ring': is_ring,
            'is_complete': is_complete,
            'is_tree': is_tree,
            'topology_type': self._determine_topology_type(is_star, is_bus, is_ring, is_complete, is_tree)
        }
        
        return result
    
    def _determine_topology_type(self, is_star, is_bus, is_ring, is_complete, is_tree):
        """确定拓扑类型"""
        if is_complete:
            return "Complete Graph"
        elif is_star:
            return "Star Topology"
        elif is_bus:
            return "Bus Topology"
        elif is_ring:
            return "Ring Topology"
        elif is_tree:
            return "Tree Topology"
        else:
            return "General Topology"
    
    def generate_test_topologies(self) -> Dict[str, nx.Graph]:
        """
        生成测试拓扑 / Generate Test Topologies
        
        返回 / Returns:
            测试拓扑字典 / Test topologies dictionary
        """
        topologies = {}
        
        # 星形拓扑
        star = nx.star_graph(5)
        topologies['star'] = star
        
        # 路径图（总线拓扑）
        path = nx.path_graph(6)
        topologies['bus'] = path
        
        # 环形拓扑
        cycle = nx.cycle_graph(6)
        topologies['ring'] = cycle
        
        # 完全图
        complete = nx.complete_graph(5)
        topologies['complete'] = complete
        
        # 随机图
        random_graph = nx.erdos_renyi_graph(10, 0.3)
        topologies['random'] = random_graph
        
        # 小世界网络
        small_world = nx.watts_strogatz_graph(10, 4, 0.3)
        topologies['small_world'] = small_world
        
        return topologies
    
    def run_comprehensive_verification(self) -> Dict[str, Any]:
        """
        运行综合验证 / Run Comprehensive Verification
        
        返回 / Returns:
            综合验证结果 / Comprehensive verification result
        """
        print("🚀 开始网络拓扑综合验证 / Starting Network Topology Comprehensive Verification")
        print("=" * 70)
        
        topologies = self.generate_test_topologies()
        results = {}
        
        for name, G in topologies.items():
            print(f"\n📋 验证拓扑: {name}")
            print(f"   节点数: {G.number_of_nodes()}, 边数: {G.number_of_edges()}")
            
            # 运行所有验证
            connectivity_result = self.verify_connectivity(G)
            redundancy_result = self.verify_redundancy(G)
            scalability_result = self.verify_scalability(G)
            efficiency_result = self.verify_efficiency(G)
            theorem_result = self.verify_topology_theorems(G)
            type_result = self.analyze_topology_type(G)
            
            # 汇总结果
            topology_result = {
                'connectivity': connectivity_result,
                'redundancy': redundancy_result,
                'scalability': scalability_result,
                'efficiency': efficiency_result,
                'theorems': theorem_result,
                'type': type_result
            }
            
            results[name] = topology_result
            
            # 显示关键结果
            print(f"   连通性: {connectivity_result['is_connected']}")
            print(f"   连通度: {connectivity_result['connectivity']}")
            print(f"   冗余性: {redundancy_result['redundancy_ratio']:.3f}")
            print(f"   效率性: {efficiency_result['efficiency_index']:.3f}")
            print(f"   拓扑类型: {type_result['topology_type']}")
        
        # 生成摘要报告
        summary = self.generate_summary_report(results)
        
        print("\n" + "=" * 70)
        print("📊 验证摘要 / Verification Summary")
        print("=" * 70)
        for name, result in results.items():
            print(f"{name}: {result['type']['topology_type']}")
        
        return results
    
    def generate_summary_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成摘要报告 / Generate Summary Report
        
        参数 / Parameters:
            results: 验证结果 / Verification results
            
        返回 / Returns:
            摘要报告 / Summary report
        """
        summary = {
            'total_topologies': len(results),
            'verification_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'topology_types': {},
            'property_statistics': {}
        }
        
        # 统计拓扑类型
        for name, result in results.items():
            topology_type = result['type']['topology_type']
            summary['topology_types'][topology_type] = summary['topology_types'].get(topology_type, 0) + 1
        
        # 统计性质
        properties = ['connectivity', 'redundancy_ratio', 'efficiency_index']
        for prop in properties:
            values = []
            for result in results.values():
                if prop == 'connectivity':
                    values.append(result['connectivity']['connectivity'])
                elif prop == 'redundancy_ratio':
                    values.append(result['redundancy']['redundancy_ratio'])
                elif prop == 'efficiency_index':
                    values.append(result['efficiency']['efficiency_index'])
            
            if values:
                summary['property_statistics'][prop] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values)
                }
        
        return summary
    
    def visualize_topology(self, G: nx.Graph, title: str = "Network Topology"):
        """
        可视化拓扑 / Visualize Topology
        
        参数 / Parameters:
            G: 网络图 / Network graph
            title: 标题 / Title
        """
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=500)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, edge_color='gray')
        
        # 添加标签
        nx.draw_networkx_labels(G, pos)
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def main():
    """主函数 / Main Function"""
    print("🎯 网络拓扑性质验证器 / Network Topology Property Verifier")
    print("=" * 70)
    
    # 创建验证器
    verifier = NetworkTopologyVerifier()
    
    # 运行综合验证
    results = verifier.run_comprehensive_verification()
    
    # 保存结果
    with open('network_topology_verification_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 验证报告已保存到: network_topology_verification_report.json")
    
    # 可视化示例
    print("\n🎨 可视化示例 / Visualization Example")
    topologies = verifier.generate_test_topologies()
    verifier.visualize_topology(topologies['star'], "Star Topology Example")
    
    print("\n✅ 验证完成！/ Verification Complete!")

if __name__ == "__main__":
    main()
