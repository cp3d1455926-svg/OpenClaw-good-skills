# 创建天猫精灵监听器任务计划
$taskName = "AliGenie-Listener"
$scriptPath = "C:\Users\shenz\.openclaw\workspace\scripts\process-aligenie-input.ps1"
$logPath = "C:\Users\shenz\.openclaw\workspace\memory\aligenie-listener.log"

# 先删除旧任务（如果存在）
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# 创建动作
$action = New-ScheduledTaskAction -Execute "powershell" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""

# 创建触发器 - 立即开始，每分钟重复
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 1) -RepetitionDuration ([TimeSpan]::MaxValue)

# 创建主体
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Highest

# 注册任务
try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Force
    Write-Host "✅ 任务计划创建成功：$taskName"
    Write-Host "   脚本路径：$scriptPath"
    Write-Host "   执行频率：每分钟一次"
    Write-Host "   日志文件：$logPath"
} catch {
    Write-Host "❌ 创建失败：$($_.Exception.Message)"
    
    # 备用方案：使用 schtasks 命令
    Write-Host "尝试使用 schtasks 命令..."
    $schCmd = "schtasks /Create /TN `"$taskName`" /TR `"powershell -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `'$scriptPath`'`" /SC MINUTE /MO 1 /RU `"$env:USERNAME`""
    Invoke-Expression $schCmd
    Write-Host "✅ 已使用 schtasks 创建：$taskName"
}

Write-Host ""
Write-Host "📋 管理命令："
Write-Host "   查看状态：schtasks /Query /TN `"$taskName`""
Write-Host "   手动运行：schtasks /Run /TN `"$taskName`""
Write-Host "   查看日志：Get-Content $logPath -Tail 20"
Write-Host "   删除任务：schtasks /Delete /TN `"$taskName`" /F"
