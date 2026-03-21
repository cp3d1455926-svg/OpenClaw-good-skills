# 翻身文件箱 - 配置说明

## 📋 功能概述

**翻身文件箱** 是一个集成了隐私保护、多端同步、文件转换的智能文件管理工具。

---

## 🔐 隐私保护

### 文件加密
- **加密算法**: AES-256
- **密码要求**: 至少 8 位，包含大小写字母和数字
- **加密文件**: `.encrypted` 后缀

### 使用示例
```bash
# 加密文件
python flipfile.py encrypt secret.docx

# 解密文件
python flipfile.py decrypt secret.encrypted
```

### 安全建议
✅ 使用强密码
✅ 定期更换密码
✅ 开启双重验证
✅ 不要分享加密文件
✅ 定期备份加密文件

---

## 🔄 多端同步

### 支持的云平台
- 百度网盘
- 阿里云盘
- 腾讯微云
- OneDrive
- Google Drive
- Dropbox

### 同步设置
编辑 `config.json`:
```json
{
  "syncInterval": 5,
  "cloudProvider": "auto",
  "autoBackup": true
}
```

### 同步状态
```bash
python flipfile.py status
```

---

## 📄 文件转换

### 支持的格式

#### 文档类
- Word (.doc, .docx)
- PDF (.pdf)
- Excel (.xls, .xlsx)
- PowerPoint (.ppt, .pptx)
- TXT (.txt)

#### 图片类
- JPG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)
- BMP (.bmp)

#### 视频类
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WMV (.wmv)

### 使用示例
```bash
# 单个转换
python flipfile.py convert report.docx pdf

# 批量转换
python flipfile.py batch_convert ./documents pdf
```

---

## ⚙️ 配置文件

### config.json
```json
{
  "encryptAlgo": "AES-256",
  "syncInterval": 5,
  "cloudProvider": "auto",
  "convertQuality": 90,
  "autoBackup": true,
  "secureSpacePath": "C:\\FlipFile\\Secure",
  "maxVersions": 10
}
```

### 环境变量
```bash
# Windows PowerShell
$env:FLIPFILE_API_KEY="你的 API 密钥"
$env:CLOUD_STORAGE_PATH="D:\\CloudStorage"

# Linux/Mac
export FLIPFILE_API_KEY="你的 API 密钥"
export CLOUD_STORAGE_PATH="~/CloudStorage"
```

---

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install cryptography requests
```

### 2. 配置
编辑 `config.json` 设置云存储路径

### 3. 创建隐私空间
```bash
python flipfile.py createspace C:\FlipFile\Secure
```

### 4. 开始使用
```bash
# 加密文件
python flipfile.py encrypt secret.docx

# 转换文件
python flipfile.py convert photo.jpg png

# 查看同步状态
python flipfile.py status
```

---

## 🔒 安全提示

- ⚠️ 不要将密码告诉他人
- ⚠️ 不要在公共电脑使用隐私空间
- ⚠️ 定期备份重要文件
- ⚠️ 使用强密码
- ⚠️ 开启双重验证

---

## 📊 版本历史

### v1.0.0 (2026-03-21)
- ✅ 文件加密/解密
- ✅ 隐私空间创建
- ✅ 文件粉碎
- ✅ 文件转换
- ✅ 批量转换
- ✅ 同步状态查看

---

**开发者**: 小鬼 👻  
**版本**: v1.0.0  
**创建日期**: 2026-03-21
