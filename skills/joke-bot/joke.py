#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Joke Bot - 笑话大全
中英文笑话、每日一笑、分类浏览
"""

import json
import os
import random
from datetime import datetime
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
JOKES_FILE = os.path.join(DATA_DIR, 'jokes.json')
HISTORY_FILE = os.path.join(DATA_DIR, 'history.json')

# 内置笑话库（示例）
DEFAULT_JOKES = [
    {
        'id': 1,
        'content': '为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25！',
        'category': '程序员',
        'language': 'zh',
        'rating': 4.5
    },
    {
        'id': 2,
        'content': '有一天，0 对 8 说：胖就胖呗，还系什么腰带啊！',
        'category': '数字',
        'language': 'zh',
        'rating': 4.0
    },
    {
        'id': 3,
        'content': '为什么数学书总是很忧郁？因为它有太多的问题了！',
        'category': '学习',
        'language': 'zh',
        'rating': 3.8
    },
    {
        'id': 4,
        'content': 'Why do programmers prefer dark mode? Because light attracts bugs!',
        'category': 'Programmer',
        'language': 'en',
        'rating': 4.2
    },
    {
        'id': 5,
        'content': 'What do you call a fake noodle? An impasta!',
        'category': 'Food',
        'language': 'en',
        'rating': 3.9
    },
    {
        'id': 6,
        'content': '小明问爸爸：爸爸，我是不是傻孩子啊？爸爸说：傻孩子，你怎么会是傻孩子呢？',
        'category': '小明',
        'language': 'zh',
        'rating': 4.3
    },
    {
        'id': 7,
        'content': '有一天，火柴棍觉得头很痒，就挠啊挠啊，然后它着火了。',
        'category': '冷笑话',
        'language': 'zh',
        'rating': 4.1
    },
    {
        'id': 8,
        'content': '为什么企鹅只有肚子是白的？因为手短洗不到后背！',
        'category': '动物',
        'language': 'zh',
        'rating': 4.4
    },
    {
        'id': 9,
        'content': 'What\'s the best thing about Switzerland? I don\'t know, but the flag is a big plus!',
        'category': 'Geography',
        'language': 'en',
        'rating': 4.0
    },
    {
        'id': 10,
        'content': '老师：用"况且"造句。小明：一列火车经过，况且况且况且况且...',
        'category': '小明',
        'language': 'zh',
        'rating': 4.6
    }
]


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_jokes() -> List[Dict]:
    ensure_data_dir()
    if os.path.exists(JOKES_FILE):
        try:
            with open(JOKES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_JOKES.copy()
    return DEFAULT_JOKES.copy()


def save_jokes(jokes: List[Dict]):
    ensure_data_dir()
    with open(JOKES_FILE, 'w', encoding='utf-8') as f:
        json.dump(jokes, f, indent=2, ensure_ascii=False)


def load_history() -> List[Dict]:
    ensure_data_dir()
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_history(history: List[Dict]):
    ensure_data_dir()
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def get_random_joke(category: str = None, language: str = None) -> Dict:
    """获取随机笑话"""
    jokes = load_jokes()
    
    filtered = jokes
    if category:
        filtered = [j for j in filtered if j.get('category') == category]
    if language:
        filtered = [j for j in filtered if j.get('language') == language]
    
    if not filtered:
        return None
    
    return random.choice(filtered)


def get_daily_joke() -> Dict:
    """获取每日一笑"""
    jokes = load_jokes()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 根据日期选择固定的笑话
    index = hash(today) % len(jokes)
    return jokes[index]


def add_joke(content: str, category: str = '其他', language: str = 'zh') -> Dict:
    """添加新笑话"""
    jokes = load_jokes()
    
    joke_id = max([j.get('id', 0) for j in jokes], default=0) + 1
    
    joke = {
        'id': joke_id,
        'content': content,
        'category': category,
        'language': language,
        'rating': 0,
        'created_at': datetime.now().isoformat()
    }
    
    jokes.append(joke)
    save_jokes(jokes)
    
    return joke


def get_categories() -> List[str]:
    """获取所有分类"""
    jokes = load_jokes()
    categories = set(j.get('category', '其他') for j in jokes)
    return sorted(list(categories))


def rate_joke(joke_id: int, rating: float) -> bool:
    """评分笑话"""
    jokes = load_jokes()
    
    for joke in jokes:
        if joke.get('id') == joke_id:
            joke['rating'] = rating
            save_jokes(jokes)
            return True
    
    return False


def search_jokes(keyword: str) -> List[Dict]:
    """搜索笑话"""
    jokes = load_jokes()
    
    results = []
    for joke in jokes:
        if keyword.lower() in joke.get('content', '').lower():
            results.append(joke)
    
    return results


def run(command: str = '', args: List[str] = None) -> str:
    """主入口"""
    args = args or []
    
    if command == 'random' or command == '随机':
        category = args[0] if args else None
        joke = get_random_joke(category)
        
        if joke:
            return f"""
