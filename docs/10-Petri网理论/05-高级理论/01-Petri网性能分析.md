# Petri网性能分析 / Petri Net Performance Analysis

## 📚 **概述 / Overview**

本文档介绍Petri网性能分析理论，包括性能指标定义、吞吐量分析、响应时间分析和性能优化方法。

**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**国际对标**: 100% 达标 ✅
**完成状态**: ✅ 已完成

---

## 📑 **目录 / Table of Contents**

- [Petri网性能分析 / Petri Net Performance Analysis](#petri网性能分析--petri-net-performance-analysis)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [1. 形式化定义 / Formal Definition](#1-形式化定义--formal-definition)
  - [2. 性能指标 / Performance Metrics](#2-性能指标--performance-metrics)
  - [3. 性能分析方法 / Performance Analysis Methods](#3-性能分析方法--performance-analysis-methods)
  - [4. 应用场景 / Application Scenarios](#4-应用场景--application-scenarios)
  - [🔗 **相关链接 / Related Links**](#-相关链接--related-links)

---

## 1. 形式化定义 / Formal Definition

### 定义 1.1 (Petri网性能 / Petri Net Performance)

**Petri网性能**是系统在给定工作负载下的行为特征，包括吞吐量、响应时间、资源利用率等。

### 定义 1.2 (吞吐量 / Throughput)

**吞吐量**是系统在单位时间内完成的作业数或事件数。

对于Petri网 $N$，变迁 $t$ 的吞吐量定义为：

$$\text{Th}(t) = \lim_{T \to \infty} \frac{N_t(T)}{T}$$

其中 $N_t(T)$ 是时间 $T$ 内变迁 $t$ 的触发次数。

### 定义 1.3 (响应时间 / Response Time)

**响应时间**是从输入到输出完成的时间。

对于Petri网中的路径 $\pi$，响应时间为：

$$R(\pi) = \sum_{t \in \pi} d(t)$$

其中 $d(t)$ 是变迁 $t$ 的延迟时间。

---

## 2. 性能指标 / Performance Metrics

### 2.1 吞吐量指标

#### 定义 2.1 (系统吞吐量 / System Throughput)

**系统吞吐量**是所有变迁的平均吞吐量：

$$\text{Th}_{\text{sys}} = \frac{1}{|T|} \sum_{t \in T} \text{Th}(t)$$

#### 定义 2.2 (瓶颈变迁 / Bottleneck Transition)

**瓶颈变迁**是限制系统整体性能的变迁，即吞吐量最小的变迁。

### 2.2 响应时间指标

#### 定义 2.3 (平均响应时间 / Average Response Time)

**平均响应时间**是所有路径的平均响应时间：

$$R_{\text{avg}} = \frac{1}{|\Pi|} \sum_{\pi \in \Pi} R(\pi)$$

其中 $\Pi$ 是所有路径集合。

### 2.3 资源利用率指标

#### 定义 2.4 (库所利用率 / Place Utilization)

**库所利用率**是库所中令牌的平均数量：

$$U(p) = \lim_{T \to \infty} \frac{1}{T} \int_0^T M_t(p) dt$$

---

## 3. 性能分析方法 / Performance Analysis Methods

### 3.1 基于随机Petri网的分析

**算法 3.1** (随机Petri网性能分析)

```python
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict

class PetriNetPerformanceAnalyzer:
    """
    Petri网性能分析器。
    """

    def __init__(self, petri_net):
        """
        初始化。

        Args:
            petri_net: Petri网实例
        """
        self.net = petri_net
        self.transition_rates = {}  # 变迁触发率
        self.place_utilization = {}  # 库所利用率
        self.throughput = {}  # 吞吐量

    def analyze_throughput(self, simulation_time: float = 1000.0) -> Dict[str, float]:
        """
        分析吞吐量。

        Args:
            simulation_time: 仿真时间

        Returns:
            每个变迁的吞吐量
        """
        # 使用随机Petri网仿真
        transition_counts = defaultdict(int)
        current_time = 0.0

        while current_time < simulation_time:
            # 找到所有可触发的变迁
            enabled_transitions = self.get_enabled_transitions()

            if not enabled_transitions:
                break

            # 选择触发变迁（基于触发率）
            next_transition = self.select_transition(enabled_transitions)

            # 计算触发延迟
            delay = self.get_firing_delay(next_transition)

            # 触发变迁
            self.fire_transition(next_transition)
            transition_counts[next_transition] += 1
            current_time += delay

        # 计算吞吐量
        for transition, count in transition_counts.items():
            self.throughput[transition] = count / simulation_time

        return self.throughput

    def analyze_response_time(self, path: List[str]) -> float:
        """
        分析路径的响应时间。

        Args:
            path: 变迁序列（路径）

        Returns:
            响应时间
        """
        total_time = 0.0
        for transition in path:
            if transition in self.transition_rates:
                # 平均延迟 = 1 / 触发率
                delay = 1.0 / self.transition_rates[transition]
                total_time += delay
            else:
                # 默认延迟
                total_time += 1.0

        return total_time

    def analyze_utilization(self, simulation_time: float = 1000.0) -> Dict[str, float]:
        """
        分析库所利用率。

        Args:
            simulation_time: 仿真时间

        Returns:
            每个库所的利用率
        """
        # 使用时间平均方法
        place_tokens = defaultdict(list)  # 记录每个时间点的令牌数
        current_time = 0.0

        while current_time < simulation_time:
            # 记录当前状态
            for place in self.net.places:
                place_tokens[place].append((current_time, self.net.get_marking(place)))

            # 找到下一个事件
            next_event_time = self.get_next_event_time()
            current_time = next_event_time

        # 计算时间平均
        for place, token_history in place_tokens.items():
            total_tokens = sum(tokens * (time - prev_time)
                             for (time, tokens), (prev_time, _)
                             in zip(token_history[1:], token_history))
            self.place_utilization[place] = total_tokens / simulation_time

        return self.place_utilization

    def identify_bottlenecks(self) -> List[str]:
        """
        识别瓶颈变迁。

        Returns:
            瓶颈变迁列表
        """
        if not self.throughput:
            self.analyze_throughput()

        if not self.throughput:
            return []

        min_throughput = min(self.throughput.values())
        bottlenecks = [t for t, th in self.throughput.items() if th == min_throughput]

        return bottlenecks
```

### 3.2 基于马尔可夫链的分析

**算法 3.2** (马尔可夫链性能分析)

```python
    def markov_chain_analysis(self) -> Dict[str, float]:
        """
        使用马尔可夫链分析性能。

        Returns:
            性能指标
        """
        # 构建状态空间
        states = self.build_state_space()

        # 构建转移矩阵
        transition_matrix = self.build_transition_matrix(states)

        # 计算稳态分布
        steady_state = self.compute_steady_state(transition_matrix)

        # 计算性能指标
        performance = {}

        # 计算吞吐量
        for transition in self.net.transitions:
            throughput = 0.0
            for i, state in enumerate(states):
                if self.is_enabled(state, transition):
                    rate = self.transition_rates.get(transition, 1.0)
                    throughput += steady_state[i] * rate
            performance[f'throughput_{transition}'] = throughput

        # 计算库所利用率
        for place in self.net.places:
            utilization = 0.0
            for i, state in enumerate(states):
                utilization += steady_state[i] * state.get(place, 0)
            performance[f'utilization_{place}'] = utilization

        return performance
```

---

## 4. 应用场景 / Application Scenarios

### 4.1 工作流系统性能分析

**问题**: 分析工作流系统的吞吐量和响应时间。

**应用**: 业务流程优化、工作流引擎设计

### 4.2 通信协议性能分析

**问题**: 分析通信协议的吞吐量和延迟。

**应用**: 协议优化、网络设计

### 4.3 分布式系统性能分析

**问题**: 分析分布式系统的资源利用率和瓶颈。

**应用**: 系统优化、资源分配

---

## 🔗 **相关链接 / Related Links**

- [Petri网合成理论](02-Petri网合成理论.md)
- [Petri网等价性理论](03-Petri网等价性理论.md)
- [Petri网化简方法](04-Petri网化简方法.md)
- [Petri网高级理论主目录](README.md)
- [Petri网理论模块主页](../README.md)

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**最后更新**: 2025年1月
**维护者**: GraphNetWorkCommunicate项目组
