# ClawHub Slug 冲突检查脚本
$skillsRoot = "X:\npm\global\node_modules\openclaw\skills"
$outputFile = "C:\Users\shenz\.openclaw\workspace\slug_check_result.txt"

# 已确认的技能
$confirmed = @("countdown-timer", "life-memory-logger", "redbook-skills", "agent-browser-tool", "cn-life-toolkit", "book-recommender", "coding-lite", "movie-recommender", "news-evening-digest", "file-super-assistant", "goal-manager")

# 已确认冲突的
$conflicts = @("calendar-manager", "habit-tracker", "humanize-ai-text", "meeting-assistant", "expense-tracker", "obsidian-ontology-sync", "ppt-generator", "pollinations-ai", "proactive-agent", "self-improving-agent", "skill-creator", "skill-vetter", "summarize")

Write-Host "开始检查 Slug 冲突..."
Write-Host "已确认发布：$($confirmed.Count) 个"
Write-Host "已确认冲突：$($conflicts.Count) 个"
Write-Host ""

# 获取所有技能目录
$allSkills = Get-ChildItem -Path $skillsRoot -Directory | Where-Object { $_.Name -notlike ".*" } | Select-Object -ExpandProperty Name | Sort-Object

Write-Host "总技能数：$($allSkills.Count)"
Write-Host ""

# 输出结果
$result = @()
$result += "=== ClawHub Slug 冲突检查 ==="
$result += "检查时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$result += ""
$result += "总技能数：$($allSkills.Count)"
$result += ""
$result += "=== 已发布（跳过） ==="
$confirmed | ForEach-Object { $result += "- $_" }
$result += ""
$result += "=== 已确认冲突（不发布） ==="
$conflicts | ForEach-Object { $result += "- $_" }
$result += ""
$result += "=== 待检查 ==="

# 过滤掉已确认的
$toCheck = $allSkills | Where-Object { $_ -notin $confirmed -and $_ -notin $conflicts }

Write-Host "待检查：$($toCheck.Count) 个"
Write-Host ""

$count = 0
$available = @()
$newConflicts = @()

foreach ($slug in $toCheck) {
    $count++
    Write-Host "[$count/$($toCheck.Count)] Checking: $slug" -NoNewline
    
    # 检查 slug
    $checkResult = npx clawhub inspect $slug 2>&1
    
    if ($checkResult -match "Skill not found") {
        Write-Host " - ✓ 可用" -ForegroundColor Green
        $available += $slug
    } else {
        Write-Host " - ✗ 冲突" -ForegroundColor Red
        $newConflicts += $slug
    }
    
    # 避免速率限制
    Start-Sleep -Milliseconds 200
}

$result += "待检查数量：$($toCheck.Count)"
$result += ""
$result += "=== 检查结果 ==="
$result += "可用：$($available.Count)"
$result += "新增冲突：$($newConflicts.Count)"
$result += ""
$result += "=== 可用技能 ==="
$available | ForEach-Object { $result += "- $_" }
$result += ""
$result += "=== 新增冲突技能 ==="
$newConflicts | ForEach-Object { $result += "- $_" }

# 保存结果
$result | Out-File -FilePath $outputFile -Encoding utf8

Write-Host ""
Write-Host "=== 检查完成 ===" -ForegroundColor Cyan
Write-Host "可用：$($available.Count)" -ForegroundColor Green
Write-Host "新增冲突：$($newConflicts.Count)" -ForegroundColor Red
Write-Host ""
Write-Host "结果已保存：$outputFile"
