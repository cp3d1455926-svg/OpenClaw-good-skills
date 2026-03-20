#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meme Maker - 表情包生成器
文字 + 模板生成表情包
"""

import os
from typing import List, Dict

# 内置表情包模板
MEME_TEMPLATES = {
    '1': {
        'name': '熊猫头',
        'text_positions': ['top', 'bottom'],
        'example': '上方文字/下方文字'
    },
    '2': {
        'name': 'doge',
        'text_positions': ['center'],
        'example': '中间文字'
    },
    '3': {
        'name': '猫猫震惊',
        'text_positions': ['top', 'bottom'],
        'example': '上方文字/下方文字'
    },
    '4': {
        'name': '地铁老人手机',
        'text_positions': ['top'],
        'example': '上方文字'
    },
    '5': {
        'name': '好的老板',
        'text_positions': ['bottom'],
        'example': '下方文字'
    }
}

# 常用表情包文字
COMMON_TEXTS = {
    '上班': ['不想上班', '摸鱼中', '下班了', '加班快乐'],
    '学习': ['学习使我快乐', '考试必过', '作业写完了', '今天学习了吗'],
    '生活': ['我太难了', '笑死', '就离谱', '绝了'],
    '情感': ['单身狗', '恋爱了', '分手快乐', '想你了'],
    '通用': ['好的', '收到', '666', '牛逼', '笑死', '就这？', '就这？']
}


def get_templates() -> List[Dict]:
    """获取所有模板"""
    return [
        {'id': k, 'name': v['name'], 'example': v['example']}
        for k, v in MEME_TEMPLATES.items()
    ]


def get_common_texts(category: str = None) -> List[str]:
    """获取常用文字"""
    if category and category in COMMON_TEXTS:
        return COMMON_TEXTS[category]
    
    all_texts = []
    for texts in COMMON_TEXTS.values():
        all_texts.extend(texts)
    
    return all_texts


def generate_meme_text(top_text: str = '', bottom_text: str = '', center_text: str = '') -> str:
    """生成表情包文字"""
    parts = []
    
    if top_text:
        parts.append(f"【上】{top_text}")
    if center_text:
        parts.append(f"【中】{center_text}")
    if bottom_text:
        parts.append(f"【下】{bottom_text}")
    
    return '\n'.join(parts) if parts else '无文字'


def create_meme(template_id: str, text: str) -> Dict:
    """创建表情包"""
    template = MEME_TEMPLATES.get(template_id)
    
    if not template:
        return None
    
    # 解析文字
    if '/' in text:
        parts = text.split('/')
        top = parts[0] if len(parts) > 0 else ''
        bottom = parts[1] if len(parts) > 1 else ''
        center = ''
    else:
        top = ''
        bottom = ''
        center = text
    
    return {
        'template': template['name'],
        'top_text': top,
        'bottom_text': bottom,
        'center_text': center,
        'preview': generate_meme_text(top, bottom, center)
    }


def run(command: str = '', args: List[str] = None) -> str:
    """主入口"""
    args = args or []
    
    if command == 'templates' or command == '模板':
        templates = get_templates()
        
        lines = ["🖼️ 表情包模板:"]
        for t in templates:
            lines.append(f"├─ {t['id']}. {t['name']} - {t['example']}")
        
        return '\n'.join(lines)
    
    elif command == 'create' or command == '生成':
        if len(args) < 2:
            return "❌ 用法：create [模板 ID] [文字]\n例如：create 1 上方文字/下方文字"
        
        template_id = args[0]
        text = ' '.join(args[1:])
        
        meme = create_meme(template_id, text)
        
        if meme:
            return f"""
🖼️ 表情包已生成！

模板：{meme['template']}

{meme['preview']}

💡 提示：实际使用时需要图片处理库生成图片
            """.strip()
        else:
            return f"❌ 未知模板 ID '{template_id}'"
    
    elif command == 'texts' or command == '文字':
        category = args[0] if args else None
        
        if category and category not in COMMON_TEXTS:
            return f"❌ 未知分类 '{category}'\n可用：{', '.join(COMMON_TEXTS.keys())}"
        
        texts = get_common_texts(category)
        
        lines = [f"💬 常用表情包文字{f' - {category}' if category else ''}:"]
        for text in texts[:10]:
            lines.append(f"├─ {text}")
        
        if len(texts) > 10:
            lines.append(f"└─ ... 还有{len(texts) - 10}条")
        
        return '\n'.join(lines)
    
    elif command == 'random' or command == '随机':
        import random
        
        template_id = random.choice(list(MEME_TEMPLATES.keys()))
        template = MEME_TEMPLATES[template_id]
        
        all_texts = get_common_texts()
        text = random.choice(all_texts)
        
        meme = create_meme(template_id, text)
        
        return f"""
🎲 随机表情包

模板：{meme['template']}

{meme['preview']}
        """.strip()
    
    elif command == 'inspire' or command == '灵感':
        import random
        
        category = random.choice(list(COMMON_TEXTS.keys()))
        texts = COMMON_TEXTS[category]
        
        return f"""
💡 表情包灵感

分类：{category}

推荐文字:
{chr(10).join(f'├─ {t}' for t in texts[:5])}

试试：create [模板 ID] [文字]
        """.strip()
    
    elif command == 'help' or command == '帮助':
        return """
🖼️ Meme Maker - 表情包生成器

可用命令:
  templates/模板              - 查看所有模板
  create/生成 [ID] [文字]      - 生成表情包
  texts/文字 [分类]            - 常用文字
  random/随机                 - 随机生成
  inspire/灵感                - 获取灵感
  help/帮助                   - 显示帮助

示例:
  查看模板：templates
  生成表情：create 1 不想上班/摸鱼中
  常用文字：texts 上班
  随机生成：random
  获取灵感：inspire

模板列表:
1. 熊猫头 - 上方文字/下方文字
2. doge - 中间文字
3. 猫猫震惊 - 上方文字/下方文字
4. 地铁老人手机 - 上方文字
5. 好的老板 - 下方文字
        """.strip()
    
    else:
        return "❌ 未知命令，输入 help 查看帮助"


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print(run('help'))
    else:
        command = sys.argv[1]
        args = sys.argv[2:]
        print(run(command, args))
