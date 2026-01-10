# Petri网算法详细选择指南 / Detailed Petri Net Algorithm Selection Guide

## 📚 **概述 / Overview**

**文档目的**: 提供Petri网算法的详细选择指南，包括算法原理、复杂度分析、适用场景、实现示例。

**适用对象**: 算法工程师、形式化方法研究人员、系统验证工程师

---

## 🎯 **一、可达性分析算法选择 / Part 1: Reachability Analysis Algorithm Selection**

### 1.1 可达图构建算法

**算法原理**:

- 从初始标识开始，递归构建所有可达状态
- 使用深度优先或广度优先搜索
- 检测死锁状态（无输出变迁的状态）

**复杂度**:

- 时间复杂度: O(2^n)（n为状态数，可能指数爆炸）
- 空间复杂度: O(2^n)

**适用场景**:

- 小规模Petri网（状态数 < 10^4）
- 需要完整状态空间分析
- 死锁检测

**实现示例**:

```python
class ReachabilityGraph:
    def __init__(self, petri_net, initial_marking):
        self.petri_net = petri_net
        self.initial_marking = initial_marking
        self.states = {}
        self.transitions = []
        self.deadlock_states = []

    def build_reachability_graph(self):
        """
        构建可达图
        """
        queue = [self.initial_marking]
        visited = set()
        visited.add(self._marking_to_tuple(self.initial_marking))

        while queue:
            current_marking = queue.pop(0)
            current_tuple = self._marking_to_tuple(current_marking)

            # 检查死锁
            enabled_transitions = self._get_enabled_transitions(current_marking)
            if not enabled_transitions:
                self.deadlock_states.append(current_marking)

            # 生成后继状态
            for transition in enabled_transitions:
                new_marking = self._fire_transition(current_marking, transition)
                new_tuple = self._marking_to_tuple(new_marking)

                # 记录状态转换
                self.transitions.append((current_tuple, transition, new_tuple))

                # 添加新状态
                if new_tuple not in visited:
                    visited.add(new_tuple)
                    queue.append(new_marking)
                    self.states[new_tuple] = new_marking

        return self.states, self.transitions

    def _get_enabled_transitions(self, marking):
        """
        获取使能变迁
        """
        enabled = []
        for transition in self.petri_net.transitions:
            if self._is_enabled(transition, marking):
                enabled.append(transition)
        return enabled

    def _is_enabled(self, transition, marking):
        """
        检查变迁是否使能
        """
        for place, weight in transition.input_arcs.items():
            if marking[place] < weight:
                return False
        return True

    def _fire_transition(self, marking, transition):
        """
        触发变迁
        """
        new_marking = marking.copy()

        # 消耗输入库所的令牌
        for place, weight in transition.input_arcs.items():
            new_marking[place] -= weight

        # 产生输出库所的令牌
        for place, weight in transition.output_arcs.items():
            new_marking[place] += weight

        return new_marking

    def _marking_to_tuple(self, marking):
        """
        将标识转换为元组（用于哈希）
        """
        return tuple(sorted(marking.items()))
```

### 1.2 覆盖树算法

**算法原理**:

- 可达图的改进，处理无界Petri网
- 使用ω符号表示无界库所
- 可以检测有界性

**复杂度**:

- 时间复杂度: O(2^n)
- 空间复杂度: O(2^n)

**适用场景**:

- 无界Petri网
- 有界性检测
- 中小规模网

**实现示例**:

