# PowerShell脚本：为所有待完善文件添加标记
# 使用方法: powershell -ExecutionPolicy Bypass -File scripts/mark-pending-files.ps1

$marker = @'
⚠️ **状态**: 待完善
📝 **说明**: 本文档为深度改进版模板，内容不完整，需要根据项目定位补充完整的理论梳理内容。

**待补充内容**:
- [ ] 完整的理论定义
- [ ] 性质与定理
- [ ] 形式化证明
- [ ] 应用案例
- [ ] 与其他理论的关系

---
'@

Write-Host "开始为待完善文件添加标记..." -ForegroundColor Green

$count = 0
$files = Get-ChildItem -Path "docs" -Recurse -Filter "*-深度改进版-2025.md" -File

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    
    # 检查是否已有标记
    if ($content -notmatch "⚠️ \*\*状态\*\*: 待完善") {
        # 获取第一行（标题）
        $lines = Get-Content -Path $file.FullName -Encoding UTF8
        $firstLine = $lines[0]
        
        # 构建新内容
        $newContent = $firstLine + "`r`n`r`n" + $marker + "`r`n`r`n"
        
        # 添加剩余内容（跳过第一行）
        for ($i = 1; $i -lt $lines.Count; $i++) {
            $newContent += $lines[$i] + "`r`n"
        }
        
        # 写入文件
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
        
        $count++
        Write-Host "已标记: $($file.FullName)" -ForegroundColor Yellow
    }
}

Write-Host "`n完成！共标记 $count 个文件。" -ForegroundColor Green
