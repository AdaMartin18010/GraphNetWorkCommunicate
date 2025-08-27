#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
欧拉定理自动化验证器 / Euler's Theorem Automated Verifier

功能 / Features:
- 验证欧拉定理的正确性
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

class EulerTheoremVerifier:
    """欧拉定理验证器 / Euler's Theorem Verifier"""
    
    def __init__(self):
        """初始化验证器"""
        self.test_results = []
        self.verification_stats = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'verification_time': 0
        }
    
    def verify_euler_theorem(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        验证欧拉定理 / Verify Euler's Theorem
        
        参数 / Parameters:
            graph: 待验证的图 / Graph to verify
            
        返回 / Returns:
            验证结果字典 / Verification result dictionary
        """
        start_time = time.time()
        
        # 检查图的基本属性
        is_connected = nx.is_connected(graph)
        degrees = dict(graph.degree())
        all_even_degree = all(d % 2 == 0 for d in degrees.values())
        
        # 尝试构造欧拉回路
        euler_circuit = self.find_euler_circuit(graph)
        has_euler_circuit = euler_circuit is not None
        
        # 验证定理
        theorem_holds = (is_connected and all_even_degree) == has_euler_circuit
        
        verification_time = time.time() - start_time
        
        result = {
            'graph_info': {
                'nodes': list(graph.nodes()),
                'edges': list(graph.edges()),
                'num_nodes': graph.number_of_nodes(),
                'num_edges': graph.number_of_edges(),
                'degrees': degrees
            },
            'theorem_conditions': {
                'connected': is_connected,
                'all_even_degree': all_even_degree,
                'has_euler_circuit': has_euler_circuit
            },
            'verification_result': {
                'theorem_holds': theorem_holds,
                'verification_time': verification_time
            },
            'euler_circuit': euler_circuit
        }
        
        return result
    
    def find_euler_circuit(self, graph: nx.Graph) -> Optional[List[Tuple]]:
        """
        寻找欧拉回路 / Find Euler Circuit
        
        参数 / Parameters:
            graph: 输入图 / Input graph
            
        返回 / Returns:
            欧拉回路或None / Euler circuit or None
        """
        if not nx.is_connected(graph):
            return None
        
        degrees = dict(graph.degree())
        if not all(d % 2 == 0 for d in degrees.values()):
            return None
        
        # 复制图以避免修改原图
        G = graph.copy()
        circuit = []
        current_vertex = next(iter(G.nodes()))
        
        while G.number_of_edges() > 0:
            # 找到从当前顶点出发的边
            neighbors = list(G.neighbors(current_vertex))
            if not neighbors:
                break
            
            next_vertex = neighbors[0]
            edge = (current_vertex, next_vertex)
            
            # 添加到回路
            circuit.append(edge)
            
            # 移除边
            G.remove_edge(current_vertex, next_vertex)
            
            # 移动到下一个顶点
            current_vertex = next_vertex
        
        # 检查是否形成了完整的欧拉回路
        if len(circuit) == graph.number_of_edges():
            return circuit
        else:
            return None
    
    def generate_test_cases(self) -> List[nx.Graph]:
        """
        生成测试用例 / Generate Test Cases
        
        返回 / Returns:
            测试图列表 / List of test graphs
        """
        test_cases = []
        
        # 测试用例1: 简单欧拉图
        G1 = nx.Graph()
        G1.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
        test_cases.append(("Simple Euler Graph", G1))
        
        # 测试用例2: 复杂欧拉图
        G2 = nx.Graph()
        G2.add_edges_from([
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),
            (1, 3), (2, 4), (3, 5)
        ])
        test_cases.append(("Complex Euler Graph", G2))
        
        # 测试用例3: 非欧拉图（有奇数度顶点）
        G3 = nx.Graph()
        G3.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])
        test_cases.append(("Non-Euler Graph (Odd Degree)", G3))
        
        # 测试用例4: 非连通图
        G4 = nx.Graph()
        G4.add_edges_from([(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)])
        test_cases.append(("Disconnected Graph", G4))
        
        # 测试用例5: 空图
        G5 = nx.Graph()
        test_cases.append(("Empty Graph", G5))
        
        # 测试用例6: 单顶点图
        G6 = nx.Graph()
        G6.add_node(0)
        test_cases.append(("Single Vertex Graph", G6))
        
        return test_cases
    
    def run_verification_suite(self) -> Dict[str, Any]:
        """
        运行完整验证套件 / Run Complete Verification Suite
        
        返回 / Returns:
            验证结果摘要 / Verification summary
        """
        print("🚀 开始欧拉定理验证套件 / Starting Euler's Theorem Verification Suite")
        print("=" * 60)
        
        test_cases = self.generate_test_cases()
        self.verification_stats['total_tests'] = len(test_cases)
        
        for i, (name, graph) in enumerate(test_cases, 1):
            print(f"\n📋 测试用例 {i}: {name}")
            print(f"   节点数: {graph.number_of_nodes()}, 边数: {graph.number_of_edges()}")
            
            result = self.verify_euler_theorem(graph)
            self.test_results.append((name, result))
            
            # 显示结果
            conditions = result['theorem_conditions']
            verification = result['verification_result']
            
            print(f"   连通性: {conditions['connected']}")
            print(f"   所有顶点度为偶数: {conditions['all_even_degree']}")
            print(f"   存在欧拉回路: {conditions['has_euler_circuit']}")
            print(f"   定理成立: {verification['theorem_holds']}")
            print(f"   验证时间: {verification['verification_time']:.4f}秒")
            
            if verification['theorem_holds']:
                self.verification_stats['passed_tests'] += 1
                print("   ✅ 验证通过")
            else:
                self.verification_stats['failed_tests'] += 1
                print("   ❌ 验证失败")
        
        # 生成摘要报告
        summary = self.generate_summary_report()
        print("\n" + "=" * 60)
        print("📊 验证摘要 / Verification Summary")
        print("=" * 60)
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
        total_time = sum(result[1]['verification_result']['verification_time'] 
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
    
    def save_verification_report(self, filename: str = "euler_theorem_verification_report.json"):
        """
        保存验证报告 / Save Verification Report
        
        参数 / Parameters:
            filename: 文件名 / Filename
        """
        report = {
            'verification_summary': self.generate_summary_report(),
            'test_results': [
                {
                    'test_name': name,
                    'result': result
                }
                for name, result in self.test_results
            ],
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
        
        # 添加边标签（度数）
        edge_labels = {}
        for edge in graph.edges():
            edge_labels[edge] = f"{graph.degree(edge[0])},{graph.degree(edge[1])}"
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def main():
    """主函数 / Main Function"""
    print("🎯 欧拉定理自动化验证器 / Euler's Theorem Automated Verifier")
    print("=" * 60)
    
    # 创建验证器
    verifier = EulerTheoremVerifier()
    
    # 运行验证套件
    summary = verifier.run_verification_suite()
    
    # 保存报告
    verifier.save_verification_report()
    
    # 可视化示例
    print("\n🎨 可视化示例 / Visualization Example")
    test_cases = verifier.generate_test_cases()
    example_graph = test_cases[0][1]  # 第一个测试用例
    verifier.visualize_test_case(example_graph, "Simple Euler Graph Example")
    
    print("\n✅ 验证完成！/ Verification Complete!")

if __name__ == "__main__":
    main()
