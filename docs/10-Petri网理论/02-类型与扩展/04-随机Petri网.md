# 随机Petri网（Stochastic Petri Net） / Stochastic Petri Net

## 📚 **概述 / Overview**

随机Petri网（Stochastic Petri Net，SPN）为每个变迁分配随机触发时间，用于性能分析和可靠性评估。

---

## 1. 随机Petri网定义 / Stochastic Petri Net Definition

**定义 2.3** (随机Petri网 / Stochastic Petri Net)

**随机Petri网**是一个扩展的Petri网：
$$SPN = (P, T, F, W, M_0, \Lambda)$$

其中：

- $P, T, F, W, M_0$ 同基本Petri网
- $\Lambda: T \to \mathbb{R}^+$ 是**触发率函数**（Firing Rate Function）

每个变迁 $t$ 的触发时间服从指数分布，参数为 $\Lambda(t)$。

---

**相关链接**：

- [基本Petri网](01-基本Petri网.md)
- [时间Petri网](03-时间Petri网.md)

---

**文档版本**: v1.0
**创建时间**: 2025年1月
**质量等级**: ⭐⭐⭐⭐⭐ 五星级
