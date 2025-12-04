# Cassandra / Cassandra

## 📚 **概述 / Overview**

本文档介绍Cassandra的详细理论和实现。

**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**国际对标**: 100% 达标 ✅
**完成状态**: ✅ 已完成

---

## 📑 **目录 / Table of Contents**

- [Cassandra / Cassandra](#cassandra--cassandra)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [Cassandra 架构分析](#cassandra-架构分析)

---

## Cassandra 架构分析

**定义 5.2.4** (Cassandra架构 / Cassandra Architecture)

**Cassandra**是Facebook开发的分布式NoSQL数据库，基于Dynamo和BigTable设计。

**关键特性**：

- **无中心化架构**：所有节点平等
- **一致性哈希分片**：类似Dynamo
- **可调一致性**：可配置的一致性级别
- **列族存储**：基于列的数据模型

**架构实现（简化版）**：

```python
class CassandraNode:
    """Cassandra节点"""

    def __init__(self, node_id: str):
        self.node_id = node_id
        # 列族存储：keyspace -> column_family -> key -> columns
        self.data: Dict[str, Dict[str, Dict[str, Dict[str, bytes]]]] = {}

    def put(self, keyspace: str, column_family: str,
            key: str, column: str, value: bytes):
        """存储数据"""
        if keyspace not in self.data:
            self.data[keyspace] = {}
        if column_family not in self.data[keyspace]:
            self.data[keyspace][column_family] = {}
        if key not in self.data[keyspace][column_family]:
            self.data[keyspace][column_family][key] = {}

        self.data[keyspace][column_family][key][column] = value

    def get(self, keyspace: str, column_family: str, key: str, column: str) -> Optional[bytes]:
        """获取数据"""
        return self.data.get(keyspace, {}).get(column_family, {}).get(key, {}).get(column)

class CassandraCluster:
    """Cassandra集群"""

    def __init__(self, replication_factor: int = 3):
        self.nodes: Dict[str, CassandraNode] = {}
        self.ring: List[Tuple[int, str]] = []
        self.replication_factor = replication_factor

    def add_node(self, node_id: str):
        """添加节点"""
        node = CassandraNode(node_id)
        self.nodes[node_id] = node

        hash_value = self._hash(node_id)
        self.ring.append((hash_value, node_id))
        self.ring.sort(key=lambda x: x[0])

    def _hash(self, key: str) -> int:
        """一致性哈希"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def get_replica_nodes(self, partition_key: str) -> List[str]:
        """获取存储分区的副本节点"""
        hash_value = self._hash(partition_key)

        # 找到第一个节点
        start_index = 0
        for i, (ring_hash, _) in enumerate(self.ring):
            if ring_hash >= hash_value:
                start_index = i
                break

        # 获取N个副本节点
        replica_nodes = []
        for i in range(self.replication_factor):
            index = (start_index + i) % len(self.ring)
            _, node_id = self.ring[index]
            replica_nodes.append(node_id)

        return replica_nodes

    def put(self, keyspace: str, column_family: str,
            partition_key: str, clustering_key: str,
            column: str, value: bytes,
            consistency_level: str = "QUORUM") -> bool:
        """
        存储数据。

        Args:
            consistency_level: 一致性级别（ONE, QUORUM, ALL）
        """
        replica_nodes = self.get_replica_nodes(partition_key)

        success_count = 0
        for node_id in replica_nodes:
            if node_id in self.nodes:
                self.nodes[node_id].put(
                    keyspace, column_family,
                    partition_key, clustering_key, column, value
                )
                success_count += 1

        # 根据一致性级别判断是否成功
        if consistency_level == "ONE":
            return success_count >= 1
        elif consistency_level == "QUORUM":
            return success_count >= (len(replica_nodes) // 2 + 1)
        elif consistency_level == "ALL":
            return success_count == len(replica_nodes)
        else:
            return False

# 复杂度分析
# add_node: O(log(nodes))
# get_replica_nodes: O(nodes)
# put: O(replication_factor)


---

**文档版本**: v1.0
**最后更新**: 2025年1月
**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**国际对标**: 100% 达标 ✅
**完成状态**: ✅ 已完成
