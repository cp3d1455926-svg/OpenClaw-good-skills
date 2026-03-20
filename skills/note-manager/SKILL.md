# 📝 Note Manager - 笔记管理

快速记录、标签分类、搜索查询的轻量级笔记工具。

## 功能列表

- ✅ 创建/编辑/删除笔记
- ✅ 标签分类管理
- ✅ 全文搜索
- ✅ 按标签筛选
- ✅ 笔记统计

## 使用示例

```
新建笔记：new 今天学习了 Python #学习 #编程
查看笔记：list
搜索笔记：search Python
按标签搜：search #学习
```

## 数据格式

```json
{
  "notes": [
    {
      "id": 1,
      "title": "笔记 #1",
      "content": "今天学习了 Python",
      "tags": ["学习", "编程"],
      "created_at": "2026-03-20T10:00:00",
      "updated_at": "2026-03-20T10:00:00"
    }
  ]
}
```

## 文件结构

```
note-manager/
├── SKILL.md
├── note.py
└── data/
    └── notes.json
```

## 依赖

无外部依赖，使用 Python 标准库

## 作者

小鬼 👻

## 版本

v1.0
