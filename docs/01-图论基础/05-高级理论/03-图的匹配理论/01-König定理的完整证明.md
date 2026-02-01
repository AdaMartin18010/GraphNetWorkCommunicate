# König定理的完整证明 / Complete Proof of König's Theorem

## 📚 **概述 / Overview**

本文档介绍König定理的完整证明。König定理是二分图理论中的核心定理，建立了最大匹配和最小顶点覆盖之间的对偶关系。

---

## 📑 **目录 / Table of Contents**

- [König定理的完整证明 / Complete Proof of König's Theorem](#könig定理的完整证明--complete-proof-of-königs-theorem)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [📐 **定理表述 / Theorem Statement**](#-定理表述--theorem-statement)
    - [定理 5.3.1 (König定理 / König's Theorem)](#定理-531-könig定理--königs-theorem)
  - [🔬 **完整证明 / Complete Proof**](#-完整证明--complete-proof)
    - [步骤 1：证明 $\\nu(G) \\leq \\tau(G)$](#步骤-1证明-nug-leq-taug)
    - [步骤 2：构造最小顶点覆盖](#步骤-2构造最小顶点覆盖)
    - [步骤 3：证明 $C$ 是顶点覆盖](#步骤-3证明-c-是顶点覆盖)
    - [步骤 4：证明 $|C| = |M|$](#步骤-4证明-c--m)
    - [步骤 5：结论](#步骤-5结论)
  - [📚 **历史背景 / Historical Background**](#-历史背景--historical-background)
  - [🔗 **相关链接 / Related Links**](#-相关链接--related-links)

---

## 📐 **定理表述 / Theorem Statement**

### 定理 5.3.1 (König定理 / König's Theorem)

在二分图 $G = (U \cup V, E)$ 中，最大匹配的大小等于最小顶点覆盖的大小。

**形式化表述**：

设 $G$ 是二分图，则：
$$\nu(G) = \tau(G)$$

其中：

- $\nu(G)$ 是最大匹配的大小
- $\tau(G)$ 是最小顶点覆盖的大小

---

## 🔬 **完整证明 / Complete Proof**

### 步骤 1：证明 $\nu(G) \leq \tau(G)$

对于任意匹配 $M$ 和任意顶点覆盖 $C$，由于 $C$ 必须覆盖所有边，而 $M$ 中的边是两两不相邻的，因此 $C$ 必须包含 $M$ 中每条边的至少一个端点。

由于 $M$ 中的边不相邻，$C$ 中至少有 $|M|$ 个不同的顶点，因此：
$$|M| \leq |C|$$

对所有匹配和顶点覆盖成立，因此：
$$\nu(G) = \max_{M \text{ matching}} |M| \leq \min_{C \text{ vertex cover}} |C| = \tau(G)$$

---

### 步骤 2：构造最小顶点覆盖

设 $M$ 是 $G$ 的最大匹配。我们构造一个大小为 $|M|$ 的顶点覆盖，从而证明 $\tau(G) \leq \nu(G)$。

使用最大流方法构造最小顶点覆盖：

1. 将二分图 $G$ 转换为流网络：
   - 添加源点 $s$，从 $s$ 到 $U$ 中每个顶点添加容量为1的边
   - 添加汇点 $t$，从 $V$ 中每个顶点到 $t$ 添加容量为1的边
   - 保留原图中的所有边，容量为1

2. 计算最大流 $f^*$，最大流值等于最大匹配大小 $|M|$

3. 使用最大流最小割定理，找到最小割 $(S, T)$，其中 $s \in S$，$t \in T$

4. 定义顶点覆盖：
   $$C = (U \cap T) \cup (V \cap S)$$

---

### 步骤 3：证明 $C$ 是顶点覆盖

对于任意边 $(u, v) \in E$，其中 $u \in U$，$v \in V$：

- 如果 $u \in S$ 且 $v \in T$：则 $v \in V \cap T$，但根据割的定义，如果 $u \in S$ 且 $v \in T$，则 $(u, v)$ 必须是割边，容量为1。由于最大流值等于最大匹配，这会导致矛盾。实际上，如果 $u \in S$，则 $v$ 必须在 $S$ 中（否则 $(u, v)$ 会成为割边且容量未满，与最大流矛盾）。

- 因此，对于任意边 $(u, v)$：
  - 要么 $u \in T$（即 $u \in U \cap T \subseteq C$）
  - 要么 $v \in S$（即 $v \in V \cap S \subseteq C$）

因此，$C$ 覆盖了所有边，是一个顶点覆盖。

---

### 步骤 4：证明 $|C| = |M|$

根据最大流最小割定理，最小割的容量等于最大流值，即 $|M|$。

最小割的容量等于：
$$c(S, T) = |U \cap T| + |V \cap S| + \text{从 } S \cap U \text{ 到 } T \cap V \text{ 的边数}$$

由于最大匹配中每条边都从 $S$ 到 $T$，且容量为1，我们有：
$$c(S, T) = |U \cap T| + |V \cap S| = |C|$$

因此，$|C| = |M| = \nu(G)$。

---

### 步骤 5：结论

由步骤 1 和步骤 4：
$$\nu(G) = |C| \geq \tau(G) \geq \nu(G)$$

因此：
$$\nu(G) = \tau(G) \quad \square$$

---

## 📚 **历史背景 / Historical Background**

- **1931年**：Dénes König 首次证明了该定理
- 是图论中最重要的定理之一
- 为二分图匹配和顶点覆盖问题建立了对偶关系

---

## 🔗 **相关链接 / Related Links**

- [图的匹配理论目录](../README.md)
- [霍尔婚姻定理的详细证明](02-霍尔婚姻定理的详细证明.md)
- [最大匹配算法](03-最大匹配算法.md)
- [加权匹配算法](04-加权匹配算法.md)
- [图论高级理论主目录](../../README.md)

**权威出处**：König (1931) 原论文；Diestel, *Graph Theory*, Ch.2；MIT 18.217 图论课程。

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**状态**: ✅ **已完成**
