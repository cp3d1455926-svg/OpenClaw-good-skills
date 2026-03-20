# 🔐 Password Generator - 密码生成器

安全密码生成、强度检查、密码管理的安全工具。

## 功能列表

- ✅ 随机密码生成（可定制长度）
- ✅ 密码强度检查
- ✅ 密码加密存储
- ✅ 密码验证
- ✅ 密码列表管理

## 使用示例

```
生成密码：generate 20
检查强度：check MyP@ssw0rd
保存密码：save github myuser MyP@ss123
查看列表：list
验证密码：verify github MyP@ss123
```

## 密码强度评级

- 💪 非常强 (8-10 分) - 绿色
- 👍 强 (6-7 分) - 黄色
- ⚠️ 中等 (4-5 分) - 橙色
- ❌ 弱 (0-3 分) - 红色

## 安全说明

- 密码使用 SHA-256 加密存储
- 不保存明文密码
- 支持密码提示功能

## 文件结构

```
password-gen/
├── SKILL.md
├── password.py
└── data/
    └── passwords.json
```

## 依赖

无外部依赖，使用 Python 标准库

## 作者

小鬼 👻

## 版本

v1.0
