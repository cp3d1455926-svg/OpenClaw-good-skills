# DeepSeek GitHub Monitor Script
# Check for new models/projects and notify user via WeCom

$stateFile = "C:\Users\shenz\.openclaw\workspace\memory\deepseek-monitor-state.json"
$outputFile = "C:\Users\shenz\.openclaw\workspace\memory\deepseek-check-result.txt"
$notifyFile = "C:\Users\shenz\.openclaw\workspace\memory\deepseek-notify-pending.txt"

Write-Host "Checking DeepSeek GitHub..."

try {
    $response = Invoke-WebRequest -Uri "https://github.com/deepseek-ai" -UseBasicParsing -TimeoutSec 30
    $content = $response.Content
    
    # Get page hash
    $hash = Get-FileHash -InputStream ([System.IO.MemoryStream]::New([System.Text.Encoding]::UTF8.GetBytes($content))) -Algorithm MD5 | Select-Object -ExpandProperty Hash
    
    # Read last state
    $lastState = $null
    if (Test-Path $stateFile) {
        $lastState = Get-Content $stateFile -Raw | ConvertFrom-Json
        $lastHash = $lastState.pageHash
        
        if ($hash -ne $lastHash) {
            $checkTime = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
            $message = "🚨 DeepSeek GitHub 有更新！`n`n检查时间：$checkTime`n`n可能发布了新模型或新项目。`n`n立即查看：https://github.com/deepseek-ai`n`n页面哈希变化：$lastHash -> $hash"
            Write-Host "ALERT: Changes detected!"
            Write-Host $message
            
            # Write notification request
            $notifyData = @{
                type = "alert"
                message = $message
                timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
                url = "https://github.com/deepseek-ai"
            } | ConvertTo-Json -Depth 5
            $notifyData | Out-File -FilePath $notifyFile -Encoding utf8
            
            # Also write to result file
            $message | Out-File -FilePath $outputFile -Encoding utf8
        }
        else {
            $checkTime = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
            $message = "OK: No changes detected`nCheck time: $checkTime`nPage hash: $hash"
            Write-Host $message
            $message | Out-File -FilePath $outputFile -Encoding utf8
            
            # Remove pending notification if exists (user was already notified)
            if (Test-Path $notifyFile) {
                Remove-Item $notifyFile -Force
                Write-Host "Cleared pending notification"
            }
        }
    }
    else {
        $checkTime = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        $message = "INIT: DeepSeek monitor initialized`nCheck time: $checkTime`nPage hash: $hash`n`nBaseline saved. Next check will compare changes."
        Write-Host $message
        $message | Out-File -FilePath $outputFile -Encoding utf8
        
        # Initialize state
        $newState = @{
            lastCheck = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
            pageHash = $hash
            notified = $false
        } | ConvertTo-Json
        $newState | Out-File -FilePath $stateFile -Encoding utf8
    }
    
    # Update state file
    $newState = @{
        lastCheck = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        pageHash = $hash
    } | ConvertTo-Json
    $newState | Out-File -FilePath $stateFile -Encoding utf8
    
}
catch {
    $errorMsg = "ERROR: Check failed: $($_.Exception.Message)`nTime: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Host $errorMsg
    $errorMsg | Out-File -FilePath $outputFile -Encoding utf8
}
