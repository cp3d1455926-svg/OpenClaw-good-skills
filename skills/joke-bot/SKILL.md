# 😄 Joke Bot - 笑话大全

中英文笑话、每日一笑、分类浏览的娱乐助手。

## 功能列表

- ✅ 随机笑话推荐
- ✅ 每日一笑
- ✅ 按分类浏览
- ✅ 搜索笑话
- ✅ 添加笑话
- ✅ 评分系统
- ✅ 热门排行

## 使用示例

```
随机笑话：random
程序员笑话：random 程序员
每日一笑：daily
添加笑话：add 今天讲了个笑话 #日常
搜索笑话：search 小明
评分：rate 1 5
排行榜：top
```

## 笑话分类

- 程序员
- 小明
- 动物
- 冷笑话
- 学习
- 数字
- 日常
- 英文笑话

## 数据格式

```json
{
  "jokes": [
    {
      "id": 1,
      "content": "为什么程序员分不清万圣节和圣诞节？",
      "category": "程序员",
      "language": "zh",
      "rating": 4.5
    }
  ]
}
```

## 文件结构

```
joke-bot/
├── SKILL.md
├── joke.py
└── data/
    ├── jokes.json
    └── history.json
```

## 依赖

无外部依赖，使用 Python 标准库

## 作者

小鬼 👻

## 版本

v1.0
