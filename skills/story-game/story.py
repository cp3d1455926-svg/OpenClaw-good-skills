#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Story Game - 故事接龙
AI 互动讲故事、创意写作
"""

import random
from typing import List, Dict

# 故事开头模板
STORY_STARTS = [
    "在一个风雨交加的夜晚，",
    "很久很久以前，有一个神秘的王国，",
    "2050 年，人类已经移民火星，",
    "小明醒来发现自己变成了会说话的猫，",
    "森林里住着一位会魔法的老奶奶，",
    "一艘宇宙飞船降落在学校操场上，",
    "传说中找到宝藏的人可以实现一个愿望，",
    "今天是开学第一天，我迟到了，",
]

# 故事元素
CHARACTERS = ['勇敢的骑士', '聪明的侦探', '调皮的精灵', '神秘的魔法师', '善良的公主', '邪恶的巫师', '外星访客', '时间旅行者']
LOCATIONS = ['古老的城堡', '神秘的森林', '繁华的都市', '遥远的星球', '海底世界', '云端之上', '地下迷宫', '魔法学院']
PLOT_TWISTS = [
    '突然，一道闪电划破天空...',
    '就在这时，门被推开了...',
    '没想到，这竟然是一个陷阱！',
    '原来，一切都是幻觉...',
    '奇迹发生了！',
    '时间仿佛静止了...',
    '一个熟悉的身影出现了...',
    '真相终于大白了！'
]


def generate_story_start() -> str:
    """生成故事开头"""
    return random.choice(STORY_STARTS)


def get_character() -> str:
    """获取角色"""
    return random.choice(CHARACTERS)


def get_location() -> str:
    """获取地点"""
    return random.choice(LOCATIONS)


def get_plot_twist() -> str:
    """获取剧情转折"""
    return random.choice(PLOT_TWISTS)


def continue_story(previous_text: str, user_input: str = '') -> str:
    """续写故事"""
    # 简单的续写逻辑（实际应该调用 AI）
    continuations = [
        f'{previous_text} {user_input} {get_plot_twist()}',
        f'{previous_text} 与此同时，{get_character()}正在{get_location()}等待着什么。',
        f'{previous_text} {user_input} 故事还没有结束，精彩还在继续...',
    ]
    
    return random.choice(continuations)


def create_story(theme: str = '') -> Dict:
    """创建故事框架"""
    return {
        'theme': theme or '奇幻冒险',
        'character': get_character(),
        'location': get_location(),
        'start': generate_story_start(),
        'twist': get_plot_twist()
    }


def run(command: str = '', args: List[str] = None) -> str:
    """主入口"""
    args = args or []
    
    if command == 'start' or command == '开始':
        theme = ' '.join(args) if args else '奇幻冒险'
        story = create_story(theme)
        
        return f"""
📖 故事接龙开始！

主题：{story['theme']}
主角：{story['character']}
地点：{story['location']}

故事开头：
{story['start']}

轮到你接龙了！输入你的故事内容...
        """.strip()
    
    elif command == 'continue' or command == '继续':
        previous = ' '.join(args[:-1]) if len(args) > 1 else ''
        user_input = args[-1] if args else ''
        
        continued = continue_story(previous, user_input)
        
        return f"""
📖 故事继续：

{continued}

接下来会发生什么？继续接龙吧！
        """.strip()
    
    elif command == 'twist' or command == '转折':
        return f"""
🎭 剧情转折：

{get_plot_twist()}

故事走向开始改变...
        """.strip()
    
    elif command == 'character' or command == '角色':
        return f"""
👤 新角色登场：

{get_character()}

Ta 会给故事带来什么变化？
        """.strip()
    
    elif command == 'location' or command == '地点':
        return f"""
🏰 新场景：

{get_location()}

故事将在这里展开...
        """.strip()
    
    elif command == 'random' or command == '随机':
        story = create_story()
        
        return f"""
🎲 随机故事元素：

主题：{story['theme']}
主角：{story['character']}
地点：{story['location']}
开头：{story['start']}
转折：{story['twist']}

用这些元素创作一个故事吧！
        """.strip()
    
    elif command == 'help' or command == '帮助':
        return """
📖 Story Game - 故事接龙

可用命令:
  start/开始 [主题]           - 开始新故事
  continue/继续 [内容]         - 续写故事
  twist/转折                 - 添加剧情转折
  character/角色              - 新角色登场
  location/地点               - 新场景
  random/随机                 - 随机故事元素
  help/帮助                   - 显示帮助

示例:
  开始故事：start 奇幻冒险
  继续：continue 小明走进了森林
  添加转折：twist
  随机元素：random

玩法说明:
1. 一人开头
2. 轮流接龙
3. 可以添加转折/角色/地点
4. 共同创作完整故事
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
