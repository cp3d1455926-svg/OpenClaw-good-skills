# ClawHub Slug 冲突完整检查报告

**检查时间**: 2026-03-30 18:05  
**总技能数**: 92 个

---

## 📊 统计汇总

| 状态 | 数量 | 百分比 |
|------|------|--------|
| ✅ 已发布 | 11 | 12.0% |
| ✅ 可用（可发布） | 17 | 18.5% |
| ❌ 冲突（不发布） | 64 | 69.6% |
| **总计** | **92** | **100%** |

---

## ✅ 已发布（11 个）

1. countdown-timer
2. life-memory-logger
3. redbook-skills
4. agent-browser-tool
5. cn-life-toolkit
6. book-recommender (2.0.1)
7. coding-lite
8. movie-recommender
9. news-evening-digest
10. file-super-assistant
11. goal-manager

---

## ✅ 可用技能（17 个，可发布）

### 第 3 批待发布（5 个）
1. data-analytics-assistant
2. email-helper
3. news-digest-aggregator
4. news-noon-digest
5. multi-source-research

### 其他可用（12 个）
6. coding-agent
7. official-account-assistant
8. pdf-reader
9. skill-preflight-checker
10. tavily-search
11. travel-planner
12. voice-call
13. wacli
14. word-memory
15. xiaohongshu-assistant
16. music-helper ✓
17. quiz-generator ✓

---

## ❌ 冲突技能（64 个，不发布或需改名）

### 之前已确认冲突（13 个）
1. calendar-manager (jackeven02)
2. expense-tracker (aholake)
3. habit-tracker (jhillin8)
4. humanize-ai-text (moltbro)
5. meeting-assistant (scikkk)
6. obsidian-ontology-sync (parthpandya1729)
7. pollinations-ai (kanfred)
8. ppt-generator (wwlyzzyorg)
9. proactive-agent (halthelobster)
10. self-improving-agent (pskoett)
11. skill-creator (chindden)
12. skill-vetter (spclaudehome)
13. summarize (steipete)

### 新增冲突（51 个）
14. apple-notes
15. apple-reminders
16. bear-notes
17. blogwatcher
18. blucli
19. bluebubbles
20. camsnap
21. discord
22. eightctl
23. gh-issues
24. gifgrep
25. github
26. gog
27. goplaces
28. healthcheck
29. himalaya
30. imsg
31. mcporter
32. model-usage
33. nano-banana-pro
34. nano-pdf
35. notion
36. obsidian
37. ontology
38. openai-image-gen
39. openai-whisper
40. openai-whisper-api
41. openhue
42. oracle
43. ordercli
44. peekaboo
45. price-tracker
46. recipe-finder
47. sag
48. session-logs
49. sherpa-onnx-tts
50. slack
51. songsee
52. sonoscli
53. spotify-player
54. stock-watcher
55. things-mac
56. tmux
57. trello
58. video-frames
59. weather
60. xiaohongshu-publisher
61. xurl
62. 1password
63. clawhub
64. gemini

---

## 📋 发布计划更新

### 第 3 批（18:30，5 个）
- data-analytics-assistant ✓
- email-helper ✓
- news-digest-aggregator ✓
- news-noon-digest ✓
- multi-source-research ✓

### 第 4 批（5 个）
- music-helper ✓
- quiz-generator ✓
- coding-agent ✓
- official-account-assistant ✓
- pdf-reader ✓

### 第 5 批（5 个）
- skill-preflight-checker ✓
- tavily-search ✓
- travel-planner ✓
- voice-call ✓
- wacli ✓

### 第 6 批（2 个）
- word-memory ✓
- xiaohongshu-assistant ✓

---

## 💡 建议

### 方案 A：只发布可用的 17 个
- 简单直接
- 无冲突风险
- 今天可完成全部发布

### 方案 B：冲突技能加前缀后发布
- 例如：`cp3d-healthcheck`, `cp3d-notion`
- 可发布更多技能
- 需要逐个指定 slug

### 方案 C：放弃冲突技能
- 只发布 17 个可用的
- 64 个冲突的放弃

---

## 📈 对比之前统计

| 项目 | 之前 | 现在 | 差异 |
|------|------|------|------|
| 可用技能 | 64 个 | 17 个 | -47 个 |
| 冲突技能 | 13 个 | 64 个 | +51 个 |

**原因**: 之前只检查了部分技能，现在完整检查了所有 92 个技能，发现大部分常用名称已被占用。

---

**结论**: 大部分通用名称的技能 slug 已被其他人发布，建议：
1. 先发布 17 个可用的
2. 对于重要的冲突技能，考虑加前缀（如 `cp3d-`）重新发布
