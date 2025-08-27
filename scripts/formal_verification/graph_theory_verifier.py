#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图论形式化验证器 / Graph Theory Formal Verifier

功能 / Features:
- 验证图论基本定理
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

class GraphTheoryVerifier:
    """图论验证器 / Graph Theory Verifier"""
    
    def __init__(self):
        """初始化验证器"""
        self.test_results = []
        self.verification_stats = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'verification_time': 0
        }
    
    def verify_handshaking_lemma(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        验证握手定理 / Verify Handshaking Lemma
        
        参数 / Parameters:
            graph: 待验证的图 / Graph to verify
            
        返回 / Returns:
            验证结果字典 / Verification result dictionary
        """
        start_time = time.time()
        
        # 计算所有顶点的度数
        degrees = dict(graph.degree())
        sum_degrees = sum(degrees.values())
        edge_count = graph.number_of_edges()
        
        # 验证握手定理
        handshaking_holds = sum_degrees == 2 * edge_count
        
        # 验证奇度顶点数为偶数
        odd_degree_count = sum(1 for d in degrees.values() if d % 2 == 1)
        odd_degree_even = odd_degree_count % 2 == 0
        
        verification_time = time.time() - start_time
        
        result = {
            'graph_info': {
                'nodes': list(graph.nodes()),
                'edges': list(graph.edges()),
                'num_nodes': graph.number_of_nodes(),
                'num_edges': graph.number_of_edges(),
                'degrees': degrees
            },
            'handshaking_lemma': {
                'sum_degrees': sum_degrees,
                'edge_count': edge_count,
                'expected': 2 * edge_count,
                'holds': handshaking_holds
            },
            'odd_degree_corollary': {
                'odd_degree_count': odd_degree_count,
                'is_even': odd_degree_even
            },
            'verification_result': {
                'both_theorems_hold': handshaking_holds and odd_degree_even,
                'verification_time': verification_time
            }
        }
        
        return result
    
    def verify_graph_properties(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        验证图的基本性质 / Verify Basic Graph Properties
        
        参数 / Parameters:
            graph: 待验证的图 / Graph to verify
            
        返回 / Returns:
            验证结果字典 / Verification result dictionary
        """
        start_time = time.time()
        
        # 基本性质验证
        properties = {
            'is_connected': nx.is_connected(graph),
            'is_bipartite': nx.is_bipartite(graph),
            'is_planar': nx.check_planarity(graph)[0] if graph.number_of_nodes() > 0 else True,
            'diameter': nx.diameter(graph) if nx.is_connected(graph) else float('inf'),
            'average_clustering': nx.average_clustering(graph),
            'density': nx.density(graph)
        }
        
        # 度数分析
        degrees = dict(graph.degree())
        degree_analysis = {
            'min_degree': min(degrees.values()) if degrees else 0,
            'max_degree': max(degrees.values()) if degrees else 0,
            'average_degree': sum(degrees.values()) / len(degrees) if degrees else 0,
            'degree_sequence': sorted(degrees.values(), reverse=True)
        }
        
        # 连通性分析
        connectivity_analysis = {
            'num_components': nx.number_connected_components(graph),
            'components': list(nx.connected_components(graph)),
            'articulation_points': list(nx.articulation_points(graph)),
            'bridges': list(nx.bridges(graph))
        }
        
        verification_time = time.time() - start_time
        
        result = {
            'graph_info': {
                'nodes': list(graph.nodes()),
                'edges': list(graph.edges()),
                'num_nodes': graph.number_of_nodes(),
                'num_edges': graph.number_of_edges()
            },
            'basic_properties': properties,
            'degree_analysis': degree_analysis,
            'connectivity_analysis': connectivity_analysis,
            'verification_time': verification_time
        }
        
        return result
    
    def generate_test_cases(self) -> List[Tuple[str, nx.Graph]]:
        """
        生成测试用例 / Generate Test Cases
        
        返回 / Returns:
            测试图列表 / List of test graphs
        """
        test_cases = []
        
        # 测试用例1: 空图
        G1 = nx.Graph()
        test_cases.append(("Empty Graph", G1))
        
        # 测试用例2: 单顶点图
        G2 = nx.Graph()
        G2.add_node(0)
        test_cases.append(("Single Vertex Graph", G2))
        
        # 测试用例3: 单边图
        G3 = nx.Graph()
        G3.add_edge(0, 1)
        test_cases.append(("Single Edge Graph", G3))
        
        # 测试用例4: 路径图
        G4 = nx.path_graph(4)
        test_cases.append(("Path Graph P4", G4))
        
        # 测试用例5: 圈图
        G5 = nx.cycle_graph(5)
        test_cases.append(("Cycle Graph C5", G5))
        
        # 测试用例6: 完全图
        G6 = nx.complete_graph(4)
        test_cases.append(("Complete Graph K4", G6))
        
        # 测试用例7: 星图
        G7 = nx.star_graph(5)
        test_cases.append(("Star Graph S5", G7))
        
        # 测试用例8: 二分图
        G8 = nx.complete_bipartite_graph(3, 3)
        test_cases.append(("Complete Bipartite Graph K3,3", G8))
        
        # 测试用例9: 随机图
        G9 = nx.erdos_renyi_graph(10, 0.3)
        test_cases.append(("Random Graph ER(10,0.3)", G9))
        
        # 测试用例10: 小世界网络
        G10 = nx.watts_strogatz_graph(10, 4, 0.3)
        test_cases.append(("Small World Network WS(10,4,0.3)", G10))
        
        return test_cases
    
    def run_comprehensive_verification(self) -> Dict[str, Any]:
        """
        运行全面验证 / Run Comprehensive Verification
        
        返回 / Returns:
            验证结果摘要 / Verification summary
        """
        print("🚀 开始图论定理全面验证 / Starting Comprehensive Graph Theory Verification")
        print("=" * 70)
        
        test_cases = self.generate_test_cases()
        self.verification_stats['total_tests'] = len(test_cases)
        
        for i, (name, graph) in enumerate(test_cases, 1):
            print(f"\n📋 测试用例 {i}: {name}")
            print(f"   节点数: {graph.number_of_nodes()}, 边数: {graph.number_of_edges()}")
            
            # 验证握手定理
            handshaking_result = self.verify_handshaking_lemma(graph)
            
            # 验证图的性质
            properties_result = self.verify_graph_properties(graph)
            
            # 合并结果
            combined_result = {
                'test_name': name,
                'handshaking_lemma': handshaking_result,
                'graph_properties': properties_result
            }
            
            self.test_results.append(combined_result)
            
            # 显示结果
            handshaking = handshaking_result['handshaking_lemma']
            odd_degree = handshaking_result['odd_degree_corollary']
            verification = handshaking_result['verification_result']
            
            print(f"   握手定理: {handshaking['holds']}")
            print(f"   奇度顶点数: {odd_degree['odd_degree_count']} (偶数: {odd_degree['is_even']})")
            print(f"   度数之和: {handshaking['sum_degrees']} = 2 × {handshaking['edge_count']}")
            print(f"   验证时间: {verification['verification_time']:.4f}秒")
            
            if verification['both_theorems_hold']:
                self.verification_stats['passed_tests'] += 1
                print("   ✅ 验证通过")
            else:
                self.verification_stats['failed_tests'] += 1
                print("   ❌ 验证失败")
        
        # 生成摘要报告
        summary = self.generate_summary_report()
        print("\n" + "=" * 70)
        print("📊 验证摘要 / Verification Summary")
        print("=" * 70)
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
        total_time = sum(result['handshaking_lemma']['verification_result']['verification_time'] 
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
    
    def save_verification_report(self, filename: str = "graph_theory_verification_report.json"):
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
    
    def visualize_test_case(self, graph: nx.Graph, title: str = "Test Graph"):
        """
        可视化测试用例 / Visualize Test Case
        
        参数 / Parameters:
            graph: 要可视化的图 / Graph to visualize
            title: 图表标题 / Chart title
        """
        plt.figure(figsize=(8, 6))
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
    print("🎯 图论形式化验证器 / Graph Theory Formal Verifier")
    print("=" * 70)
    
    # 创建验证器
    verifier = GraphTheoryVerifier()
    
    # 运行全面验证
    summary = verifier.run_comprehensive_verification()
    
    # 保存报告
    verifier.save_verification_report()
    
    # 可视化示例
    print("\n🎨 可视化示例 / Visualization Example")
    test_cases = verifier.generate_test_cases()
    example_graph = test_cases[3][1]  # 路径图
    verifier.visualize_test_case(example_graph, "Path Graph P4 Example")
    
    print("\n✅ 验证完成！/ Verification Complete!")

if __name__ == "__main__":
    main()
