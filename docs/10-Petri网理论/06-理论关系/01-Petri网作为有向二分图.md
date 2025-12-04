# Petri网作为有向二分图 / Petri Nets as Directed Bipartite Graphs

## 📚 **概述 / Overview**

本文档描述Petri网与图论的关系，特别是Petri网作为有向二分图的形式化定义和理论基础。Petri网的底层结构本质上是一个有向二分图，这使得我们可以利用图论的理论和方法来分析Petri网。

---

## 🔧 **核心内容 / Core Content**

- Petri网的有向二分图结构
- 形式化定义和证明
- 图论视角下的Petri网
- 二分图性质的应用

---

## 📐 **形式化定义 / Formal Definition**

### 定理 5.1 (Petri网是有向二分图)

Petri网 $N = (P, T, F, W, M_0)$ 的底层结构是一个**有向二分图** $G = (V, E)$，其中：

- $V = P \cup T$（顶点集 = 库所集 ∪ 变迁集）
- $E = F$（边集 = 流关系）
- 二分性：$P \cap T = \emptyset$，且所有边都连接 $P$ 和 $T$ 之间的顶点

### 证明

根据Petri网的定义：

- $P \cap T = \emptyset$（库所和变迁不相交）
- $F \subseteq (P \times T) \cup (T \times P)$（流关系只连接库所和变迁）

因此，$G$ 是有向二分图，其中两个顶点集是 $P$ 和 $T$。$\square$

---

## 🔗 **相关链接 / Related Links**

- [Petri网理论主目录](../../README.md)
- [理论关系目录](../README.md)
- [图论基础模块](../../../01-图论基础/)
- [特殊图性质](02-特殊图性质.md)

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**状态**: ✅ **已完成**
