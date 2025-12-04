# Petri网的定义 / Petri Net Definition

## 📚 **概述 / Overview**

本文档介绍Petri网的形式化定义和基本概念。

---

## 📑 **目录 / Table of Contents**

- [Petri网的定义 / Petri Net Definition](#petri网的定义--petri-net-definition)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [1. Petri网的定义 / Petri Net Definition](#1-petri网的定义--petri-net-definition)
    - [1.1 基本Petri网 / Basic Petri Net](#11-基本petri网--basic-petri-net)
    - [1.2 前集和后集 / Pre-set and Post-set](#12-前集和后集--pre-set-and-post-set)

---

## 1. Petri网的定义 / Petri Net Definition

### 1.1 基本Petri网 / Basic Petri Net

**定义 1.1** (基本Petri网 / Basic Petri Net)

一个**Petri网**是一个五元组：
$$N = (P, T, F, W, M_0)$$

其中：

- $P = \{p_1, p_2, \ldots, p_m\}$ 是**库所集**（Place Set），表示系统状态
- $T = \{t_1, t_2, \ldots, t_n\}$ 是**变迁集**（Transition Set），表示系统事件或动作
- $F \subseteq (P \times T) \cup (T \times P)$ 是**流关系**（Flow Relation），表示库所和变迁之间的连接
- $W: F \to \mathbb{N}^+$ 是**权重函数**（Weight Function），表示边的权重（通常默认为1）
- $M_0: P \to \mathbb{N}$ 是**初始标识**（Initial Marking），表示系统的初始状态

**形式化约束**：

- $P \cap T = \emptyset$（库所和变迁不相交）
- $P \cup T \neq \emptyset$（至少有一个库所或变迁）
- $F \neq \emptyset$（至少有一条边）

### 1.2 前集和后集 / Pre-set and Post-set

**定义 1.2** (前集和后集 / Pre-set and Post-set)

对于Petri网 $N = (P, T, F, W, M_0)$：

- 对于变迁 $t \in T$，其**前集**（Pre-set）为：$\prescript{}{}{t} = \{p \in P \mid (p, t) \in F\}$
- 对于变迁 $t \in T$，其**后集**（Post-set）为：$t^{\bullet} = \{p \in P \mid (t, p) \in F\}$
- 对于库所 $p \in P$，其**前集**为：$\prescript{}{}{p} = \{t \in T \mid (t, p) \in F\}$
- 对于库所 $p \in P$，其**后集**为：$p^{\bullet} = \{t \in T \mid (p, t) \in F\}$

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**质量等级**: ⭐⭐⭐⭐⭐ 五星级
