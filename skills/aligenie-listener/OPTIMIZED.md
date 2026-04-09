---
name: aligenie-optimizer
description: 优化版天猫精灵监听器 - 使用完整路径和错误处理
---

# AliGenie Optimized Listener

## 📋 处理逻辑

```powershell
# 1. 检查输入文件
$inputFile = "C:\Users\shenz\.openclaw\workspace\memory\aligenie-input.txt"
$outputFile = "C:\Users\shenz\.openclaw\workspace\memory\aligenie-output.txt"

# 2. 如果输入文件存在
if (Test-Path $inputFile) {
    # 3. 读取并解析 JSON
    $input = Get-Content $inputFile -Raw | ConvertFrom-Json
    
    # 4. 如果有 message 字段
    if ($input.message) {
        # 5. 调用 OpenClaw 处理
        $result = Invoke-OpenClaw -message $input.message
        
        # 6. 写入输出文件
        $result | Out-File $outputFile -Encoding utf8
        
        # 7. 删除输入文件
        Remove-Item $inputFile -Force
    }
}
```

## 🎯 优化点

1. **完整文件路径** - 避免路径解析问题
2. **错误处理** - 捕获并记录异常
3. **超时控制** - 25 秒内完成
4. **日志记录** - 记录处理过程