😄 随机笑话

{ joke['content'] }

分类：{ joke.get('category', '其他') }
评分：{'⭐' * int(joke.get('rating', 0))}
            """.strip()
        else:
            return "😅 未找到笑话"
    
    elif command == 'daily' or command == '每日':
        joke = get_daily_joke()
        
        return f"""
📅 每日一笑

{ joke['content'] }

分类：{ joke.get('category', '其他') }
评分：{'⭐' * int(joke.get('rating', 0))}

明天再来哦！
        """.strip()
    
    elif command == 'add' or command == '添加':
        content = ' '.join(args) if args else ''
        
        if not content:
            return "❌ 请提供笑话内容"
        
        # 解析分类 #category
        category = '其他'
        words = content.split()
        for word in words:
            if word.startswith('#'):
                category = word[1:]
                content = content.replace(word, '').strip()
        
        joke = add_joke(content, category)
        return f"✅ 已添加笑话 #{joke['id']}\n分类：{category}"
    
    elif command == 'categories' or command == '分类':
        categories = get_categories()
        
        return "📂 笑话分类:\n" + '\n'.join(f"├─ {cat}" for cat in categories)
    
    elif command == 'search' or command == '搜索':
        keyword = ' '.join(args) if args else ''
        
        if not keyword:
            return "❌ 请提供搜索关键词"
        
        results = search_jokes(keyword)
        
        if not results:
            return f"😅 未找到包含 '{keyword}' 的笑话"
        
        lines = [f"🔍 搜索结果 ({len(results)} 条):"]
        for joke in results[:5]:
            preview = joke['content'][:40] + '...' if len(joke['content']) > 40 else joke['content']
            lines.append(f"├─ [{joke.get('category', '其他')}] {preview}")
        
        return '\n'.join(lines)
    
    elif command == 'rate' or command == '评分':
        if len(args) < 2:
            return "❌ 用法：rate [笑话 ID] [评分 1-5]"
        
        try:
            joke_id = int(args[0])
            rating = float(args[1])
            
            if 1 <= rating <= 5:
                if rate_joke(joke_id, rating):
                    return f"✅ 已评分 #{joke_id}: {'⭐' * int(rating)}"
                else:
                    return f"❌ 未找到笑话 #{joke_id}"
            else:
                return "❌ 评分范围 1-5"
        except ValueError:
            return "❌ 参数错误"
    
    elif command == 'top' or command == '排行':
        jokes = load_jokes()
        top_jokes = sorted(jokes, key=lambda x: x.get('rating', 0), reverse=True)[:5]
        
        lines = ["🏆 热门笑话排行:"]
        for i, joke in enumerate(top_jokes, 1):
            lines.append(f"{i}. [{joke.get('category', '其他')}] {joke['content'][:30]}... {'⭐' * int(joke.get('rating', 0))}")
        
        return '\n'.join(lines)
    
    elif command == 'help' or command == '帮助':
        return """
😄 Joke Bot - 笑话大全

可用命令:
  random/随机 [分类]          - 随机笑话
  daily/每日                 - 每日一笑
  add/添加 [内容] [#分类]      - 添加笑话
  categories/分类            - 查看所有分类
  search/搜索 [关键词]         - 搜索笑话
  rate/评分 [ID] [1-5]        - 评分笑话
  top/排行                   - 热门排行
  help/帮助                  - 显示帮助

示例:
  随机笑话：random
  程序员笑话：random 程序员
  每日一笑：daily
  添加笑话：add 今天讲了个笑话 #日常
  搜索笑话：search 小明
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
