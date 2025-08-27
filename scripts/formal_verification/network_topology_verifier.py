#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络拓扑形式化验证器 / Network Topology Formal Verifier

功能 / Features:
- 验证网络拓扑基本定理
- 自动生成测试用例
- 提供形式化证明支持
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
    """网络拓扑验证器 / Network Topology Verifier"""
    
    def __init__(self):
        """初始化验证器"""
        self.test_results = []
        self.verification_stats = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'verification_time': 0
        }
    
    def verify_topology_properties(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        验证网络拓扑性质 / Verify Network Topology Properties
        
        参数 / Parameters:
            graph: 待验证的网络 / Network to verify
            
        返回 / Returns:
            验证结果字典 / Verification result dictionary
        """
        start_time = time.time()
        
        # 计算基本性质
        n = graph.number_of_nodes()
        m = graph.number_of_edges()
        
        # 连通性验证
        connectivity = nx.node_connectivity(graph) if n > 1 else 0
        min_degree = min(dict(graph.degree()).values()) if n > 0 else 0
        connectivity_bound = connectivity <= min_degree
        
        # 冗余性验证
        mst_edges = n - 1 if nx.is_connected(graph) else 0
        redundancy = (m - mst_edges) / mst_edges if mst_edges > 0 else 0
        redundancy_nonnegative = redundancy >= 0
        
        # 可扩展性验证
        degrees = dict(graph.degree())
        max_degree = max(degrees.values()) if degrees else 0
        avg_degree = sum(degrees.values()) / len(degrees) if degrees else 0
        scalability = max_degree / avg_degree if avg_degree > 0 else 0
        
        # 效率性验证
        if nx.is_connected(graph) and n > 1:
            avg_path_length = nx.average_shortest_path_length(graph)
            efficiency = 1 / avg_path_length
            efficiency_bound = efficiency <= 1
        else:
            efficiency = 0
            efficiency_bound = True
        
        verification_time = time.time() - start_time
        
        result = {
            'graph_info': {
                'nodes': list(graph.nodes()),
                'edges': list(graph.edges()),
                'num_nodes': n,
                'num_edges': m
            },
            'topology_properties': {
                'connectivity': connectivity,
                'min_degree': min_degree,
                'connectivity_bound': connectivity_bound,
                'redundancy': redundancy,
                'redundancy_nonnegative': redundancy_nonnegative,
                'scalability': scalability,
                'efficiency': efficiency,
                'efficiency_bound': efficiency_bound
            },
            'verification_result': {
                'all_properties_hold': (connectivity_bound and 
                                      redundancy_nonnegative and 
                                      efficiency_bound),
                'verification_time': verification_time
            }
        }
        
        return result
    
    def verify_small_world_properties(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        验证小世界网络性质 / Verify Small World Network Properties
        
        参数 / Parameters:
            graph: 待验证的网络 / Network to verify
            
        返回 / Returns:
            验证结果字典 / Verification result dictionary
        """
        start_time = time.time()
        
        n = graph.number_of_nodes()
        
        if n < 3:
            return {
                'is_small_world': False,
                'reason': 'Network too small',
                'verification_time': time.time() - start_time
            }
        
        # 计算聚类系数
        clustering_coeff = nx.average_clustering(graph)
        
        # 计算平均路径长度
        if nx.is_connected(graph):
            avg_path_length = nx.average_shortest_path_length(graph)
        else:
            avg_path_length = float('inf')
        
        # 生成随机图进行比较
        random_graph = nx.erdos_renyi_graph(n, nx.density(graph))
        random_clustering = nx.average_clustering(random_graph)
        random_path_length = nx.average_shortest_path_length(random_graph) if nx.is_connected(random_graph) else float('inf')
        
        # 小世界网络判断标准
        high_clustering = clustering_coeff > random_clustering
        short_path = avg_path_length < random_path_length * 1.5  # 允许一定的误差
        
        is_small_world = high_clustering and short_path and nx.is_connected(graph)
        
        verification_time = time.time() - start_time
        
        result = {
            'small_world_properties': {
                'clustering_coefficient': clustering_coeff,
                'random_clustering': random_clustering,
                'high_clustering': high_clustering,
                'avg_path_length': avg_path_length,
                'random_path_length': random_path_length,
                'short_path': short_path,
                'is_connected': nx.is_connected(graph)
            },
            'verification_result': {
                'is_small_world': is_small_world,
                'verification_time': verification_time
            }
        }
        
        return result
    
    def verify_scale_free_properties(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        验证无标度网络性质 / Verify Scale-Free Network Properties
        
        参数 / Parameters:
            graph: 待验证的网络 / Network to verify
            
        返回 / Returns:
            验证结果字典 / Verification result dictionary
        """
        start_time = time.time()
        
        degrees = dict(graph.degree())
        degree_values = list(degrees.values())
        
        if len(degree_values) < 10:
            return {
                'is_scale_free': False,
                'reason': 'Network too small for reliable analysis',
                'verification_time': time.time() - start_time
            }
        
        # 计算度分布
        degree_counts = {}
        for d in degree_values:
            degree_counts[d] = degree_counts.get(d, 0) + 1
        
        # 计算幂律指数（简化方法）
        log_degrees = [np.log(d) for d in degree_counts.keys() if d > 0]
        log_counts = [np.log(degree_counts[d]) for d in degree_counts.keys() if d > 0]
        
        if len(log_degrees) < 3:
            return {
                'is_scale_free': False,
                'reason': 'Insufficient degree diversity',
                'verification_time': time.time() - start_time
            }
        
        # 线性拟合
        try:
            coeffs = np.polyfit(log_degrees, log_counts, 1)
            gamma = -coeffs[0]  # 幂律指数
            
            # 判断是否为幂律分布
            is_power_law = 2 < gamma < 4  # 典型的无标度网络幂律指数范围
            
            # 计算拟合优度
            predicted = np.polyval(coeffs, log_degrees)
            r_squared = 1 - np.sum((log_counts - predicted) ** 2) / np.sum((log_counts - np.mean(log_counts)) ** 2)
            
            is_scale_free = is_power_law and r_squared > 0.7
            
        except:
            is_scale_free = False
            gamma = 0
            r_squared = 0
        
        verification_time = time.time() - start_time
        
        result = {
            'scale_free_properties': {
                'gamma': gamma,
                'r_squared': r_squared,
                'is_power_law': is_power_law if 'is_power_law' in locals() else False,
                'degree_distribution': degree_counts
            },
            'verification_result': {
                'is_scale_free': is_scale_free,
                'verification_time': verification_time
            }
        }
        
        return result
    
    def generate_test_cases(self) -> List[Tuple[str, nx.Graph]]:
        """
        生成测试用例 / Generate Test Cases
        
        返回 / Returns:
            测试网络列表 / List of test networks
        """
        test_cases = []
        
        # 测试用例1: 空网络
        G1 = nx.Graph()
        test_cases.append(("Empty Network", G1))
        
        # 测试用例2: 单节点网络
        G2 = nx.Graph()
        G2.add_node(0)
        test_cases.append(("Single Node Network", G2))
        
        # 测试用例3: 星形网络
        G3 = nx.star_graph(5)
        test_cases.append(("Star Network", G3))
        
        # 测试用例4: 环形网络
        G4 = nx.cycle_graph(6)
        test_cases.append(("Ring Network", G4))
        
        # 测试用例5: 完全网络
        G5 = nx.complete_graph(5)
        test_cases.append(("Complete Network", G5))
        
        # 测试用例6: 树形网络
        G6 = nx.balanced_tree(2, 3)
        test_cases.append(("Tree Network", G6))
        
        # 测试用例7: 小世界网络
        G7 = nx.watts_strogatz_graph(20, 4, 0.3)
        test_cases.append(("Small World Network", G7))
        
        # 测试用例8: 无标度网络
        G8 = nx.barabasi_albert_graph(50, 2)
        test_cases.append(("Scale-Free Network", G8))
        
        # 测试用例9: 随机网络
        G9 = nx.erdos_renyi_graph(30, 0.2)
        test_cases.append(("Random Network", G9))
        
        # 测试用例10: 网格网络
        G10 = nx.grid_2d_graph(4, 4)
        test_cases.append(("Grid Network", G10))
        
        return test_cases
    
    def run_comprehensive_verification(self) -> Dict[str, Any]:
        """
        运行全面验证 / Run Comprehensive Verification
        
        返回 / Returns:
            验证结果摘要 / Verification summary
        """
        print("🚀 开始网络拓扑定理全面验证 / Starting Comprehensive Network Topology Verification")
        print("=" * 80)
        
        test_cases = self.generate_test_cases()
        self.verification_stats['total_tests'] = len(test_cases)
        
        for i, (name, graph) in enumerate(test_cases, 1):
            print(f"\n📋 测试用例 {i}: {name}")
            print(f"   节点数: {graph.number_of_nodes()}, 边数: {graph.number_of_edges()}")
            
            # 验证拓扑性质
            topology_result = self.verify_topology_properties(graph)
            
            # 验证小世界性质
            small_world_result = self.verify_small_world_properties(graph)
            
            # 验证无标度性质
            scale_free_result = self.verify_scale_free_properties(graph)
            
            # 合并结果
            combined_result = {
                'test_name': name,
                'topology_properties': topology_result,
                'small_world_properties': small_world_result,
                'scale_free_properties': scale_free_result
            }
            
            self.test_results.append(combined_result)
            
            # 显示结果
            topology = topology_result['topology_properties']
            verification = topology_result['verification_result']
            
            print(f"   连通性: {topology['connectivity']} ≤ {topology['min_degree']} ({topology['connectivity_bound']})")
            print(f"   冗余性: {topology['redundancy']:.3f} ≥ 0 ({topology['redundancy_nonnegative']})")
            print(f"   效率性: {topology['efficiency']:.3f} ≤ 1 ({topology['efficiency_bound']})")
            print(f"   小世界: {small_world_result['verification_result']['is_small_world']}")
            print(f"   无标度: {scale_free_result['verification_result']['is_scale_free']}")
            print(f"   验证时间: {verification['verification_time']:.4f}秒")
            
            if verification['all_properties_hold']:
                self.verification_stats['passed_tests'] += 1
                print("   ✅ 验证通过")
            else:
                self.verification_stats['failed_tests'] += 1
                print("   ❌ 验证失败")
        
        # 生成摘要报告
        summary = self.generate_summary_report()
        print("\n" + "=" * 80)
        print("📊 验证摘要 / Verification Summary")
        print("=" * 80)
        print(f"总测试数: {summary['total_tests']}")
        print(f"通过测试: {summary['passed_tests']}")
        print(f"失败测试: {summary['failed_tests']}")
        print(f"成功率: {summary['success_rate']:.2f}%")
        print(f"总验证时间: {summary['total_time']:.4f}秒")
        
        return summary
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """
        生成摘要报告 / Generate Summary Report
        
        返回 / Returns:
            摘要报告 / Summary report
        """
        total_time = sum(result['topology_properties']['verification_result']['verification_time'] 
                        for result in self.test_results)
        
        success_rate = (self.verification_stats['passed_tests'] / 
                       self.verification_stats['total_tests'] * 100) if self.verification_stats['total_tests'] > 0 else 0
        
        return {
            'total_tests': self.verification_stats['total_tests'],
            'passed_tests': self.verification_stats['passed_tests'],
            'failed_tests': self.verification_stats['failed_tests'],
            'success_rate': success_rate,
            'total_time': total_time,
            'verification_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def save_verification_report(self, filename: str = "network_topology_verification_report.json"):
        """
        保存验证报告 / Save Verification Report
        
        参数 / Parameters:
            filename: 文件名 / Filename
        """
        report = {
            'verification_summary': self.generate_summary_report(),
            'test_results': self.test_results,
            'metadata': {
                'verifier_version': '1.0.0',
                'verification_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'python_version': '3.8+',
                'dependencies': ['networkx', 'matplotlib', 'numpy']
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 验证报告已保存到: {filename}")
    
    def visualize_test_case(self, graph: nx.Graph, title: str = "Test Network"):
        """
        可视化测试用例 / Visualize Test Case
        
        参数 / Parameters:
            graph: 要可视化的网络 / Network to visualize
            title: 图表标题 / Chart title
        """
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(graph)
        
        # 绘制节点
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue', 
                              node_size=500)
        
        # 绘制边
        nx.draw_networkx_edges(graph, pos, edge_color='gray')
        
        # 添加节点标签
        nx.draw_networkx_labels(graph, pos)
        
        # 添加度数标签
        degrees = dict(graph.degree())
        for node, degree in degrees.items():
            plt.text(pos[node][0], pos[node][1] + 0.1, f'd={degree}', 
                    ha='center', va='bottom', fontsize=8)
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def main():
    """主函数 / Main Function"""
    print("🎯 网络拓扑形式化验证器 / Network Topology Formal Verifier")
    print("=" * 80)
    
    # 创建验证器
    verifier = NetworkTopologyVerifier()
    
    # 运行全面验证
    summary = verifier.run_comprehensive_verification()
    
    # 保存报告
    verifier.save_verification_report()
    
    # 可视化示例
    print("\n🎨 可视化示例 / Visualization Example")
    test_cases = verifier.generate_test_cases()
    example_graph = test_cases[6][1]  # 小世界网络
    verifier.visualize_test_case(example_graph, "Small World Network Example")
    
    print("\n✅ 验证完成！/ Verification Complete!")

if __name__ == "__main__":
    main()
