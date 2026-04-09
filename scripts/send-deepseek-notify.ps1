# Check for pending DeepSeek notifications and send via WeCom

$notifyFile = "C:\Users\shenz\.openclaw\workspace\memory\deepseek-notify-pending.txt"
$stateFile = "C:\Users\shenz\.openclaw\workspace\memory\deepseek-monitor-state.json"

if (Test-Path $notifyFile) {
    Write-Host "Pending notification found!"
    
    try {
        $notifyData = Get-Content $notifyFile -Raw | ConvertFrom-Json
        
        if ($notifyData.type -eq "alert") {
            Write-Host "Sending alert notification..."
            Write-Host "Message: $($notifyData.message)"
            
            # Output the message for OpenClaw to process
            Write-Host "NOTIFY_WECOM:$($notifyData.message)"
            
            # Mark as notified
            if (Test-Path $stateFile) {
                $state = Get-Content $stateFile -Raw | ConvertFrom-Json
                $state.notified = $true
                $state.notifiedAt = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
                ($state | ConvertTo-Json) | Out-File -FilePath $stateFile -Encoding utf8
            }
        }
    }
    catch {
        Write-Host "Error processing notification: $($_.Exception.Message)"
    }
}
else {
    Write-Host "No pending notifications"
}
