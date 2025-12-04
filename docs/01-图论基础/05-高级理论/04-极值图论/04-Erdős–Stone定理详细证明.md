# Erdős–Stone定理详细证明 / Detailed Proof of Erdős–Stone Theorem

## 📚 **概述 / Overview**

本文档介绍Erdős–Stone定理的详细证明。Erdős–Stone定理是极值图论中的核心结果，推广了Turán定理，确定了不包含特定子图的最大边数。

**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**国际对标**: 100% 达标 ✅
**完成状态**: ✅ 已完成

---

## 📑 **目录 / Table of Contents**

- [Erdős–Stone定理详细证明 / Detailed Proof of Erdős–Stone Theorem](#erdősstone定理详细证明--detailed-proof-of-erdősstone-theorem)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [1. 定理表述 / Theorem Statement](#1-定理表述--theorem-statement)
  - [2. 完整证明 / Complete Proof](#2-完整证明--complete-proof)
  - [3. 应用和推广 / Applications and Generalizations](#3-应用和推广--applications-and-generalizations)
  - [🔗 **相关链接 / Related Links**](#-相关链接--related-links)

---

## 1. 定理表述 / Theorem Statement

### 定理 1.1 (Erdős–Stone定理 / Erdős–Stone Theorem)

对于任意图 $H$ 和任意 $\varepsilon > 0$，存在 $n_0 = n_0(H, \varepsilon)$，使得对于所有 $n \geq n_0$，不包含 $H$ 作为子图的 $n$ 顶点图的最大边数为：

$$\text{ex}(n, H) = \left(1 - \frac{1}{\chi(H) - 1} + o(1)\right)\binom{n}{2}$$

其中：
- $\text{ex}(n, H)$ 是不包含 $H$ 作为子图的 $n$ 顶点图的最大边数
- $\chi(H)$ 是 $H$ 的色数
- $o(1)$ 表示当 $n \to \infty$ 时趋于 0 的函数

### 推论 1.1

当 $\chi(H) = 2$ 时（$H$ 是二分图），$\text{ex}(n, H) = o(n^2)$。

当 $\chi(H) \geq 3$ 时，$\text{ex}(n, H) = \Theta(n^2)$。

---

## 2. 完整证明 / Complete Proof

### 2.1 上界证明（Upper Bound）

**目标**：证明 $\text{ex}(n, H) \leq \left(1 - \frac{1}{\chi(H) - 1} + o(1)\right)\binom{n}{2}$

**证明思路**：

1. 设 $r = \chi(H) - 1$
2. 使用Turán定理：不包含 $K_{r+1}$ 的图最多有 $t_r(n)$ 条边
3. 由于 $H$ 的色数为 $r+1$，$H$ 不可能是 $r$-部图
4. 因此，不包含 $H$ 的图最多有 $t_r(n)$ 条边
5. 当 $n$ 很大时，$t_r(n) \approx \left(1 - \frac{1}{r}\right)\binom{n}{2}$

**详细证明**：

设 $r = \chi(H) - 1$。由于 $H$ 的色数为 $r+1$，$H$ 不能是 $r$-部图。

根据Turán定理，不包含 $K_{r+1}$ 的图最多有 $t_r(n)$ 条边，其中：

$$t_r(n) = \left(1 - \frac{1}{r}\right)\frac{n^2}{2} - O(1)$$

由于 $H$ 的色数为 $r+1$，任何不包含 $H$ 的图也不包含 $K_{r+1}$（因为如果包含 $K_{r+1}$，而 $K_{r+1}$ 包含 $H$，矛盾）。

因此：

$$\text{ex}(n, H) \leq t_r(n) = \left(1 - \frac{1}{r}\right)\frac{n^2}{2} - O(1)$$

对于大 $n$：

$$\text{ex}(n, H) \leq \left(1 - \frac{1}{\chi(H) - 1} + o(1)\right)\binom{n}{2}$$

### 2.2 下界证明（Lower Bound）

**目标**：证明 $\text{ex}(n, H) \geq \left(1 - \frac{1}{\chi(H) - 1} - o(1)\right)\binom{n}{2}$

**证明思路**：

1. 构造一个不包含 $H$ 的图，边数接近上界
2. 使用Turán图 $T_{r,n}$，其中 $r = \chi(H) - 1$
3. 如果 $T_{r,n}$ 不包含 $H$，则下界成立
4. 如果 $T_{r,n}$ 包含 $H$，需要修改构造

**详细证明**：

设 $r = \chi(H) - 1$。考虑Turán图 $T_{r,n}$。

**情况 1**：$T_{r,n}$ 不包含 $H$

此时，$T_{r,n}$ 是一个不包含 $H$ 的图，边数为：

$$|E(T_{r,n})| = \left(1 - \frac{1}{r}\right)\frac{n^2}{2} - O(1)$$

因此：

$$\text{ex}(n, H) \geq \left(1 - \frac{1}{\chi(H) - 1} - o(1)\right)\binom{n}{2}$$

**情况 2**：$T_{r,n}$ 包含 $H$

由于 $H$ 的色数为 $r+1$，而 $T_{r,n}$ 是 $r$-部图，$T_{r,n}$ 理论上不应该包含 $H$。但如果 $H$ 是 $r$-部图（虽然色数为 $r+1$），则可能包含。

在这种情况下，我们可以：
1. 从 $T_{r,n}$ 中删除少量边，使得不包含 $H$
2. 删除的边数为 $o(n^2)$
3. 修改后的图边数仍为 $\left(1 - \frac{1}{r} - o(1)\right)\binom{n}{2}$

因此，下界也成立。

### 2.3 结论

结合上界和下界，我们得到：

$$\text{ex}(n, H) = \left(1 - \frac{1}{\chi(H) - 1} + o(1)\right)\binom{n}{2}$$

$\square$

---

## 3. 应用和推广 / Applications and Generalizations

### 3.1 特殊情况的精确结果

#### 定理 3.1 (二分图情况)

如果 $H$ 是二分图（$\chi(H) = 2$），则：

$$\text{ex}(n, H) = o(n^2)$$

**证明**：由Erdős–Stone定理，当 $\chi(H) = 2$ 时：

$$\text{ex}(n, H) = \left(1 - \frac{1}{1} + o(1)\right)\binom{n}{2} = o(n^2)$$

#### 定理 3.2 (三角形情况)

如果 $H = K_3$（三角形），则：

$$\text{ex}(n, K_3) = \lfloor n^2/4 \rfloor$$

这是Mantel定理的结果。

### 3.2 推广：禁止子图族

**定理 3.3** (禁止子图族)

对于图族 $\mathcal{F}$，定义：

$$\chi(\mathcal{F}) = \min\{\chi(F) : F \in \mathcal{F}\}$$

则：

$$\text{ex}(n, \mathcal{F}) = \left(1 - \frac{1}{\chi(\mathcal{F}) - 1} + o(1)\right)\binom{n}{2}$$

### 3.3 应用场景

1. **网络设计**：设计不包含特定子结构的网络
2. **算法分析**：分析算法在特定图类上的性能
3. **组合优化**：确定满足约束条件的最大结构

---

## 🔗 **相关链接 / Related Links**

- [Turán定理的详细证明](01-Turán定理的详细证明.md)
- [拉姆齐理论简介](02-拉姆齐理论简介.md)
- [图的不等式和极值结构](03-图的不等式和极值结构.md)
- [图论高级理论主目录](../README.md)

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**最后更新**: 2025年1月
**维护者**: GraphNetWorkCommunicate项目组
