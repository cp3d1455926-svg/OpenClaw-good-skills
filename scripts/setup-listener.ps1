# 创建天猫精灵监听器任务计划
$taskName = "AliGenie-Listener"
$scriptPath = "C:\Users\shenz\.openclaw\workspace\scripts\process-aligenie-input.ps1"

# 删除旧任务
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# 使用 schtasks 命令创建
Write-Host "Creating scheduled task: $taskName"
schtasks /Create /TN "$taskName" /TR "powershell -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File '$scriptPath'" /SC MINUTE /MO 1 /RU SYSTEM

Write-Host "Done! Task created."
Write-Host ""
Write-Host "Commands:"
Write-Host "  Status: schtasks /Query /TN '$taskName'"
Write-Host "  Run: schtasks /Run /TN '$taskName'"
Write-Host "  Delete: schtasks /Delete /TN '$taskName' /F"
