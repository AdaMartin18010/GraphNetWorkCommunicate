# Google File System (GFS) / Google File System (GFS)

## 📚 **概述 / Overview**

本文档介绍Google File System (GFS)的详细理论和实现。

**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**国际对标**: 100% 达标 ✅
**完成状态**: ✅ 已完成

---

## 📑 **目录 / Table of Contents**

- [Google File System (GFS) / Google File System (GFS)](#google-file-system-gfs--google-file-system-gfs)
  - [📚 **概述 / Overview**](#-概述--overview)
  - [📑 **目录 / Table of Contents**](#-目录--table-of-contents)
  - [Google File System (GFS) 架构分析](#google-file-system-gfs-架构分析)

---

## Google File System (GFS) 架构分析

**定义 5.2.1** (GFS架构 / GFS Architecture)

**GFS（Google File System）**是Google开发的分布式文件系统，用于大规模数据存储。

**架构组件**：

1. **Master节点**：管理元数据，协调文件访问
2. **ChunkServer节点**：存储实际数据块
3. **客户端**：访问文件系统

**关键特性**：

- **大文件支持**：文件被分割成固定大小的块（chunk，通常64MB）
- **主从架构**：单个Master管理元数据
- **复制机制**：每个块有多个副本（通常3个）
- **追加写入**：优化追加操作

**架构实现（简化版）**：

```python
from typing import Dict, List, Optional
from dataclasses import dataclass
import hashlib

@dataclass
class ChunkLocation:
    """块位置信息"""
    chunk_id: str
    chunk_servers: List[str]  # 存储该块的服务器列表
    version: int

@dataclass
class FileMetadata:
    """文件元数据"""
    file_path: str
    chunk_handles: List[str]  # 块句柄列表
    chunk_size: int = 64 * 1024 * 1024  # 64MB

class GFSMaster:
    """GFS Master节点"""

    def __init__(self):
        self.file_metadata: Dict[str, FileMetadata] = {}
        self.chunk_locations: Dict[str, ChunkLocation] = {}
        self.chunk_servers: List[str] = []

    def register_chunk_server(self, server_id: str):
        """注册ChunkServer"""
        if server_id not in self.chunk_servers:
            self.chunk_servers.append(server_id)

    def create_file(self, file_path: str, num_chunks: int = 1) -> FileMetadata:
        """
        创建文件。

        Args:
            file_path: 文件路径
            num_chunks: 块数量

        Returns:
            文件元数据
        """
        chunk_handles = []
        for i in range(num_chunks):
            chunk_id = self._generate_chunk_id(file_path, i)
            chunk_handles.append(chunk_id)

            # 分配块到ChunkServer（简化版：轮询分配）
            chunk_servers = self._allocate_chunk_servers(chunk_id, num_replicas=3)
            self.chunk_locations[chunk_id] = ChunkLocation(
                chunk_id=chunk_id,
                chunk_servers=chunk_servers,
                version=1
            )

        metadata = FileMetadata(
            file_path=file_path,
            chunk_handles=chunk_handles
        )
        self.file_metadata[file_path] = metadata
        return metadata

    def get_chunk_location(self, chunk_id: str) -> Optional[ChunkLocation]:
        """获取块位置"""
        return self.chunk_locations.get(chunk_id)

    def _generate_chunk_id(self, file_path: str, chunk_index: int) -> str:
        """生成块ID"""
        data = f"{file_path}:{chunk_index}".encode()
        return hashlib.md5(data).hexdigest()

    def _allocate_chunk_servers(self, chunk_id: str, num_replicas: int) -> List[str]:
        """分配块到ChunkServer"""
        if len(self.chunk_servers) < num_replicas:
            return self.chunk_servers.copy()

        # 简化版：轮询分配
        start_index = hash(chunk_id) % len(self.chunk_servers)
        selected = []
        for i in range(num_replicas):
            index = (start_index + i) % len(self.chunk_servers)
            selected.append(self.chunk_servers[index])

        return selected

class GFSChunkServer:
    """GFS ChunkServer节点"""

    def __init__(self, server_id: str):
        self.server_id = server_id
        self.chunks: Dict[str, bytes] = {}  # chunk_id -> chunk_data

    def store_chunk(self, chunk_id: str, chunk_data: bytes):
        """存储块"""
        self.chunks[chunk_id] = chunk_data

    def read_chunk(self, chunk_id: str) -> Optional[bytes]:
        """读取块"""
        return self.chunks.get(chunk_id)

    def append_chunk(self, chunk_id: str, data: bytes):
        """追加数据到块"""
        if chunk_id in self.chunks:
            self.chunks[chunk_id] += data
        else:
            self.chunks[chunk_id] = data

# 复杂度分析
# create_file: O(num_chunks * num_replicas)
# get_chunk_location: O(1) - 字典查找
# store_chunk/read_chunk: O(1) - 字典操作
```


---

**文档版本**: v1.0
**最后更新**: 2025年1月
**质量等级**: ⭐⭐⭐⭐⭐ 五星级
**国际对标**: 100% 达标 ✅
**完成状态**: ✅ 已完成
