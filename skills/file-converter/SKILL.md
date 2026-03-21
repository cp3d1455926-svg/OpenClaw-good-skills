# File Converter - 文件格式转换器

📄 支持多种文件格式转换，一键搞定！

## 功能

- 📝 文档转换（Word/Excel/PPT/PDF）
- 🖼️ 图片转换（JPG/PNG/GIF/WebP）
- 🎵 音频转换（MP3/WAV/FLAC/AAC）
- 🎬 视频转换（MP4/AVI/MOV/MKV）
- 📦 压缩解压（ZIP/RAR/7Z）
- 🔗 URL 转文件
- 📱 手机格式适配
- 🎨 批量转换

## 使用方法

### 文档转换
```
转换文件 file.docx 转 pdf
PDF 转 Word file.pdf
Excel 转 CSV data.xlsx
```

### 图片转换
```
图片转格式 photo.jpg 转 png
PNG 转 JPG image.png
WebP 转 PNG image.webp
```

### 音视频转换
```
视频转 MP4 video.avi
音频转 MP3 song.wav
提取视频音频 video.mp4
```

### 批量转换
```
批量转换 文件夹路径 转 pdf
压缩图片 文件夹 质量：80%
```

## 特性

✅ 支持 50+ 种格式
✅ 保持原格式质量
✅ 批量处理
✅ 云端/本地转换
✅ 自动识别格式
✅ 压缩优化
✅ 元数据保留
✅ 转换历史记录

## 示例输出

### 文档转换
```
📄 文件转换完成

📝 类型：Word → PDF
📁 原文件：report.docx (2.5MB)
📁 新文件：report.pdf (1.8MB)
⏱️ 用时：3.2 秒
📊 压缩率：28%

💾 保存位置：
C:\Users\...\report.pdf

✅ 转换成功！
```

### 图片批量转换
```
🖼️ 批量图片转换

📁 源文件夹：/photos (15 张)
🔄 格式：JPG → PNG
⏱️ 总用时：12.5 秒
📊 成功：15 张
❌ 失败：0 张

💾 输出文件夹：
/photos/converted/

✅ 全部转换完成！
```

### 视频转换
```
🎬 视频转换完成

📹 类型：AVI → MP4
📁 原文件：video.avi (125MB)
📁 新文件：video.mp4 (98MB)
⏱️ 用时：45 秒
📊 压缩率：22%
🎞️ 分辨率：1920x1080
🎬 编码：H.264

💾 保存位置：
C:\Users\...\video.mp4

✅ 转换成功！
```

## 配置

在 `config.json` 中设置：
- `outputDir`: 输出目录
- `quality`: 默认质量（90%）
- `maxSize`: 最大文件大小
- `formats`: 支持的格式列表

## 开发者

小鬼 👻

## 版本

v1.0.0
