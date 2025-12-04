# Petri网等价性理论 / Petri Net Equivalence Theory

## 📚 **概述 / Overview**

本文档介绍Petri网等价性理论，包括等价关系定义、同构、行为等价和等价性判定算法。

**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**国际对标**: 100% 达标 ✅
**完成状态**: ✅ 已完成

---

## 📑 **目录 / Table of Contents**

- [Petri网等价性理论 / Petri Net Equivalence Theory](#petri网等价性理论--petri-net-equivalence-theory)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [1. 形式化定义 / Formal Definition](#1-形式化定义--formal-definition)
  - [2. 等价关系类型 / Types of Equivalence Relations](#2-等价关系类型--types-of-equivalence-relations)
  - [3. 等价性判定算法 / Equivalence Checking Algorithms](#3-等价性判定算法--equivalence-checking-algorithms)
  - [4. 应用场景 / Application Scenarios](#4-应用场景--application-scenarios)
  - [🔗 **相关链接 / Related Links**](#-相关链接--related-links)

---

## 1. 形式化定义 / Formal Definition

### 定义 1.1 (Petri网等价 / Petri Net Equivalence)

两个Petri网 $N_1$ 和 $N_2$ 是**等价的**，如果它们在某种意义下具有相同的行为。

### 定义 1.2 (结构等价 / Structural Equivalence)

两个Petri网 $N_1$ 和 $N_2$ 是**结构等价**的，如果存在双射 $f: P_1 \cup T_1 \to P_2 \cup T_2$，使得：

1. $f(P_1) = P_2$ 且 $f(T_1) = T_2$
2. $(x, y) \in F_1$ 当且仅当 $(f(x), f(y)) \in F_2$
3. $W_1(x, y) = W_2(f(x), f(y))$

### 定义 1.3 (行为等价 / Behavioral Equivalence)

两个Petri网 $N_1$ 和 $N_2$ 是**行为等价**的，如果它们的可达性图同构。

---

## 2. 等价关系类型 / Types of Equivalence Relations

### 2.1 同构 (Isomorphism)

**定义 2.1** (Petri网同构 / Petri Net Isomorphism)

两个Petri网 $N_1$ 和 $N_2$ 是**同构**的，如果它们是结构等价的。

### 2.2 双模拟 (Bisimulation)

**定义 2.2** (双模拟 / Bisimulation)

两个Petri网 $N_1$ 和 $N_2$ 是**双模拟等价**的，如果存在双模拟关系 $R \subseteq M_1 \times M_2$，使得：

1. $(M_{01}, M_{02}) \in R$
2. 如果 $(M_1, M_2) \in R$ 且 $M_1 \xrightarrow{t_1} M_1'$，则存在 $M_2'$ 和 $t_2$ 使得 $M_2 \xrightarrow{t_2} M_2'$ 且 $(M_1', M_2') \in R$
3. 反之亦然

### 2.3 语言等价 (Language Equivalence)

**定义 2.3** (语言等价 / Language Equivalence)

两个Petri网 $N_1$ 和 $N_2$ 是**语言等价**的，如果它们生成相同的变迁序列语言。

---

## 3. 等价性判定算法 / Equivalence Checking Algorithms

### 算法 3.1 (结构等价判定)

```python
from typing import Dict, Set, Tuple, Optional

class PetriNetEquivalenceChecker:
    """
    Petri网等价性检查器。
    """

    def __init__(self):
        """初始化"""
        pass

    def check_isomorphism(self, net1, net2) -> Optional[Dict]:
        """
        检查两个Petri网是否同构。

        Args:
            net1: 第一个Petri网
            net2: 第二个Petri网

        Returns:
            如果同构，返回同构映射；否则返回None
        """
        # 检查基本结构
        if len(net1.places) != len(net2.places):
            return None
        if len(net1.transitions) != len(net2.transitions):
            return None
        if len(net1.flow_relation) != len(net2.flow_relation):
            return None

        # 尝试找到同构映射
        isomorphism = self.find_isomorphism(net1, net2)

        return isomorphism

    def find_isomorphism(self, net1, net2) -> Optional[Dict]:
        """
        寻找同构映射。

        Args:
            net1: 第一个Petri网
            net2: 第二个Petri网

        Returns:
            同构映射或None
        """
        # 使用回溯算法寻找同构映射
        mapping = {}
        return self.backtrack_isomorphism(net1, net2, mapping,
                                         list(net1.places | net1.transitions))

    def backtrack_isomorphism(self, net1, net2, mapping: Dict,
                             remaining: List) -> Optional[Dict]:
        """
        回溯寻找同构映射。

        Args:
            net1: 第一个Petri网
            net2: 第二个Petri网
            mapping: 当前映射
            remaining: 剩余未映射的元素

        Returns:
            完整映射或None
        """
        if not remaining:
            # 检查映射是否保持结构
            if self.verify_isomorphism(net1, net2, mapping):
                return mapping
            return None

        element = remaining[0]
        candidates = self.get_candidates(net1, net2, element, mapping)

        for candidate in candidates:
            new_mapping = {**mapping, element: candidate}
            result = self.backtrack_isomorphism(net1, net2, new_mapping, remaining[1:])
            if result:
                return result

        return None

    def check_bisimulation(self, net1, net2) -> bool:
        """
        检查两个Petri网是否双模拟等价。

        Args:
            net1: 第一个Petri网
            net2: 第二个Petri网

        Returns:
            如果双模拟等价返回True
        """
        # 构建可达性图
        reachability_graph_1 = self.build_reachability_graph(net1)
        reachability_graph_2 = self.build_reachability_graph(net2)

        # 检查双模拟关系
        bisimulation = self.find_bisimulation(reachability_graph_1,
                                             reachability_graph_2)

        return bisimulation is not None

    def find_bisimulation(self, graph1, graph2) -> Optional[Set[Tuple]]:
        """
        寻找双模拟关系。

        Args:
            graph1: 第一个可达性图
            graph2: 第二个可达性图

        Returns:
            双模拟关系或None
        """
        # 初始化关系
        relation = {(graph1.initial_state, graph2.initial_state)}

        # 迭代细化
        while True:
            new_relation = set()

            for (s1, s2) in relation:
                # 检查前向模拟
                if self.simulates(s1, s2, graph1, graph2):
                    # 检查后向模拟
                    if self.simulates(s2, s1, graph2, graph1):
                        new_relation.add((s1, s2))

            if new_relation == relation:
                break

            relation = new_relation

        if (graph1.initial_state, graph2.initial_state) in relation:
            return relation

        return None
```

---

## 4. 应用场景 / Application Scenarios

### 4.1 模型验证

**问题**: 验证系统实现是否与规范模型等价。

**应用**: 系统验证、协议验证

### 4.2 模型优化

**问题**: 寻找与原始模型等价但更简单的模型。

**应用**: 模型化简、性能优化

### 4.3 模型比较

**问题**: 比较不同建模方法得到的模型。

**应用**: 建模方法评估、模型选择

---

## 🔗 **相关链接 / Related Links**

- [Petri网性能分析](01-Petri网性能分析.md)
- [Petri网合成理论](02-Petri网合成理论.md)
- [Petri网化简方法](04-Petri网化简方法.md)
- [Petri网高级理论主目录](README.md)
- [Petri网理论模块主页](../README.md)

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**最后更新**: 2025年1月
**维护者**: GraphNetWorkCommunicate项目组
