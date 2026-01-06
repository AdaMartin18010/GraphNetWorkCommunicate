# 脚本说明 / Scripts README

## 📋 脚本列表

### 0. check-doc-links.ps1

**用途**: 校验 Markdown 文档内的本地链接健康度（目标文件是否存在、锚点是否可定位）。

**使用方法**:

```powershell
# 校验 docs/01-图论基础（文件链接 + 文件内锚点）
powershell -ExecutionPolicy Bypass -File scripts/check-doc-links.ps1 -Root "docs/01-图论基础" -StrictAnchors
```

**说明**:

- 默认会检查 `(.md)` 与 `(.md#anchor)` 链接是否有效
- `-StrictAnchors` 额外校验文档内 `(#anchor)` 形式的锚点

### 1. mark-pending-files.ps1

**用途**: 为所有待完善文件添加标记

**使用方法**:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/mark-pending-files.ps1
```

**功能**:

- 查找所有 `*-深度改进版-2025.md` 文件
- 检查是否已有标记
- 为未标记的文件添加待完善标记

**标记内容**:

- 状态说明
- 待补充内容清单

### 2. mark-pending-files.sh

**用途**: Linux/Mac环境下的批量标记脚本

**使用方法**:

```bash
bash scripts/mark-pending-files.sh
```

## ⚠️ 注意事项

1. **备份**: 执行脚本前建议先备份文件
2. **测试**: 可以先在单个文件上测试
3. **权限**: PowerShell脚本可能需要设置执行策略

## 📚 相关文档

- [待完善文件标记说明](../待完善文件标记说明-2025.md)
- [待完善文件清单](../待完善文件清单-2025.md)
