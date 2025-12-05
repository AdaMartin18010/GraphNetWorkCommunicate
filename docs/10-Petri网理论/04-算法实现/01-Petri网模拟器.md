# Petri网模拟器 / Petri Net Simulator

## 📚 **概述 / Overview**

本文档描述基本Petri网模拟器的实现，包括模拟器的核心功能、状态管理和执行机制。Petri网模拟器是分析和验证Petri网模型的基础工具，支持状态转换、可达性分析和性质验证。

---

## 📑 **目录 / Table of Contents**

- [Petri网模拟器 / Petri Net Simulator](#petri网模拟器--petri-net-simulator)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [🔧 **功能特性 / Features**](#-功能特性--features)
  - [💻 **算法实现 / Implementation**](#-算法实现--implementation)
    - [完整代码实现](#完整代码实现)
  - [📊 **复杂度分析 / Complexity Analysis**](#-复杂度分析--complexity-analysis)
    - [时间复杂度](#时间复杂度)
    - [空间复杂度](#空间复杂度)
  - [🔗 **相关链接 / Related Links**](#-相关链接--related-links)

---

## 🔧 **功能特性 / Features**

- Petri网状态表示和初始化
- 变迁使能性检查
- 变迁触发和状态更新
- 可达性分析
- 状态图生成
- 有界性检查
- 死锁检测

---

## 💻 **算法实现 / Implementation**

### 完整代码实现

```python
from typing import Dict, Set, List, Tuple
from collections import defaultdict

class PetriNet:
    """
    基本Petri网实现。
    """

    def __init__(self, places: List[str], transitions: List[str],
                 flows: List[Tuple[str, str, int]], initial_marking: Dict[str, int]):
        """
        初始化Petri网。

        Args:
            places: 库所列表
            transitions: 变迁列表
            flows: 流关系列表，每个元素为 (source, target, weight)
            initial_marking: 初始标识，字典 {place: token_count}
        """
        self.places = set(places)
        self.transitions = set(transitions)

        # 构建前集和后集
        self.pre_set: Dict[str, Set[Tuple[str, int]]] = defaultdict(set)
        self.post_set: Dict[str, Set[Tuple[str, int]]] = defaultdict(set)

        for source, target, weight in flows:
            if source in self.places and target in self.transitions:
                # 库所 -> 变迁
                self.pre_set[target].add((source, weight))
            elif source in self.transitions and target in self.places:
                # 变迁 -> 库所
                self.post_set[source].add((target, weight))
            else:
                raise ValueError(f"Invalid flow: {source} -> {target}")

        self.marking = dict(initial_marking)
        self.reachability_set: Set[Tuple] = set()
        self.reachability_graph: Dict[Tuple, List[Tuple[str, Tuple]]] = defaultdict(list)

    def is_enabled(self, transition: str) -> bool:
        """
        检查变迁是否可触发。

        Args:
            transition: 变迁名称

        Returns:
            如果可触发返回True，否则返回False
        """
        for place, weight in self.pre_set[transition]:
            if self.marking.get(place, 0) < weight:
                return False
        return True

    def fire(self, transition: str) -> bool:
        """
        触发变迁。

        Args:
            transition: 变迁名称

        Returns:
            如果成功触发返回True，否则返回False
        """
        if not self.is_enabled(transition):
            return False

        # 消耗输入库所的令牌
        for place, weight in self.pre_set[transition]:
            self.marking[place] -= weight

        # 产生输出库所的令牌
        for place, weight in self.post_set[transition]:
            self.marking[place] = self.marking.get(place, 0) + weight

        return True

    def get_current_marking(self) -> Dict[str, int]:
        """获取当前标识"""
        return dict(self.marking)

    def reset(self, initial_marking: Dict[str, int]):
        """重置为初始标识"""
        self.marking = dict(initial_marking)

    def reachability_analysis(self, max_depth: int = 100) -> Set[Tuple]:
        """
        进行可达性分析。

        Args:
            max_depth: 最大搜索深度

        Returns:
            可达标识集
        """
        initial_marking_tuple = tuple(sorted(self.marking.items()))
        self.reachability_set = {initial_marking_tuple}
        queue = [(initial_marking_tuple, 0)]

        while queue:
            marking_tuple, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            # 恢复标识
            self.marking = dict(marking_tuple)

            # 尝试触发所有变迁
            for transition in self.transitions:
                if self.is_enabled(transition):
                    old_marking = dict(self.marking)
                    self.fire(transition)
                    new_marking_tuple = tuple(sorted(self.marking.items()))

                    # 记录可达性图
                    self.reachability_graph[marking_tuple].append((transition, new_marking_tuple))

                    # 如果新标识未访问过，加入队列
                    if new_marking_tuple not in self.reachability_set:
                        self.reachability_set.add(new_marking_tuple)
                        queue.append((new_marking_tuple, depth + 1))

                    # 恢复标识
                    self.marking = old_marking

        # 恢复初始标识
        self.marking = dict(initial_marking_tuple)
        return self.reachability_set

    def is_bounded(self, k: int = None) -> bool:
        """
        检查是否有界。

        Args:
            k: 界限值，如果为None则检查是否有界

        Returns:
            如果k有界返回True，否则返回False
        """
        reachable = self.reachability_analysis()

        for marking_tuple in reachable:
            marking = dict(marking_tuple)
            for place in self.places:
                tokens = marking.get(place, 0)
                if k is None:
                    # 检查是否有无限增长的库所
                    if tokens > 1000:  # 启发式阈值
                        return False
                elif tokens > k:
                    return False

        return True

    def is_safe(self) -> bool:
        """检查是否安全（1-有界）"""
        return self.is_bounded(k=1)

    def has_deadlock(self) -> bool:
        """
        检查是否存在死锁。

        Returns:
            如果存在死锁返回True，否则返回False
        """
        reachable = self.reachability_analysis()

        for marking_tuple in reachable:
            marking = dict(marking_tuple)
            old_marking = self.marking
            self.marking = marking

            # 检查是否有可触发的变迁
            has_enabled = any(self.is_enabled(t) for t in self.transitions)

            self.marking = old_marking

            if not has_enabled:
                return True

        return False
```

---

## 📊 **复杂度分析 / Complexity Analysis**

### 时间复杂度

- **is_enabled**: $O(|\prescript{}{}{t}|)$ - 其中 $|\prescript{}{}{t}|$ 是变迁 $t$ 的前集大小
- **fire**: $O(|\prescript{}{}{t}| + |t^{\bullet}|)$ - 需要更新输入和输出库所
- **reachability_analysis**: $O(|R| \cdot |T| \cdot (|P| + |T|))$ - 其中 $|R|$ 是可达标识数
- **is_bounded**: $O(|R| \cdot |P|)$
- **has_deadlock**: $O(|R| \cdot |T| \cdot |P|)$

### 空间复杂度

- $O(|R| \cdot |P| + |R| \cdot |T|)$ - 用于存储可达集和可达性图

---

## 🔗 **相关链接 / Related Links**

- [Petri网理论主目录](../../README.md)
- [算法实现目录](../README.md)
- [基础理论](../../01-基础理论/)
- [可达性分析算法](02-可达性分析算法.md)

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**状态**: ✅ **已完成**
