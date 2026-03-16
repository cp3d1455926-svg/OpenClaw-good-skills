#!/usr/bin/env python3
# 使用 Pollinations.AI 生成宣传图片

import requests
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)

# 图片生成提示词
PROMPTS = {
    "cover": "Futuristic AI assistant dashboard, 38 skill icons, cyberpunk style, neon colors, tech background, high quality, digital art",
    
    "skills_map": "Mind map of 38 AI skills, 12 categories, colorful icons, clean design, infographic style, white background",
    
    "workflow": "AI workflow diagram, text to action, automation process, modern flat design, blue and purple gradient",
    
    "code": "Programming code on screen, Python syntax, dark theme, neon green text, hacker style, tech atmosphere",
    
    "github": "GitHub repository page mockup, 38 skills, many stars, open source project, professional design"
}

def generate_image(prompt, filename):
    """生成图片"""
    url = f"https://image.pollinations.ai/prompt/{prompt}"
    params = {
        "width": 1024,
        "height": 1024,
        "nologo": "true"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            output_path = OUTPUT_DIR / filename
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Done: {filename}")
            return output_path
        else:
            print(f"Failed: {filename}")
    except Exception as e:
        print(f"Error: {e}")
    
    return None

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("Generating images...")
    
    # 生成封面图
    generate_image(PROMPTS["cover"], "cover.png")
    
    # 生成技能地图
    generate_image(PROMPTS["skills_map"], "skills_map.png")
    
    # 生成工作流程图
    generate_image(PROMPTS["workflow"], "workflow.png")
    
    # 生成代码图
    generate_image(PROMPTS["code"], "code.png")
    
    # 生成 GitHub 截图
    generate_image(PROMPTS["github"], "github.png")
    
    print("\nAll images generated!")
    print(f"Save location: {OUTPUT_DIR}")
