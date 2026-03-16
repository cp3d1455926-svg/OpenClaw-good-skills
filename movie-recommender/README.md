# 🎬 Movie Recommender - 电影推荐助手

## 📖 功能说明

根据心情、类型推荐电影，支持豆瓣评分查询、观影记录管理。

## 🚀 使用方法

### 在 OpenClaw 中使用

```
推荐电影
今天有点累，推荐电影
查一下星际穿越的评分
喜欢《星际穿越》，推荐类似的
```

### Python 脚本调用

```python
from movie_recommender import main

# 心情推荐
result = main("今天有点累，推荐电影")
print(result)

# 类型推荐
result = main("推荐科幻电影")
print(result)

# 搜索电影
result = main("查一下星际穿越的评分")
print(result)
```

## 📁 文件结构

```
movie-recommender/
├── SKILL.md              # 技能描述
├── movie_recommender.py  # 主程序
├── douban_api.py         # 豆瓣 API 对接
├── watched.json          # 已看电影记录（自动生成）
└── want_to_watch.json    # 想看列表（自动生成）
```

## 🔧 配置说明

### 豆瓣 API Key（可选）

1. 申请：https://developers.douban.com/
2. 编辑 `douban_api.py`，填入 API Key：
   ```python
   DOUBAN_API_KEY = "your_api_key"
   ```

## 📊 示例输出

```
😊 根据你的**放松**心情，推荐这 3 部电影：

1. 🎬 《绿皮书》(2018)
   ⭐ 豆瓣评分：8.9
   🎯 导演：彼得·法雷利
   📝 简介：黑人钢琴家与白人司机的公路之旅

2. 🎬 《三傻大闹宝莱坞》(2009)
   ⭐ 豆瓣评分：9.2
   🎯 导演：拉库马·希拉尼
   📝 简介：三个大学生挑战教育体制

3. 🎬 《触不可及》(2011)
   ⭐ 豆瓣评分：9.3
   🎯 导演：奥利维埃·纳卡什
   📝 简介：富豪与街头青年的友情故事
```

## 🛠️ 开发计划

- [x] 基础推荐功能
- [x] 心情匹配算法
- [x] 观影记录存储
- [ ] 豆瓣 API 完整对接
- [ ] 相似电影推荐优化
- [ ] 观影统计功能

## 📝 更新日志

### v1.1.0 (2026-03-16)
- ✨ 添加豆瓣 API 对接
- 🐛 修复推荐算法

### v1.0.0 (2026-03-16)
- 🎉 初始版本

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License
