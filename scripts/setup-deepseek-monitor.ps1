# Create Windows Task Scheduler to monitor DeepSeek GitHub

$taskName = "DeepSeekMonitor"
$scriptPath = "C:\Users\shenz\.openclaw\workspace\scripts\check-deepseek.ps1"

# Create action
$action = New-ScheduledTaskAction -Execute "powershell" -Argument "-NoProfile -WindowStyle Hidden -File `"$scriptPath`""

# Create trigger - start now, repeat every hour (for 365 days)
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 365)

# Create principal
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Highest

# Register task
try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Force
    Write-Host "SUCCESS: Task created: $taskName"
    Write-Host "Script: $scriptPath"
    Write-Host "Frequency: Every hour"
}
catch {
    Write-Host "ERROR: $($_.Exception.Message)"
    Write-Host "Trying alternative method..."
    
    # Alternative: use schtasks command
    $schCmd = "schtasks /Create /TN `"$taskName`" /TR `"powershell -NoProfile -WindowStyle Hidden -File `'$scriptPath`'`" /SC HOURLY /MO 1 /RU `"$env:USERNAME`""
    Invoke-Expression $schCmd
    Write-Host "Created via schtasks: $taskName"
}
