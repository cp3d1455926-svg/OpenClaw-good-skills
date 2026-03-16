#!/usr/bin/env python3
# 使用 Pollinations.AI 生成宣传图片 - 直接 URL 下载版

import requests
from pathlib import Path
import time

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)

# 图片生成 URL（直接访问）
IMAGES = {
    "cover": "https://image.pollinations.ai/prompt/Futuristic%20AI%20assistant%20dashboard%2038%20skill%20icons%20cyberpunk%20style%20neon%20colors?width=1024&height=1024&nologo=true",
    
    "skills_map": "https://image.pollinations.ai/prompt/Mind%20map%20of%2038%20AI%20skills%2012%20categories%20colorful%20icons%20clean%20design?width=1024&height=1024&nologo=true",
    
    "workflow": "https://image.pollinations.ai/prompt/AI%20workflow%20diagram%20text%20to%20action%20automation%20modern%20flat%20design?width=1024&height=1024&nologo=true",
    
    "code": "https://image.pollinations.ai/prompt/Programming%20code%20on%20screen%20Python%20syntax%20dark%20theme%20neon%20green?width=1024&height=1024&nologo=true",
    
    "github": "https://image.pollinations.ai/prompt/GitHub%20repository%20page%2038%20skills%20many%20stars%20open%20source?width=1024&height=1024&nologo=true"
}

def download_image(url, filename):
    """下载图片"""
    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            output_path = OUTPUT_DIR / filename
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"  Done: {filename}")
            return output_path
        else:
            print(f"  Failed: {filename}")
    except Exception as e:
        print(f"  Error: {e}")
    
    return None

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("Generating promotional images...\n")
    
    for name, url in IMAGES.items():
        download_image(url, f"{name}.png")
        time.sleep(2)  # 避免请求太快
    
    print("\nAll done!")
    print(f"Saved to: {OUTPUT_DIR}")
