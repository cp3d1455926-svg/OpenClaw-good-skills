#!/usr/bin/env python3
import urllib.request
import json

try:
    response = urllib.request.urlopen('http://localhost:19000/api/openclaw/status', timeout=5)
    data = json.loads(response.read().decode())
    print("API 响应成功！")
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"错误：{e}")
