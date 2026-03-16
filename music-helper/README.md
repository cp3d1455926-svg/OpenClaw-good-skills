# 🎵 Music Helper - 音乐助手

## 📖 功能说明

根据场景、心情推荐音乐，支持歌词获取、歌单管理。

## 🚀 使用方法

### 在 OpenClaw 中使用

```
学习的时候听什么
推荐摇滚音乐
查一下晴天的歌词
收藏晴天
```

### Python 脚本调用

```python
from music_helper import main

# 场景推荐
result = main("学习的时候听什么")
print(result)

# 歌词查询
result = main("查一下晴天的歌词")
print(result)
```

## 📁 文件结构

```
music-helper/
├── SKILL.md              # 技能描述
├── music_helper.py       # 主程序
├── netease_api.py        # 网易云 API 对接
├── favorites.json        # 收藏列表（自动生成）
└── playlists.json        # 歌单列表（自动生成）
```

## 🔧 配置说明

### 网易云音乐 API

使用开源 API，无需配置即可使用基础功能。

如需完整功能，可部署自己的 API 服务：
1. 参考：https://github.com/Binaryify/NeteaseCloudMusicApi
2. 部署后修改 `netease_api.py` 中的 `NETEASE_BASE_URL`

## 📊 示例输出

```
🎧 适合**学习**的音乐：

1. 🎵 《Summer》- 久石让 ⭐4.9
2. 🎵 《雨的印记》- 李闰珉 ⭐4.8
3. 🎵 《卡农》- 帕赫贝尔 ⭐4.9
4. 🎵 《风居住的街道》- 矶村由纪子 ⭐4.8
5. 🎵 《神秘园之歌》- Secret Garden ⭐4.7
```

## 🛠️ 开发计划

- [x] 基础推荐功能
- [x] 歌词获取
- [x] 收藏管理
- [ ] 网易云 API 完整对接
- [ ] 歌单同步
- [ ] 每日推荐

## 📝 更新日志

### v1.1.0 (2026-03-16)
- ✨ 添加网易云 API 对接
- 🐛 修复歌词解析

### v1.0.0 (2026-03-16)
- 🎉 初始版本

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License
