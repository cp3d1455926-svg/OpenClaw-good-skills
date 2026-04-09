# Stop all OpenClaw processes
Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Stop-Process -Force

# Wait 5 seconds
Start-Sleep -Seconds 5

# Delete locked database
Remove-Item "C:\Users\shenz\.openclaw\memory\main.sqlite" -Force
Remove-Item "C:\Users\shenz\.openclaw\memory\main.sqlite-journal" -Force -ErrorAction SilentlyContinue

# Reindex
openclaw memory index --force

Write-Host "Memory database rebuilt successfully!"
