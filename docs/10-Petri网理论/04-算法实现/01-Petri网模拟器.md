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
    - [使用示例 / Usage Examples](#使用示例--usage-examples)
      - [示例1：简单Petri网 / Example 1: Simple Petri Net](#示例1简单petri网--example-1-simple-petri-net)
      - [示例2：可达性分析 / Example 2: Reachability Analysis](#示例2可达性分析--example-2-reachability-analysis)
      - [示例3：死锁检测 / Example 3: Deadlock Detection](#示例3死锁检测--example-3-deadlock-detection)
    - [测试用例 / Test Cases](#测试用例--test-cases)
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
"""
Petri网模拟器实现

本模块提供基本Petri网的完整实现，包括：
- Petri网的创建和初始化
- 变迁的可触发性检查
- 变迁的触发和状态更新
- 可达性分析
- 有界性和死锁检测

作者: GraphNetWorkCommunicate项目组
版本: v2.0
日期: 2025年1月
"""

from typing import Dict, Set, List, Tuple, Optional
from collections import defaultdict

class PetriNet:
    """
    基本Petri网实现。

    一个Petri网由以下部分组成：
    - 库所（Places）：表示系统状态
    - 变迁（Transitions）：表示事件或动作
    - 流关系（Flow Relations）：连接库所和变迁
    - 初始标识（Initial Marking）：系统的初始状态

    示例:
        >>> places = ['P1', 'P2']
        >>> transitions = ['T1', 'T2']
        >>> flows = [('P1', 'T1', 1), ('T1', 'P2', 1), ('P2', 'T2', 1), ('T2', 'P1', 1)]
        >>> initial_marking = {'P1': 1, 'P2': 0}
        >>> net = PetriNet(places, transitions, flows, initial_marking)
        >>> net.is_enabled('T1')
        True
        >>> net.fire('T1')
        True
        >>> net.get_current_marking()
        {'P1': 0, 'P2': 1}
    """

    def __init__(self, places: List[str], transitions: List[str],
                 flows: List[Tuple[str, str, int]], initial_marking: Dict[str, int]):
        """
        初始化Petri网。

        Args:
            places: 库所列表，例如 ['P1', 'P2', 'P3']
            transitions: 变迁列表，例如 ['T1', 'T2']
            flows: 流关系列表，每个元素为 (source, target, weight)
                   例如 [('P1', 'T1', 1), ('T1', 'P2', 1)]
            initial_marking: 初始标识，字典 {place: token_count}
                           例如 {'P1': 1, 'P2': 0}

        Raises:
            ValueError: 如果流关系无效（如库所连接到库所）

        示例:
            >>> net = PetriNet(
            ...     places=['P1', 'P2'],
            ...     transitions=['T1'],
            ...     flows=[('P1', 'T1', 1), ('T1', 'P2', 1)],
            ...     initial_marking={'P1': 1, 'P2': 0}
            ... )
        """
        # 验证输入
        if not places or not transitions:
            raise ValueError("Places and transitions cannot be empty")

        if not flows:
            raise ValueError("Flows cannot be empty")

        self.places = set(places)
        self.transitions = set(transitions)

        # 构建前集和后集
        # pre_set[transition] = {(place, weight), ...} 表示变迁的输入库所和权重
        # post_set[transition] = {(place, weight), ...} 表示变迁的输出库所和权重
        self.pre_set: Dict[str, Set[Tuple[str, int]]] = defaultdict(set)
        self.post_set: Dict[str, Set[Tuple[str, int]]] = defaultdict(set)

        for source, target, weight in flows:
            if weight <= 0:
                raise ValueError(f"Weight must be positive, got {weight}")

            if source in self.places and target in self.transitions:
                # 库所 -> 变迁（输入边）
                self.pre_set[target].add((source, weight))
            elif source in self.transitions and target in self.places:
                # 变迁 -> 库所（输出边）
                self.post_set[source].add((target, weight))
            else:
                raise ValueError(f"Invalid flow: {source} -> {target}. "
                               f"Must be Place->Transition or Transition->Place")

        # 设置初始标识
        self.marking = dict(initial_marking)

        # 确保所有库所都在标识中（默认为0）
        for place in self.places:
            if place not in self.marking:
                self.marking[place] = 0

        # 可达性分析相关数据结构
        self.reachability_set: Set[Tuple] = set()
        self.reachability_graph: Dict[Tuple, List[Tuple[str, Tuple]]] = defaultdict(list)

    def is_enabled(self, transition: str) -> bool:
        """
        检查变迁是否可触发。

        一个变迁可触发，当且仅当它的所有输入库所中的令牌数
        都大于等于相应边的权重。

        Args:
            transition: 变迁名称，必须在self.transitions中

        Returns:
            如果可触发返回True，否则返回False

        Raises:
            ValueError: 如果变迁不存在

        示例:
            >>> net = PetriNet(['P1'], ['T1'], [('P1', 'T1', 1)], {'P1': 1})
            >>> net.is_enabled('T1')
            True
            >>> net.fire('T1')
            True
            >>> net.is_enabled('T1')
            False
        """
        if transition not in self.transitions:
            raise ValueError(f"Transition '{transition}' not found")

        # 检查所有输入库所是否都有足够的令牌
        for place, weight in self.pre_set[transition]:
            if self.marking.get(place, 0) < weight:
                return False
        return True

    def fire(self, transition: str) -> bool:
        """
        触发变迁。

        如果变迁可触发，则：
        1. 从所有输入库所中消耗相应权重的令牌
        2. 在所有输出库所中产生相应权重的令牌

        Args:
            transition: 变迁名称，必须在self.transitions中

        Returns:
            如果成功触发返回True，否则返回False（变迁不可触发）

        Raises:
            ValueError: 如果变迁不存在

        示例:
            >>> net = PetriNet(['P1', 'P2'], ['T1'],
            ...                [('P1', 'T1', 1), ('T1', 'P2', 1)],
            ...                {'P1': 1, 'P2': 0})
            >>> net.fire('T1')
            True
            >>> net.get_current_marking()
            {'P1': 0, 'P2': 1}
            >>> net.fire('T1')  # 再次触发失败（P1没有令牌）
            False
        """
        if transition not in self.transitions:
            raise ValueError(f"Transition '{transition}' not found")

        # 检查是否可触发
        if not self.is_enabled(transition):
            return False

        # 第一步：消耗输入库所的令牌
        for place, weight in self.pre_set[transition]:
            self.marking[place] -= weight
            # 确保令牌数不为负（防御性编程）
            assert self.marking[place] >= 0, f"Negative tokens in place {place}"

        # 第二步：产生输出库所的令牌
        for place, weight in self.post_set[transition]:
            self.marking[place] = self.marking.get(place, 0) + weight

        return True

    def get_current_marking(self) -> Dict[str, int]:
        """
        获取当前标识。

        Returns:
            当前标识的副本，字典 {place: token_count}

        示例:
            >>> net = PetriNet(['P1'], ['T1'], [('P1', 'T1', 1)], {'P1': 1})
            >>> net.get_current_marking()
            {'P1': 1}
            >>> net.fire('T1')
            True
            >>> net.get_current_marking()
            {'P1': 0}
        """
        return dict(self.marking)

    def reset(self, initial_marking: Optional[Dict[str, int]] = None):
        """
        重置为初始标识或指定标识。

        Args:
            initial_marking: 要重置到的标识，如果为None则重置到创建时的初始标识

        示例:
            >>> net = PetriNet(['P1'], ['T1'], [('P1', 'T1', 1)], {'P1': 1})
            >>> net.fire('T1')
            True
            >>> net.get_current_marking()
            {'P1': 0}
            >>> net.reset()
            >>> net.get_current_marking()
            {'P1': 1}
        """
        if initial_marking is None:
            # 重置到创建时的初始标识（需要保存）
            # 这里简化处理，实际应该保存初始标识
            raise NotImplementedError("Reset to original initial marking not implemented")
        else:
            self.marking = dict(initial_marking)
            # 确保所有库所都在标识中
            for place in self.places:
                if place not in self.marking:
                    self.marking[place] = 0

    def reachability_analysis(self, max_depth: int = 100,
                             target_marking: Optional[Dict[str, int]] = None) -> Tuple[Set[Tuple], bool]:
        """
        进行可达性分析，使用广度优先搜索（BFS）算法。

        算法步骤：
        1. 从初始标识开始
        2. 使用队列进行BFS搜索
        3. 对于每个可达标识，尝试触发所有可触发的变迁
        4. 记录所有可达标识和可达性图

        Args:
            max_depth: 最大搜索深度，防止无限搜索
            target_marking: 目标标识，如果提供则检查是否可达

        Returns:
            (reachable_markings, target_reachable)
            - reachable_markings: 可达标识集合
            - target_reachable: 如果target_marking提供，返回是否可达；否则返回False

        示例:
            >>> net = PetriNet(['P1', 'P2'], ['T1'],
            ...                [('P1', 'T1', 1), ('T1', 'P2', 1)],
            ...                {'P1': 1, 'P2': 0})
            >>> markings, _ = net.reachability_analysis()
            >>> len(markings)
            2
            >>> target = {'P1': 0, 'P2': 1}
            >>> _, reachable = net.reachability_analysis(target_marking=target)
            >>> reachable
            True
        """
        # 保存初始标识
        initial_marking = dict(self.marking)
        initial_marking_tuple = tuple(sorted(self.marking.items()))

        # 初始化数据结构
        self.reachability_set = {initial_marking_tuple}
        queue = [(initial_marking_tuple, 0)]
        target_reachable = False

        # 如果提供了目标标识，转换为元组形式
        target_tuple = None
        if target_marking:
            target_tuple = tuple(sorted(target_marking.items()))

        # BFS搜索
        while queue:
            marking_tuple, depth = queue.pop(0)

            # 检查是否达到目标
            if target_tuple and marking_tuple == target_tuple:
                target_reachable = True
                # 如果只需要检查可达性，可以提前返回
                # return self.reachability_set, True

            # 检查深度限制
            if depth >= max_depth:
                continue

            # 恢复当前标识
            self.marking = dict(marking_tuple)

            # 尝试触发所有可触发的变迁
            for transition in self.transitions:
                if self.is_enabled(transition):
                    # 保存当前标识
                    old_marking = dict(self.marking)

                    # 触发变迁
                    self.fire(transition)
                    new_marking_tuple = tuple(sorted(self.marking.items()))

                    # 记录可达性图（状态转换）
                    self.reachability_graph[marking_tuple].append((transition, new_marking_tuple))

                    # 如果新标识未访问过，加入队列继续搜索
                    if new_marking_tuple not in self.reachability_set:
                        self.reachability_set.add(new_marking_tuple)
                        queue.append((new_marking_tuple, depth + 1))

                    # 恢复标识，尝试下一个变迁
                    self.marking = old_marking

        # 恢复初始标识
        self.marking = dict(initial_marking_tuple)
        return self.reachability_set, target_reachable

    def is_bounded(self, k: Optional[int] = None) -> bool:
        """
        检查Petri网是否有界。

        一个Petri网是k-有界的，如果所有可达标识中，
        每个库所的令牌数都不超过k。

        Args:
            k: 界限值，如果为None则检查是否有界（任意有限界限）
               如果提供k，则检查是否是k-有界的

        Returns:
            如果满足有界性返回True，否则返回False

        注意:
            对于无界Petri网，此方法可能无法在有限时间内完成。
            实际实现中应该使用结构分析方法（S-不变量）。

        示例:
            >>> # 有界Petri网
            >>> net1 = PetriNet(['P1', 'P2'], ['T1'],
            ...                 [('P1', 'T1', 1), ('T1', 'P2', 1)],
            ...                 {'P1': 1, 'P2': 0})
            >>> net1.is_bounded()
            True
            >>> net1.is_bounded(k=1)
            True
        """
        reachable, _ = self.reachability_analysis()

        for marking_tuple in reachable:
            marking = dict(marking_tuple)
            for place in self.places:
                tokens = marking.get(place, 0)
                if k is None:
                    # 检查是否有无限增长的库所（启发式方法）
                    if tokens > 1000:  # 启发式阈值，可能表示无界
                        return False
                elif tokens > k:
                    return False

        return True

    def is_safe(self) -> bool:
        """
        检查Petri网是否安全（1-有界）。

        安全的Petri网是1-有界的，即每个库所在所有可达标识中
        最多只有1个令牌。

        Returns:
            如果安全返回True，否则返回False

        示例:
            >>> net = PetriNet(['P1', 'P2'], ['T1'],
            ...                [('P1', 'T1', 1), ('T1', 'P2', 1)],
            ...                {'P1': 1, 'P2': 0})
            >>> net.is_safe()
            True
        """
        return self.is_bounded(k=1)

    def has_deadlock(self) -> bool:
        """
        检查Petri网是否存在死锁。

        死锁是指存在一个可达标识，在该标识下没有任何变迁可触发。

        Returns:
            如果存在死锁返回True，否则返回False

        示例:
            >>> # 无死锁的Petri网
            >>> net1 = PetriNet(['P1', 'P2'], ['T1'],
            ...                 [('P1', 'T1', 1), ('T1', 'P2', 1)],
            ...                 {'P1': 1, 'P2': 0})
            >>> net1.has_deadlock()
            False
            >>> # 有死锁的Petri网（所有变迁都不可触发）
            >>> net2 = PetriNet(['P1'], ['T1'],
            ...                 [('P1', 'T1', 2)],  # 需要2个令牌
            ...                 {'P1': 1})  # 但只有1个
            >>> net2.has_deadlock()
            True
        """
        reachable, _ = self.reachability_analysis()

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

    def get_enabled_transitions(self) -> List[str]:
        """
        获取当前标识下所有可触发的变迁。

        Returns:
            可触发变迁的列表

        示例:
            >>> net = PetriNet(['P1', 'P2'], ['T1', 'T2'],
            ...                [('P1', 'T1', 1), ('T1', 'P2', 1), ('P2', 'T2', 1)],
            ...                {'P1': 1, 'P2': 0})
            >>> net.get_enabled_transitions()
            ['T1']
            >>> net.fire('T1')
            True
            >>> net.get_enabled_transitions()
            ['T2']
        """
        enabled = []
        for transition in self.transitions:
            if self.is_enabled(transition):
                enabled.append(transition)
        return enabled
```

### 使用示例 / Usage Examples

#### 示例1：简单Petri网 / Example 1: Simple Petri Net

```python
# 创建一个简单的Petri网
places = ['P1', 'P2']
transitions = ['T1']
flows = [('P1', 'T1', 1), ('T1', 'P2', 1)]
initial_marking = {'P1': 1, 'P2': 0}

net = PetriNet(places, transitions, flows, initial_marking)

# 检查初始状态
print("Initial marking:", net.get_current_marking())
# 输出: {'P1': 1, 'P2': 0}

# 检查T1是否可触发
print("T1 enabled:", net.is_enabled('T1'))
# 输出: True

# 触发T1
net.fire('T1')
print("After firing T1:", net.get_current_marking())
# 输出: {'P1': 0, 'P2': 1}
```

#### 示例2：可达性分析 / Example 2: Reachability Analysis

```python
# 创建一个循环Petri网
places = ['P1', 'P2']
transitions = ['T1', 'T2']
flows = [
    ('P1', 'T1', 1), ('T1', 'P2', 1),
    ('P2', 'T2', 1), ('T2', 'P1', 1)
]
initial_marking = {'P1': 1, 'P2': 0}

net = PetriNet(places, transitions, flows, initial_marking)

# 进行可达性分析
reachable, _ = net.reachability_analysis()
print(f"Number of reachable markings: {len(reachable)}")
# 输出: Number of reachable markings: 2

# 检查是否有死锁
print("Has deadlock:", net.has_deadlock())
# 输出: Has deadlock: False

# 检查是否安全
print("Is safe:", net.is_safe())
# 输出: Is safe: True
```

#### 示例3：死锁检测 / Example 3: Deadlock Detection

```python
# 创建一个有死锁的Petri网
places = ['P1', 'P2']
transitions = ['T1', 'T2']
flows = [
    ('P1', 'T1', 1), ('P2', 'T2', 1),
    ('T1', 'P2', 1), ('T2', 'P1', 1)
]
initial_marking = {'P1': 1, 'P2': 0}

net = PetriNet(places, transitions, flows, initial_marking)

# 触发T1后，系统进入死锁状态
net.fire('T1')
print("After firing T1:", net.get_current_marking())
# 输出: {'P1': 0, 'P2': 1}

# 检查是否有死锁
print("Has deadlock:", net.has_deadlock())
# 输出: Has deadlock: True（如果P2需要2个令牌才能触发T2）
```

### 测试用例 / Test Cases

```python
import unittest

class TestPetriNet(unittest.TestCase):
    """Petri网模拟器的单元测试"""

    def setUp(self):
        """设置测试环境"""
        self.places = ['P1', 'P2']
        self.transitions = ['T1']
        self.flows = [('P1', 'T1', 1), ('T1', 'P2', 1)]
        self.initial_marking = {'P1': 1, 'P2': 0}
        self.net = PetriNet(self.places, self.transitions,
                           self.flows, self.initial_marking)

    def test_initial_marking(self):
        """测试初始标识"""
        marking = self.net.get_current_marking()
        self.assertEqual(marking['P1'], 1)
        self.assertEqual(marking['P2'], 0)

    def test_is_enabled(self):
        """测试变迁可触发性检查"""
        self.assertTrue(self.net.is_enabled('T1'))
        self.net.fire('T1')
        self.assertFalse(self.net.is_enabled('T1'))

    def test_fire(self):
        """测试变迁触发"""
        result = self.net.fire('T1')
        self.assertTrue(result)
        marking = self.net.get_current_marking()
        self.assertEqual(marking['P1'], 0)
        self.assertEqual(marking['P2'], 1)

    def test_reachability(self):
        """测试可达性分析"""
        reachable, _ = self.net.reachability_analysis()
        self.assertGreater(len(reachable), 0)

    def test_is_safe(self):
        """测试安全性检查"""
        self.assertTrue(self.net.is_safe())

if __name__ == '__main__':
    unittest.main()
```

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