```python
class CoverabilityTree:
    def __init__(self, petri_net, initial_marking):
        self.petri_net = petri_net
        self.initial_marking = initial_marking
        self.tree = {}
        self.omega_symbol = float('inf')  # ω符号

    def build_coverability_tree(self):
        """
        构建覆盖树
        """
        root = self.initial_marking
        self.tree[root] = {'children': [], 'marking': root}
        queue = [root]

        while queue:
            current = queue.pop(0)
            enabled = self._get_enabled_transitions(current)

            for transition in enabled:
                new_marking = self._fire_transition(current, transition)

                # 检查是否被覆盖
                ancestor = self._find_ancestor(new_marking, current)
                if ancestor:
                    # 使用ω标记无界库所
                    new_marking = self._apply_omega(new_marking, ancestor)

                # 添加新节点
                self.tree[new_marking] = {
                    'children': [],
                    'marking': new_marking,
                    'parent': current
                }
                self.tree[current]['children'].append(new_marking)

                # 如果不是终止节点，继续扩展
                if not self._is_terminal(new_marking):
                    queue.append(new_marking)

        return self.tree

    def _find_ancestor(self, marking, current):
        """
        查找覆盖当前标识的祖先
        """
        # 向上遍历树，查找覆盖关系
        parent = self.tree[current].get('parent')
        while parent:
            if self._covers(parent, marking):
                return parent
            parent = self.tree[parent].get('parent')
        return None

    def _covers(self, marking1, marking2):
        """
        检查marking1是否覆盖marking2
        """
        for place in marking2:
            if marking1.get(place, 0) < marking2[place]:
                return False
        return True

    def _apply_omega(self, marking, ancestor):
        """
        应用ω符号
        """
        new_marking = marking.copy()
        for place in marking:
            if ancestor.get(place, 0) < marking[place]:
                new_marking[place] = self.omega_symbol
        return new_marking
```

---

## 📊 **二、不变量分析算法选择 / Part 2: Invariant Analysis Algorithm Selection**

### 2.1 S-不变量计算

**算法原理**:

- S-不变量：库所令牌数的线性组合守恒
- 求解线性方程组 C·y = 0
- C为关联矩阵

**复杂度**:

- 时间复杂度: O(n³)（n为库所数，使用高斯消元）
- 空间复杂度: O(n²)

**适用场景**:

- 任意规模Petri网
- 资源守恒验证
- 系统不变量证明

**实现示例**:

```python
import numpy as np
from scipy.linalg import null_space

class SInvariantCalculator:
    def __init__(self, petri_net):
        self.petri_net = petri_net
        self.incidence_matrix = self._build_incidence_matrix()

    def _build_incidence_matrix(self):
        """
        构建关联矩阵
        """
        places = list(self.petri_net.places)
        transitions = list(self.petri_net.transitions)

        matrix = np.zeros((len(places), len(transitions)))

        for i, place in enumerate(places):
            for j, transition in enumerate(transitions):
                # 输出权重 - 输入权重
                output_weight = transition.output_arcs.get(place, 0)
                input_weight = transition.input_arcs.get(place, 0)
                matrix[i][j] = output_weight - input_weight

        return matrix

    def calculate_s_invariants(self):
        """
        计算S-不变量
        """
        # 求解 C·y = 0
        null_space_vectors = null_space(self.incidence_matrix)

        # 转换为整数不变量
        invariants = []
        for vector in null_space_vectors.T:
            # 归一化为整数
            integer_invariant = self._normalize_to_integers(vector)
            if integer_invariant is not None:
                invariants.append(integer_invariant)

        return invariants

    def _normalize_to_integers(self, vector):
        """
        归一化为整数向量
        """
        # 找到最小公倍数
        non_zero = [abs(v) for v in vector if abs(v) > 1e-10]
        if not non_zero:
            return None

        # 简化为整数
        min_val = min(non_zero)
        normalized = vector / min_val

        # 检查是否为整数
        if np.allclose(normalized, np.round(normalized)):
            return np.round(normalized).astype(int)
        return None

    def verify_invariant(self, invariant, initial_marking, current_marking):
        """
        验证不变量在标识中是否成立
        """
        places = list(self.petri_net.places)

        initial_sum = sum(invariant[i] * initial_marking[places[i]]
                         for i in range(len(places)))
        current_sum = sum(invariant[i] * current_marking[places[i]]
                         for i in range(len(places)))

        return abs(initial_sum - current_sum) < 1e-10
```

### 2.2 T-不变量计算

**算法原理**:

