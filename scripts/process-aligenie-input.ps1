# 天猫精灵输入处理脚本（优化版）
# 每分钟执行一次，处理输入文件并生成响应

$ErrorActionPreference = "Stop"
$logFile = "C:\Users\shenz\.openclaw\workspace\memory\aligenie-listener.log"
$inputFile = "C:\Users\shenz\.openclaw\workspace\memory\aligenie-input.txt"
$outputFile = "C:\Users\shenz\.openclaw\workspace\memory\aligenie-output.txt"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $Message"
    Add-Content -Path $logFile -Value $logEntry -Encoding UTF8
}

try {
    Write-Log "开始检查输入文件..."
    
    # 检查输入文件是否存在
    if (-not (Test-Path $inputFile)) {
        Write-Log "无新输入，跳过"
        exit 0
    }
    
    Write-Log "发现输入文件，读取内容..."
    
    # 读取并解析 JSON
    $inputData = Get-Content $inputFile -Raw -Encoding UTF8 | ConvertFrom-Json
    
    # 检查是否有 message 字段
    if (-not $inputData.message) {
        Write-Log "输入文件缺少 message 字段"
        Remove-Item $inputFile -Force
        exit 0
    }
    
    $message = $inputData.message
    Write-Log "处理指令：$message"
    
    # 创建输出文件（模拟 OpenClaw 响应）
    $response = @{
        status = "success"
        query = $message
        result = "你好！我是小鬼 (Little Ghost) 👻，你的 AI 助手！`n`n我已收到你的指令：`"$message`"`n`n天猫精灵桥接功能测试成功！✅"
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        source = "openclaw-optimized"
    } | ConvertTo-Json -Depth 5
    
    # 写入输出文件
    $response | Out-File $outputFile -Encoding UTF8
    Write-Log "响应已写入输出文件"
    
    # 删除输入文件
    Remove-Item $inputFile -Force
    Write-Log "输入文件已删除"
    
    Write-Log "处理完成！"
    
} catch {
    $errorMsg = "处理失败：$($_.Exception.Message)"
    Write-Log $errorMsg
    
    # 写入错误响应
    $errorResponse = @{
        status = "error"
        error = $_.Exception.Message
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    } | ConvertTo-Json
    
    $errorResponse | Out-File $outputFile -Encoding UTF8
    
    # 如果有输入文件，删除它
    if (Test-Path $inputFile) {
        Remove-Item $inputFile -Force
    }
}
