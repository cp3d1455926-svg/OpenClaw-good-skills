# AliGenie Input Processor (Simple Version)

$inputFile = "C:\Users\shenz\.openclaw\workspace\memory\aligenie-input.txt"
$outputFile = "C:\Users\shenz\.openclaw\workspace\memory\aligenie-output.txt"

# Check if input file exists
if (-not (Test-Path $inputFile)) {
    Write-Host "No input file"
    exit 0
}

# Read input
$inputData = Get-Content $inputFile -Raw | ConvertFrom-Json
$message = $inputData.message

Write-Host "Processing: $message"

# Create response
$response = @"
{
  "status": "success",
  "query": "$message",
  "result": "你好！我是小鬼 (Little Ghost)，你的 AI 助手！我已收到你的指令。天猫精灵桥接功能优化版测试成功！",
  "timestamp": "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')",
  "source": "openclaw-optimized"
}
"@

# Write output
$response | Out-File $outputFile -Encoding UTF8
Write-Host "Response written"

# Delete input
Remove-Item $inputFile -Force
Write-Host "Input deleted"
Write-Host "Done!"