- T-不变量：变迁触发序列的线性组合
- 求解线性方程组 C^T·x = 0
- 表示系统的循环行为

**复杂度**:

- 时间复杂度: O(m³)（m为变迁数）
- 空间复杂度: O(m²)

**适用场景**:

- 任意规模Petri网
- 循环行为验证
- 公平性验证

**实现示例**:

```python
class TInvariantCalculator:
    def __init__(self, petri_net):
        self.petri_net = petri_net
        self.incidence_matrix = self._build_incidence_matrix()

    def _build_incidence_matrix(self):
        """
        构建关联矩阵
        """
        places = list(self.petri_net.places)
        transitions = list(self.petri_net.transitions)

        matrix = np.zeros((len(places), len(transitions)))

        for i, place in enumerate(places):
            for j, transition in enumerate(transitions):
                output_weight = transition.output_arcs.get(place, 0)
                input_weight = transition.input_arcs.get(place, 0)
                matrix[i][j] = output_weight - input_weight

        return matrix

    def calculate_t_invariants(self):
        """
        计算T-不变量
        """
        # 求解 C^T·x = 0
        transposed = self.incidence_matrix.T
        null_space_vectors = null_space(transposed)

        # 转换为整数不变量
        invariants = []
        for vector in null_space_vectors.T:
            integer_invariant = self._normalize_to_integers(vector)
            if integer_invariant is not None:
                invariants.append(integer_invariant)

        return invariants

    def _normalize_to_integers(self, vector):
        """
        归一化为整数向量
        """
        non_zero = [abs(v) for v in vector if abs(v) > 1e-10]
        if not non_zero:
            return None

        min_val = min(non_zero)
        normalized = vector / min_val

        if np.allclose(normalized, np.round(normalized)):
            return np.round(normalized).astype(int)
        return None
```

---

## 🔧 **三、活性分析算法选择 / Part 3: Liveness Analysis Algorithm Selection**

### 3.1 活性检测算法

**算法原理**:

- 活性定义：变迁在任意可达状态都可能被触发
- 基于可达图分析
- 检测死锁状态

**复杂度**:

- 时间复杂度: O(2^n × m)（n为状态数，m为变迁数）
- 空间复杂度: O(2^n)

**适用场景**:

- 小规模Petri网
- 死锁检测
- 协议活性验证

**实现示例**:

```python
class LivenessAnalyzer:
    def __init__(self, reachability_graph):
        self.reachability_graph = reachability_graph
        self.liveness_results = {}

    def analyze_liveness(self):
        """
        分析所有变迁的活性
        """
        states = self.reachability_graph.states
        transitions = self.reachability_graph.petri_net.transitions

        for transition in transitions:
            is_live = self._check_transition_liveness(transition, states)
            self.liveness_results[transition] = is_live

        return self.liveness_results

    def _check_transition_liveness(self, transition, states):
        """
        检查变迁的活性
        """
        # 检查是否存在从任意状态到使能该变迁的状态的路径
        for state in states.values():
            if not self._can_reach_enabled_state(state, transition, states):
                return False
        return True

    def _can_reach_enabled_state(self, start_state, transition, states):
        """
        检查是否可以从start_state到达使能transition的状态
        """
        visited = set()
        queue = [start_state]

        while queue:
            current = queue.pop(0)
            current_tuple = self._marking_to_tuple(current)

            if current_tuple in visited:
                continue
            visited.add(current_tuple)

            # 检查当前状态是否使能transition
            if self._is_enabled(transition, current):
                return True

            # 继续搜索
            enabled = self._get_enabled_transitions(current)
            for t in enabled:
                new_state = self._fire_transition(current, t)
                queue.append(new_state)

        return False
```

---

## 🔬 **四、性能分析算法选择 / Part 4: Performance Analysis Algorithm Selection**

### 4.1 随机Petri网分析

**算法原理**:

- 将Petri网转换为连续时间马尔可夫链（CTMC）
- 求解稳态概率分布
- 计算性能指标（吞吐量、延迟等）

**复杂度**:

