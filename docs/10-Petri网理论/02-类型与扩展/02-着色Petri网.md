# 着色Petri网（Colored Petri Net） / Colored Petri Net

## 📚 **概述 / Overview**

着色Petri网（Colored Petri Net，CPN）允许库所中的令牌携带数据值（颜色），从而更简洁地表示复杂系统。

---

## 📑 **目录 / Table of Contents**

- [着色Petri网（Colored Petri Net） / Colored Petri Net](#着色petri网colored-petri-net--colored-petri-net)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [1. 着色Petri网定义 / Colored Petri Net Definition](#1-着色petri网定义--colored-petri-net-definition)

---

## 1. 着色Petri网定义 / Colored Petri Net Definition

**定义 2.1** (着色Petri网 / Colored Petri Net)

**着色Petri网**是一个扩展的Petri网：
$$CPN = (P, T, F, \Sigma, C, W, M_0)$$

其中：

- $P, T, F$ 同基本Petri网
- $\Sigma$ 是**颜色集**（Color Set）
- $C: P \cup T \to \Sigma$ 是**颜色函数**（Color Function）
- $W: F \to \text{Expr}$ 是**表达式函数**（Expression Function），返回多集表达式
- $M_0: P \to \text{MS}(\Sigma)$ 是**初始标识**，返回多集

着色Petri网允许库所中的令牌携带数据值（颜色），从而更简洁地表示复杂系统。

---

**相关链接**：

- [基本Petri网](01-基本Petri网.md)
- [Petri网定义](../01-基础理论/01-Petri网定义.md)

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**质量等级**: ⭐⭐⭐⭐⭐ 五星级
