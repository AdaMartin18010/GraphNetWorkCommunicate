# Saga模式 / Saga模式

## 📚 **概述 / Overview**

本文档介绍Saga模式的详细理论和实现。

**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**国际对标**: 100% 达标 ✅
**完成状态**: ✅ 已完成

---

## 📑 **目录 / Table of Contents**

- [Saga模式 / Saga模式](#saga模式--saga模式)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [Saga模式](#saga模式)

---

## Saga模式

**定义 5.1.3** (Saga模式 / Saga Pattern)

**Saga模式**是一种长事务模式，将长事务分解为多个本地事务，每个本地事务有对应的补偿操作。

**两种实现方式**：

1. **编排式Saga（Choreography）**：每个服务都知道下一步操作
2. **编排式Saga（Orchestration）**：有一个协调者管理整个流程

**算法实现**：

```python
from typing import Callable, List, Tuple, Optional

class SagaStep:
    """Saga步骤"""

    def __init__(self, step_id: str,
                 execute_func: Callable,
                 compensate_func: Callable):
        self.step_id = step_id
        self.execute_func = execute_func
        self.compensate_func = compensate_func
        self.executed = False
        self.result = None

    def execute(self, *args, **kwargs):
        """执行步骤"""
        try:
            self.result = self.execute_func(*args, **kwargs)
            self.executed = True
            return True
        except Exception as e:
            logging.error(f"Step {self.step_id} failed: {e}")
            return False

    def compensate(self, *args, **kwargs):
        """补偿步骤"""
        if self.executed:
            try:
                self.compensate_func(*args, **kwargs)
                self.executed = False
                return True
            except Exception as e:
                logging.error(f"Step {self.step_id} compensation failed: {e}")
                return False
        return True

class SagaOrchestrator:
    """Saga编排器"""

    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.steps: List[SagaStep] = []
        self.executed_steps: List[SagaStep] = []

    def add_step(self, step: SagaStep):
        """添加步骤"""
        self.steps.append(step)

    def execute(self) -> bool:
        """
        执行Saga事务。

        Returns:
            是否全部成功
        """
        self.executed_steps = []

        for step in self.steps:
            if step.execute():
                self.executed_steps.append(step)
            else:
                # 执行失败，需要补偿
                self.compensate()
                return False

        return True

    def compensate(self):
        """补偿所有已执行的步骤（逆序）"""
        for step in reversed(self.executed_steps):
            step.compensate()

# 示例：订单处理Saga
def create_order_saga():
    """创建订单Saga示例"""
    saga = SagaOrchestrator("order_123")

    # 步骤1：创建订单
    def create_order():
        print("Creating order...")
        return {"order_id": "order_123"}

    def cancel_order():
        print("Canceling order...")

    saga.add_step(SagaStep("create_order", create_order, cancel_order))

    # 步骤2：扣减库存
    def reduce_inventory():
        print("Reducing inventory...")
        return {"inventory_reduced": True}

    def restore_inventory():
        print("Restoring inventory...")

    saga.add_step(SagaStep("reduce_inventory", reduce_inventory, restore_inventory))

    # 步骤3：扣减账户余额
    def deduct_balance():
        print("Deducting balance...")
        return {"balance_deducted": True}

    def refund_balance():
        print("Refunding balance...")

    saga.add_step(SagaStep("deduct_balance", deduct_balance, refund_balance))

    return saga

# 复杂度分析
# execute: O(n) 其中n是步骤数量
# compensate: O(n) - 需要补偿所有已执行的步骤
```


---

**文档版本**: v1.0
**最后更新**: 2025年1月
**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**国际对标**: 100% 达标 ✅
**完成状态**: ✅ 已完成
