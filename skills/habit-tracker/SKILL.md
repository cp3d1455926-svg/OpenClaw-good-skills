# 🎯 Habit Tracker - 习惯追踪器

每日打卡、统计分析、习惯养成的智能助手。

## 功能列表

- ✅ 添加/管理习惯
- ✅ 每日打卡签到
- ✅ 连续天数统计
- ✅ 完成率分析
- ✅ 今日打卡提醒

## 使用示例

```
添加习惯：add 早起跑步
打卡：checkin 1
查看今日：today
查看统计：stats
```

## 数据格式

```json
{
  "habits": [
    {
      "id": 1,
      "name": "早起跑步",
      "frequency": "daily",
      "goal": 30,
      "created_at": "2026-03-20T06:00:00"
    }
  ],
  "logs": [
    {
      "habit_id": 1,
      "date": "2026-03-20",
      "checked_at": "2026-03-20T06:30:00"
    }
  ]
}
```

## 文件结构

```
habit-tracker/
├── SKILL.md
├── habit.py
└── data/
    ├── habits.json
    └── logs.json
```

## 依赖

无外部依赖，使用 Python 标准库

## 作者

小鬼 👻

## 版本

v1.0
