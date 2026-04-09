# Kimi (MoonshotAI) GitHub Monitor Script
$stateFile = "C:\Users\shenz\.openclaw\workspace\memory\kimi-monitor-state.json"
$notifyFile = "C:\Users\shenz\.openclaw\workspace\memory\kimi-notify-pending.txt"

try {
    $response = Invoke-WebRequest -Uri "https://github.com/MoonshotAI" -UseBasicParsing -TimeoutSec 60
    $content = $response.Content
    
    # Check for K3
    $k3Found = $content -match "K3"
    $hash = Get-FileHash -InputStream ([System.IO.MemoryStream]::New([System.Text.Encoding]::UTF8.GetBytes($content))) -Algorithm MD5 | Select-Object -ExpandProperty Hash
    
    if (Test-Path $stateFile) {
        $lastState = Get-Content $stateFile -Raw | ConvertFrom-Json
        if ($k3Found -and -not $lastState.k3Found) {
            $msg = "Kimi K3 Released! Check https://github.com/MoonshotAI"
            @{type="alert"; message=$msg; url="https://github.com/MoonshotAI"} | ConvertTo-Json | Out-File $notifyFile -Encoding utf8
            Write-Host "ALERT: K3 detected!"
        }
    } else {
        Write-Host "INIT: Baseline saved (Kimi K2.5)"
        @{lastCheck=(Get-Date -Format "o"); pageHash=$hash; k3Found=$k3Found; currentModel="Kimi K2.5"} | ConvertTo-Json | Out-File $stateFile -Encoding utf8
    }
    
    @{lastCheck=(Get-Date -Format "o"); pageHash=$hash; k3Found=$k3Found} | ConvertTo-Json | Out-File $stateFile -Encoding utf8
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
}
