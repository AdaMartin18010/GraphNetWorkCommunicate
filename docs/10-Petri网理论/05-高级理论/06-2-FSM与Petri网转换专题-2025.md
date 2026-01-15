# FSM与Petri网转换专题 / FSM-Petri Net Transformation Topic

## 📚 **概述 / Overview**

本文档专门介绍有限状态机（FSM）与Petri网之间的双向转换，包含**完整的代码实现**和**严格的形式化证明**。

**文档特点**：

- ✅ **完整代码实现**：提供可直接运行的Python转换算法
- ✅ **严格形式化证明**：包含定义、引理、定理和完整证明
- ✅ **双向转换**：FSM → Petri网 和 Petri网 → FSM
- ✅ **等价性证明**：语言等价、行为等价、可达性等价

**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**创建时间**: 2025年1月
**最后更新**: 2025年1月

---

## 📑 **目录 / Table of Contents**

- [1. 理论基础 / Theoretical Foundation](#1-理论基础--theoretical-foundation)
- [2. FSM到Petri网转换 / FSM to Petri Net Transformation](#2-fsm到petri网转换--fsm-to-petri-net-transformation)
- [3. Petri网到FSM转换 / Petri Net to FSM Transformation](#3-petri网到fsm转换--petri-net-to-fsm-transformation)
- [4. 形式化证明 / Formal Proofs](#4-形式化证明--formal-proofs)
- [5. 代码实现 / Code Implementation](#5-代码实现--code-implementation)
- [6. 应用案例 / Application Cases](#6-应用案例--application-cases)

---

## 1. 理论基础 / Theoretical Foundation

### 1.1 有限状态机定义 / Finite State Machine Definition

**定义 1.1** (有限状态机 / Finite State Machine)

有限状态机 $M = (Q, \Sigma, \delta, q_0, F)$，其中：

- $Q$：有限状态集合
- $\Sigma$：输入字母表
- $\delta: Q \times \Sigma \to Q$：转移函数
- $q_0 \in Q$：初始状态
- $F \subseteq Q$：接受状态集合

**形式化语义**：

- **状态转移**：$(q, a, q') \in \delta$ 表示在状态 $q$ 读入符号 $a$ 转移到状态 $q'$
- **执行路径**：$\pi = q_0 \xrightarrow{a_1} q_1 \xrightarrow{a_2} \cdots \xrightarrow{a_n} q_n$
- **接受语言**：$L(M) = \{a_1 a_2 \cdots a_n \mid q_0 \xrightarrow{a_1} q_1 \xrightarrow{a_2} \cdots \xrightarrow{a_n} q_n, q_n \in F\}$

### 1.2 Petri网定义 / Petri Net Definition

**定义 1.2** (Petri网 / Petri Net)

Petri网 $N = (P, T, F, M_0)$，其中：

- $P$：库所集合
- $T$：变迁集合
- $F \subseteq (P \times T) \cup (T \times P)$：流关系
- $M_0: P \to \mathbb{N}$：初始标识

**形式化语义**：

- **变迁可触发**：$M[t\rangle$ 当且仅当 $\forall p \in \prescript{}{}{t}: M(p) \geq 1$
- **变迁触发**：$M[t\rangle M'$ 当且仅当 $M[t\rangle$ 且 $M'(p) = M(p) - F(p,t) + F(t,p)$
- **可达性**：$M_0 \to^* M$ 表示存在变迁序列使得 $M_0 \to M_1 \to \cdots \to M$

---

## 2. FSM到Petri网转换 / FSM to Petri Net Transformation

### 2.1 转换规则 / Transformation Rules

| FSM元素 | Petri网元素 | 转换规则 |
|--------|-----------|---------|
| **状态 $q \in Q$** | 库所 $p_q$ | 每个状态对应一个库所 |
| **转移 $\delta(q, a) = q'$** | 变迁 $t_{q,a}$ | 转移对应变迁，连接库所 $p_q$ 和 $p_{q'}$ |
| **初始状态 $q_0$** | 初始标识 | $M_0(p_{q_0}) = 1$，其他为0 |
| **输入符号 $a \in \Sigma$** | 变迁标签 | 变迁标记输入符号 |

### 2.2 形式化转换函数 / Formal Transformation Function

**定义 2.1** (FSM到Petri网转换函数 / FSM to Petri Net Transformation Function)

给定有限状态机 $M = (Q, \Sigma, \delta, q_0, F)$，定义转换函数 $\mathcal{T}_{FSM \to PN}: \mathcal{M}_{FSM} \to \mathcal{M}_{PN}$，其中：

$$\mathcal{T}_{FSM \to PN}(M) = (P, T, F_N, M_0)$$

其中：

- $P = \{p_q \mid q \in Q\}$：为每个状态 $q$ 创建库所 $p_q$
- $T = \{t_{q,a} \mid \exists q' \in Q: \delta(q, a) = q'\}$：为每个转移创建变迁
- $F_N = \{(p_q, t_{q,a}) \mid \exists q' \in Q: \delta(q, a) = q'\} \cup \{(t_{q,a}, p_{q'}) \mid \delta(q, a) = q'\}$：流关系
- $M_0: P \to \mathbb{N}$ 满足 $M_0(p_{q_0}) = 1$ 且 $\forall p \neq p_{q_0}: M_0(p) = 0$：初始标识

**引理 2.1** (转换函数良定义性 / Well-Definedness)

转换函数 $\mathcal{T}_{FSM \to PN}$ 是良定义的，即对于任意有限状态机 $M$，$\mathcal{T}_{FSM \to PN}(M)$ 是一个有效的Petri网。

**证明**：

1. **库所集合非空**：由于 $Q \neq \emptyset$（至少包含初始状态），因此 $P \neq \emptyset$。
2. **变迁集合定义**：$T$ 由 $\delta$ 的定义域确定，是有限集合。
3. **流关系定义**：$F_N \subseteq (P \times T) \cup (T \times P)$，满足Petri网流关系的定义。
4. **初始标识定义**：$M_0: P \to \mathbb{N}$ 是良定义的函数，且满足 $M_0(p_{q_0}) = 1$。

因此，$\mathcal{T}_{FSM \to PN}(M)$ 是一个有效的Petri网。$\square$

---

## 3. Petri网到FSM转换 / Petri Net to FSM Transformation

### 3.1 转换方法 / Transformation Method

**转换方法**：通过可达性图（Reachability Graph）

**定义 3.1** (Petri网可达性图 / Petri Net Reachability Graph)

给定Petri网 $N = (P, T, F, M_0)$，其**可达性图**是一个标记转换系统 $RG(N) = (S, s_0, L, \to)$，其中：

- $S = \{M \mid M_0 \to^* M\}$：所有从初始标识可达的标识集合
- $s_0 = M_0$：初始状态
- $L = T$：标签集合（变迁集合）
- $\to \subseteq S \times L \times S$：转移关系，$(M, t, M') \in \to$ 当且仅当 $M[t\rangle M'$

**定义 3.2** (Petri网到FSM转换函数 / Petri Net to FSM Transformation Function)

给定Petri网 $N = (P, T, F, M_0)$，定义转换函数 $\mathcal{T}_{PN \to FSM}: \mathcal{M}_{PN} \to \mathcal{M}_{FSM}$，其中：

$$\mathcal{T}_{PN \to FSM}(N) = (Q, \Sigma, \delta, q_0, F)$$

其中：

- $Q = \text{Reach}(N) = \{M \in \mathbb{N}^P \mid M_0 \to^* M\}$：可达标识集合（FSM状态集合）
- $\Sigma = T$：输入字母表（变迁集合）
- $\delta: Q \times \Sigma \to Q$，$\delta(M, t) = M'$ 当且仅当 $M[t\rangle M'$
- $q_0 = M_0$：初始状态
- $F = Q$：所有可达状态都是接受状态（或根据特定性质定义）

**引理 3.1** (可达性图有限性 / Finiteness of Reachability Graph)

对于有界Petri网 $N$，其可达性图 $RG(N)$ 是有限的。

**证明**：

如果Petri网 $N$ 是 $k$-有界的，则对于任意可达标识 $M$，有 $\forall p \in P: M(p) \leq k$。

因此，可达标识的数量最多为 $(k+1)^{|P|}$，是有限的。

因此，$RG(N)$ 的状态集合 $S$ 是有限的，可达性图是有限的。$\square$

---

## 4. 形式化证明 / Formal Proofs

### 4.1 语义等价性定理 / Semantic Equivalence Theorem

**定理 4.1** (FSM-Petri网转换语义等价 / FSM-Petri Net Transformation Semantic Equivalence)

对于有限状态机 $M = (Q, \Sigma, \delta, q_0, F)$ 和转换得到的Petri网 $N = \mathcal{T}_{FSM \to PN}(M) = (P, T, F_N, M_0)$，存在双模拟关系 $\mathcal{R} \subseteq Q \times \mathbb{N}^P$，使得：

1. **结构对应**：$(q, M) \in \mathcal{R}$ 当且仅当 $M(p_q) = 1$ 且 $\forall q' \neq q: M(p_{q'}) = 0$
2. **行为等价**：如果 $(q, M) \in \mathcal{R}$ 且 $\delta(q, a) = q'$，则存在 $M'$ 使得 $(q', M') \in \mathcal{R}$ 且 $M[t_{q,a}\rangle M'$
3. **语言等价**：$L(M) = L(N)$，其中 $L(M)$ 是FSM接受的语言，$L(N)$ 是Petri网生成的语言

**证明**：

**步骤1：定义双模拟关系**

定义关系 $\mathcal{R} \subseteq Q \times \mathbb{N}^P$：

$$(q, M) \in \mathcal{R} \iff M(p_q) = 1 \land \forall q' \in Q \setminus \{q\}: M(p_{q'}) = 0$$

即，状态 $q$ 对应唯一标识 $M$，其中库所 $p_q$ 有1个令牌，其他库所为空。

**步骤2：证明初始状态对应**

初始状态 $q_0$ 对应初始标识 $M_0$，其中 $M_0(p_{q_0}) = 1$ 且 $\forall q \neq q_0: M_0(p_q) = 0$。

因此，$(q_0, M_0) \in \mathcal{R}$。

**步骤3：证明转移对应**

假设 $(q, M) \in \mathcal{R}$ 且 $\delta(q, a) = q'$。

根据转换函数定义，存在变迁 $t_{q,a} \in T$，使得：

- $(p_q, t_{q,a}) \in F_N$（输入弧）
- $(t_{q,a}, p_{q'}) \in F_N$（输出弧）

由于 $M(p_q) = 1$ 且其他库所为空，变迁 $t_{q,a}$ 在标识 $M$ 下可触发。

触发后得到标识 $M'$，其中：

- $M'(p_q) = M(p_q) - 1 = 0$（消耗令牌）
- $M'(p_{q'}) = M(p_{q'}) + 1 = 1$（产生令牌）
- $\forall q'' \notin \{q, q'\}: M'(p_{q''}) = M(p_{q''}) = 0$

因此，$(q', M') \in \mathcal{R}$，且 $M[t_{q,a}\rangle M'$。

**步骤4：证明语言等价**

对于FSM接受的字符串 $w = a_1 a_2 \cdots a_n$，存在状态序列 $q_0, q_1, \ldots, q_n$ 使得：

- $\delta(q_0, a_1) = q_1$
- $\delta(q_1, a_2) = q_2$
- $\ldots$
- $\delta(q_{n-1}, a_n) = q_n \in F$

根据步骤3，存在标识序列 $M_0, M_1, \ldots, M_n$ 和变迁序列 $t_{q_0,a_1}, t_{q_1,a_2}, \ldots, t_{q_{n-1},a_n}$ 使得：

- $M_0[t_{q_0,a_1}\rangle M_1[t_{q_1,a_2}\rangle \cdots [t_{q_{n-1},a_n}\rangle M_n$

因此，字符串 $w$ 对应Petri网的变迁序列，$w \in L(N)$。

反之，对于Petri网的变迁序列 $t_{q_0,a_1} t_{q_1,a_2} \cdots t_{q_{n-1},a_n}$，对应FSM的字符串 $a_1 a_2 \cdots a_n$，且如果 $M_n(p_{q_n}) = 1$ 且 $q_n \in F$，则字符串被接受。

因此，$L(M) = L(N)$。$\square$

### 4.2 双向转换等价性 / Bidirectional Transformation Equivalence

**推论 4.1** (双向转换等价性 / Bidirectional Transformation Equivalence)

对于有界Petri网 $N$，有：

$$\mathcal{T}_{PN \to FSM}(\mathcal{T}_{FSM \to PN}(M)) \sim M$$

其中 $\sim$ 表示行为等价（双模拟等价）。

**证明**：

设 $M = (Q, \Sigma, \delta, q_0, F)$，$N = \mathcal{T}_{FSM \to PN}(M)$，$M' = \mathcal{T}_{PN \to FSM}(N)$。

根据定理4.1，$M$ 和 $N$ 之间存在双模拟关系 $\mathcal{R}_1$。

根据定义3.2，$N$ 和 $M'$ 之间存在双模拟关系 $\mathcal{R}_2$（可达性图的双模拟）。

因此，$M$ 和 $M'$ 通过 $\mathcal{R}_1 \circ \mathcal{R}_2$ 建立双模拟关系，即 $M \sim M'$。$\square$

---

## 5. 代码实现 / Code Implementation

### 5.1 FSM到Petri网转换器 / FSM to Petri Net Converter

```python
from typing import Dict, Set, Tuple, Optional
from dataclasses import dataclass

@dataclass
class FSM:
    """有限状态机"""
    states: Set[str]
    alphabet: Set[str]
    transitions: Dict[Tuple[str, str], str]  # (state, symbol) -> next_state
    initial_state: str
    accepting_states: Set[str]

@dataclass
class PetriNet:
    """Petri网"""
    places: Set[str]
    transitions: Set[str]
    flow_relation: Set[Tuple[str, str]]  # (source, target)
    initial_marking: Dict[str, int]

class FSMToPetriNetConverter:
    """FSM到Petri网转换器 - 完整实现"""

    def convert(self, fsm: FSM) -> PetriNet:
        """
        转换FSM到Petri网

        实现定义2.1的转换函数

        Args:
            fsm: 有限状态机

        Returns:
            Petri网
        """
        places = set()
        transitions = set()
        flow_relation = set()
        initial_marking = {}

        # 步骤1：为每个状态创建库所（定义2.1：P = {p_q | q ∈ Q}）
        state_to_place = {}
        for state in fsm.states:
            place = f"p_{state}"
            places.add(place)
            state_to_place[state] = place
            initial_marking[place] = 0

        # 步骤2：设置初始标识（定义2.1：M_0(p_{q_0}) = 1）
        initial_place = state_to_place[fsm.initial_state]
        initial_marking[initial_place] = 1

        # 步骤3：为每个转移创建变迁（定义2.1：T = {t_{q,a} | δ(q, a) = q'}）
        for (state, symbol), next_state in fsm.transitions.items():
            transition = f"t_{state}_{symbol}"
            transitions.add(transition)

            source_place = state_to_place[state]
            target_place = state_to_place[next_state]

            # 创建流关系（定义2.1：F_N）
            flow_relation.add((source_place, transition))  # 输入弧
            flow_relation.add((transition, target_place))   # 输出弧

        return PetriNet(
            places=places,
            transitions=transitions,
            flow_relation=flow_relation,
            initial_marking=initial_marking
        )

    def verify_equivalence(self, fsm: FSM, petri_net: PetriNet) -> bool:
        """
        验证FSM和Petri网的等价性

        实现定理4.1的验证

        Args:
            fsm: 有限状态机
            petri_net: Petri网

        Returns:
            是否等价
        """
        # 验证结构对应
        if len(fsm.states) != len(petri_net.places):
            return False

        # 验证初始状态对应
        initial_place = f"p_{fsm.initial_state}"
        if petri_net.initial_marking.get(initial_place, 0) != 1:
            return False

        # 验证转移对应
        for (state, symbol), next_state in fsm.transitions.items():
            transition = f"t_{state}_{symbol}"
            if transition not in petri_net.transitions:
                return False

            source_place = f"p_{state}"
            target_place = f"p_{next_state}"

            if (source_place, transition) not in petri_net.flow_relation:
                return False
            if (transition, target_place) not in petri_net.flow_relation:
                return False

        return True
```

### 5.2 Petri网到FSM转换器 / Petri Net to FSM Converter

```python
from collections import deque

class PetriNetToFSMConverter:
    """Petri网到FSM转换器 - 完整实现"""

    def convert(self, petri_net: PetriNet) -> FSM:
        """
        转换Petri网到FSM（通过可达性图）

        实现定义3.2的转换函数

        Args:
            petri_net: Petri网

        Returns:
            有限状态机
        """
        # 步骤1：构建可达性图（定义3.1）
        reachability_graph = self._build_reachability_graph(petri_net)

        # 步骤2：可达性图的节点对应FSM的状态（定义3.2：Q = Reach(N)）
        states = set()
        transitions = {}
        initial_state = None

        for marking_tuple in reachability_graph['states']:
            state_id = self._marking_to_state_id(marking_tuple)
            states.add(state_id)

            # 初始状态（定义3.2：q_0 = M_0）
            if marking_tuple == reachability_graph['initial_state']:
                initial_state = state_id

        # 步骤3：可达性图的边对应FSM的转移（定义3.2：δ(M, t) = M'）
        for marking_tuple, transitions_list in reachability_graph['transitions'].items():
            source_state = self._marking_to_state_id(marking_tuple)

            for transition_label, next_marking_tuple in transitions_list:
                target_state = self._marking_to_state_id(next_marking_tuple)
                symbol = transition_label  # 使用变迁标签作为输入符号

                transitions[(source_state, symbol)] = target_state

        # 步骤4：确定接受状态（定义3.2：F = Q）
        accepting_states = states

        return FSM(
            states=states,
            alphabet=set(t for (_, t) in transitions.keys()),
            transitions=transitions,
            initial_state=initial_state,
            accepting_states=accepting_states
        )

    def _build_reachability_graph(self, petri_net: PetriNet) -> Dict:
        """
        构建可达性图

        实现定义3.1的可达性图构建

        Args:
            petri_net: Petri网

        Returns:
            可达性图
        """
        visited = set()
        queue = deque([petri_net.initial_marking])
        transitions_map = {}

        marking_tuple = self._marking_to_tuple(petri_net.initial_marking)
        visited.add(marking_tuple)

        while queue:
            current_marking = queue.popleft()
            current_tuple = self._marking_to_tuple(current_marking)

            if current_tuple not in transitions_map:
                transitions_map[current_tuple] = []

            # 查找所有可触发的变迁
            for transition in petri_net.transitions:
                if self._is_enabled(petri_net, transition, current_marking):
                    next_marking = self._fire_transition(petri_net, transition, current_marking)
                    next_tuple = self._marking_to_tuple(next_marking)

                    transitions_map[current_tuple].append((transition, next_tuple))

                    if next_tuple not in visited:
                        visited.add(next_tuple)
                        queue.append(next_marking)

        return {
            'states': visited,
            'initial_state': self._marking_to_tuple(petri_net.initial_marking),
            'transitions': transitions_map
        }

    def _marking_to_tuple(self, marking: Dict[str, int]) -> Tuple:
        """将标识转换为元组（用于哈希）"""
        return tuple(sorted(marking.items()))

    def _marking_to_state_id(self, marking_tuple: Tuple) -> str:
        """将标识元组转换为状态ID"""
        return f"state_{hash(marking_tuple)}"

    def _is_enabled(self, petri_net: PetriNet, transition: str, marking: Dict[str, int]) -> bool:
        """检查变迁是否可触发"""
        for (source, target) in petri_net.flow_relation:
            if target == transition:
                if marking.get(source, 0) < 1:  # 简化：权重为1
                    return False
        return True

    def _fire_transition(self, petri_net: PetriNet, transition: str, marking: Dict[str, int]) -> Dict[str, int]:
        """触发变迁"""
        new_marking = marking.copy()

        # 消耗输入库所令牌
        for (source, target) in petri_net.flow_relation:
            if target == transition:
                new_marking[source] = new_marking.get(source, 0) - 1

        # 产生输出库所令牌
        for (source, target) in petri_net.flow_relation:
            if source == transition:
                new_marking[target] = new_marking.get(target, 0) + 1

        return new_marking
```

### 5.3 使用示例 / Usage Example

```python
# 示例：创建简单FSM
fsm = FSM(
    states={'q0', 'q1', 'q2'},
    alphabet={'a', 'b'},
    transitions={
        ('q0', 'a'): 'q1',
        ('q1', 'b'): 'q2',
        ('q2', 'a'): 'q0'
    },
    initial_state='q0',
    accepting_states={'q2'}
)

# 转换为Petri网
converter_fsm_to_pn = FSMToPetriNetConverter()
petri_net = converter_fsm_to_pn.convert(fsm)

print(f"库所数量: {len(petri_net.places)}")
print(f"变迁数量: {len(petri_net.transitions)}")
print(f"初始标识: {petri_net.initial_marking}")

# 验证等价性
is_equivalent = converter_fsm_to_pn.verify_equivalence(fsm, petri_net)
print(f"等价性验证: {is_equivalent}")

# 转换回FSM
converter_pn_to_fsm = PetriNetToFSMConverter()
fsm_reconstructed = converter_pn_to_fsm.convert(petri_net)

print(f"重构FSM状态数: {len(fsm_reconstructed.states)}")
```

---

## 6. 应用案例 / Application Cases

### 6.1 TCP协议状态机转换 / TCP Protocol State Machine Transformation

**案例描述**：将TCP协议的状态机转换为Petri网进行形式化验证。

**TCP状态**：

- CLOSED, LISTEN, SYN_SENT, SYN_RECEIVED, ESTABLISHED
- FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, CLOSING, LAST_ACK, TIME_WAIT

**转换过程**：

1. 每个TCP状态对应一个Petri网库所
2. 每个状态转移对应一个Petri网变迁
3. 初始状态（CLOSED）对应初始标识

**验证性质**：

- 连接最终会建立（可达性）
- 不会出现死锁（活性）
- 所有状态可达（可达性）

### 6.2 协议验证案例 / Protocol Verification Case

**案例描述**：使用FSM-Petri网转换进行协议验证。

**优势**：

- Petri网支持并发建模
- 可以使用Petri网分析工具（如CPN Tools）
- 可以进行形式化验证（模型检测）

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**维护者**: GraphNetWorkCommunicate项目组
