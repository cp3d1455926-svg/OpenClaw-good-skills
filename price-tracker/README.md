# 💰 Price Tracker - 价格监控助手

## 📖 功能说明

价格监控、历史价格查询、降价提醒、多平台比价。

## 🚀 使用方法

### 在 OpenClaw 中使用

```
监控 https://item.jd.com/100012345.html
查历史价格
比价 iPhone 15 Pro
有降价吗
监控列表
```

### Python 脚本调用

```python
from price_tracker import main

# 比价
result = main("比价 iPhone 15 Pro")
print(result)

# 历史价格
result = main("查历史价格")
print(result)
```

## 📁 文件结构

```
price-tracker/
├── SKILL.md              # 技能描述
├── price_tracker.py      # 主程序
├── price_crawler.py      # 价格爬虫
├── watchlist.json        # 监控列表（自动生成）
└── price_history.json    # 历史价格（自动生成）
```

## 🔧 依赖安装

```bash
pip install requests beautifulsoup4
```

## 📊 示例输出

```
🔍 **多平台比价** iPhone 15 Pro 256GB

🏆1. 💰 拼多多
   价格：¥7599
   优惠：-¥0
   到手：¥7599
   配送：5 天达
   库存：✅

2. 🛍️ 天猫
   价格：¥7899
   优惠：-¥300
   到手：¥7599
   配送：3 天达
   库存：✅

3. 🛒 京东
   价格：¥7999
   优惠：-¥200
   到手：¥7799
   配送：次日达
   库存：✅

🏆 **推荐**：💰 拼多多 最便宜！
```

## 🛠️ 开发计划

- [x] 价格监控基础
- [x] 多平台比价
- [x] 降价检测
- [ ] 京东价格实时抓取
- [ ] 淘宝价格实时抓取
- [ ] 定时查询任务
- [ ] 降价推送

## ⚠️ 注意事项

- 拼多多价格需要第三方 API
- 电商平台可能反爬，建议用官方 API
- 价格数据仅供参考

## 📝 更新日志

### v1.1.0 (2026-03-16)
- ✨ 添加价格爬虫
- 🐛 修复比价算法

### v1.0.0 (2026-03-16)
- 🎉 初始版本

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License