- 时间复杂度: O(n³)（n为状态数）
- 空间复杂度: O(n²)

**适用场景**:

- 性能分析
- 吞吐量计算
- 延迟分析

**实现示例**:

```python
import numpy as np
from scipy.linalg import solve

class StochasticPetriNetAnalyzer:
    def __init__(self, stochastic_petri_net):
        self.spn = stochastic_petri_net
        self.ctmc = self._build_ctmc()

    def _build_ctmc(self):
        """
        构建连续时间马尔可夫链
        """
        # 构建状态空间
        states = self._build_state_space()

        # 构建转移率矩阵
        rate_matrix = self._build_rate_matrix(states)

        return {
            'states': states,
            'rate_matrix': rate_matrix
        }

    def calculate_steady_state(self):
        """
        计算稳态概率分布
        """
        Q = self.ctmc['rate_matrix']
        n = Q.shape[0]

        # 构建线性方程组：π·Q = 0, Σπ = 1
        A = np.vstack([Q.T, np.ones(n)])
        b = np.zeros(n + 1)
        b[-1] = 1

        # 求解
        pi = solve(A, b)

        return pi

    def calculate_throughput(self, transition):
        """
        计算变迁的吞吐量
        """
        pi = self.calculate_steady_state()

        throughput = 0
        for i, state in enumerate(self.ctmc['states']):
            if self._is_enabled(transition, state):
                rate = transition.firing_rate
                throughput += pi[i] * rate

        return throughput
```

---

## 📈 **五、算法选择决策表 / Part 5: Algorithm Selection Decision Table**

### 5.1 可达性分析算法选择表

| 场景 | 网规模 | 有界性 | 推荐算法 | 理由 |
|------|--------|--------|----------|------|
| 死锁检测 | 小(<10^4状态) | 有界 | 可达图 | 精确完整 |
| 死锁检测 | 中 | 无界 | 覆盖树 | 处理无界 |
| 状态空间分析 | 小 | 任意 | 可达图 | 完整信息 |
| 状态空间分析 | 大 | 任意 | BDD符号化 | 避免爆炸 |

### 5.2 不变量分析算法选择表

| 场景 | 网规模 | 需求 | 推荐算法 | 理由 |
|------|--------|------|----------|------|
| 资源守恒验证 | 任意 | S-不变量 | 线性方程求解 | 多项式复杂度 |
| 循环行为验证 | 任意 | T-不变量 | 线性方程求解 | 多项式复杂度 |
| 系统不变量 | 任意 | 综合 | S/T不变量 | 完整分析 |

### 5.3 活性分析算法选择表

| 场景 | 网规模 | 网类型 | 推荐算法 | 理由 |
|------|--------|--------|----------|------|
| 死锁检测 | 小 | 任意 | 可达图+活性检测 | 精确 |
| 活性验证 | 小 | 自由选择网 | 多项式算法 | 高效 |
| 活性验证 | 中 | 一般网 | 可达图分析 | 通用 |

---

## 💡 **六、最佳实践建议 / Part 6: Best Practice Recommendations**

### 6.1 算法选择原则

1. **规模优先**: 根据网规模选择算法
2. **精度权衡**: 在精度和效率间权衡
3. **工具利用**: 使用成熟的Petri网工具（CPN Tools、GreatSPN）

### 6.2 性能优化建议

1. **状态空间优化**: 使用BDD符号化表示
2. **偏序规约**: 利用并发性减少状态数
3. **对称性约简**: 利用网的对称性

---

## 📚 **七、参考文档 / Part 7: Reference Documents**

### 7.1 相关文档

- [算法选择认知路径概述](./00-算法选择认知路径概述.md)
- [Petri网理论模块](../../10-Petri网理论/README.md)

### 7.2 工具参考

- [CPN Tools文档](https://cpntools.org/documentation/)
- [GreatSPN文档](http://www.di.unito.it/~greatspn/)

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**最后更新**: 2025年1月
**状态**: ✅ 完成
**维护者**: GraphNetWorkCommunicate项目组
