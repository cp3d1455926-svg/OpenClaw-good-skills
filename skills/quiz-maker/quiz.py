#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz Maker - 测试生成器
知识测验、答题闯关、自动评分
"""

import json
import os
import random
from datetime import datetime
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
QUIZZES_FILE = os.path.join(DATA_DIR, 'quizzes.json')
RESULTS_FILE = os.path.join(DATA_DIR, 'results.json')

# 内置题库（示例）
DEFAULT_QUIZZES = [
    {
        'id': 1,
        'category': 'Python',
        'question': 'Python 中哪个关键字用于定义函数？',
        'options': ['def', 'function', 'func', 'define'],
        'answer': 0,
        'difficulty': 'easy'
    },
    {
        'id': 2,
        'category': 'Python',
        'question': '以下哪个不是 Python 的数据类型？',
        'options': ['list', 'tuple', 'array', 'dict'],
        'answer': 2,
        'difficulty': 'medium'
    },
    {
        'id': 3,
        'category': '常识',
        'question': '中国的首都是？',
        'options': ['上海', '北京', '广州', '深圳'],
        'answer': 1,
        'difficulty': 'easy'
    },
    {
        'id': 4,
        'category': '常识',
        'question': '一年有多少天？',
        'options': ['365', '366', '364', '365 或 366'],
        'answer': 3,
        'difficulty': 'easy'
    },
    {
        'id': 5,
        'category': '英语',
        'question': '"Hello" 的中文意思是？',
        'options': ['再见', '你好', '谢谢', '对不起'],
        'answer': 1,
        'difficulty': 'easy'
    },
    {
        'id': 6,
        'category': '数学',
        'question': '15 × 8 = ?',
        'options': ['120', '125', '115', '130'],
        'answer': 0,
        'difficulty': 'medium'
    },
    {
        'id': 7,
        'category': '科技',
        'question': 'CPU 的中文名称是？',
        'options': ['中央处理器', '图形处理器', '内存', '硬盘'],
        'answer': 0,
        'difficulty': 'medium'
    },
    {
        'id': 8,
        'category': '历史',
        'question': '唐朝建立于哪一年？',
        'options': ['618 年', '620 年', '615 年', '625 年'],
        'answer': 0,
        'difficulty': 'hard'
    }
]


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_quizzes() -> List[Dict]:
    ensure_data_dir()
    if os.path.exists(QUIZZES_FILE):
        try:
            with open(QUIZZES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_QUIZZES.copy()
    return DEFAULT_QUIZZES.copy()


def save_quizzes(quizzes: List[Dict]):
    ensure_data_dir()
    with open(QUIZZES_FILE, 'w', encoding='utf-8') as f:
        json.dump(quizzes, f, indent=2, ensure_ascii=False)


def load_results() -> List[Dict]:
    ensure_data_dir()
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_results(results: List[Dict]):
    ensure_data_dir()
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def get_categories() -> List[str]:
    """获取所有分类"""
    quizzes = load_quizzes()
    categories = set(q.get('category', '其他') for q in quizzes)
    return sorted(list(categories))


def generate_quiz(category: str = None, count: int = 5, difficulty: str = None) -> List[Dict]:
    """生成测验"""
    quizzes = load_quizzes()
    
    filtered = quizzes
    if category:
        filtered = [q for q in filtered if q.get('category') == category]
    if difficulty:
        filtered = [q for q in filtered if q.get('difficulty') == difficulty]
    
    # 随机选择题目
    selected = random.sample(filtered, min(count, len(filtered)))
    
    return selected


def check_answer(quiz_id: int, user_answer: int) -> bool:
    """检查答案"""
    quizzes = load_quizzes()
    
    for quiz in quizzes:
        if quiz.get('id') == quiz_id:
            return quiz.get('answer') == user_answer
    
    return False


def save_result(username: str, category: str, score: int, total: int, answers: List[Dict]):
    """保存测试结果"""
    results = load_results()
    
    result = {
        'id': len(results) + 1,
        'username': username,
        'category': category,
        'score': score,
        'total': total,
        'percentage': round(score / total * 100, 1) if total > 0 else 0,
        'answers': answers,
        'completed_at': datetime.now().isoformat()
    }
    
    results.append(result)
    save_results(results)
    
    return result


def get_stats(username: str = None) -> Dict:
    """获取统计信息"""
    results = load_results()
    
    if username:
        results = [r for r in results if r.get('username') == username]
    
    if not results:
        return None
    
    total_tests = len(results)
    avg_score = sum(r.get('percentage', 0) for r in results) / total_tests
    best_score = max(r.get('percentage', 0) for r in results)
    
    return {
        'total_tests': total_tests,
        'avg_score': round(avg_score, 1),
        'best_score': round(best_score, 1),
        'total_questions': sum(r.get('total', 0) for r in results),
        'correct_answers': sum(r.get('score', 0) for r in results)
    }


def run(command: str = '', args: List[str] = None) -> str:
    """主入口"""
    args = args or []
    
    if command == 'start' or command == '开始':
        category = None
        count = 5
        
        # 解析参数
        for arg in args:
            if arg.isdigit():
                count = int(arg)
            elif arg in get_categories():
                category = arg
        
        quizzes = generate_quiz(category, count)
        
        if not quizzes:
            return "😅 未找到符合条件的题目"
        
        lines = [f"📝 测验开始！共{len(quizzes)}题\n"]
        
        for i, quiz in enumerate(quizzes, 1):
            lines.append(f"{i}. [{quiz.get('category', '其他')}] {quiz['question']}")
            for j, option in enumerate(quiz['options']):
                lines.append(f"   {chr(65+j)}. {option}")
            lines.append("")
        
        lines.append("作答格式：answer [题号] [选项]\n例如：answer 1 A")
        
        return '\n'.join(lines)
    
    elif command == 'answer' or command == '答题':
        if len(args) < 2:
            return "❌ 用法：answer [题号] [选项 A/B/C/D]"
        
        try:
            question_num = int(args[0])
            user_answer = args[1].upper()
            answer_index = ord(user_answer) - 65  # A=0, B=1, C=2, D=3
            
            # 这里简化处理，实际需要保存测验状态
            return f"✅ 已记录答案：第{question_num}题 选择{user_answer}"
        except:
            return "❌ 参数错误"
    
    elif command == 'categories' or command == '分类':
        categories = get_categories()
        
        return "📚 题目分类:\n" + '\n'.join(f"├─ {cat}" for cat in categories)
    
    elif command == 'add' or command == '添加':
        # 简化添加题目
        return """
📝 添加题目

格式：add [分类] [难度] [题目] [答案] [选项 A] [选项 B] [选项 C] [选项 D]

示例：
add Python easy Python 中哪个关键字用于定义函数？ A def B function C func D define

注意：答案用字母表示（A/B/C/D）
        """.strip()
    
    elif command == 'stats' or command == '统计':
        username = args[0] if args else None
        stats = get_stats(username)
        
        if not stats:
            return "📭 暂无测试记录"
        
        return f"""
📊 测试统计

测试次数：{stats['total_tests']}
平均得分：{stats['avg_score']}%
最高得分：{stats['best_score']}%
总题数：{stats['total_questions']}
正确数：{stats['correct_answers']}
        """.strip()
    
    elif command == 'practice' or command == '练习':
        category = args[0] if args else None
        quizzes = generate_quiz(category, 1)
        
        if not quizzes:
            return "😅 未找到题目"
        
        quiz = quizzes[0]
        
        return f"""
📖 每日练习

[{quiz.get('category', '其他')}] {quiz['question']}

A. {quiz['options'][0]}
B. {quiz['options'][1]}
C. {quiz['options'][2]}
D. {quiz['options'][3]}

答案：{chr(65 + quiz['answer'])}
        """.strip()
    
    elif command == 'help' or command == '帮助':
        return """
📝 Quiz Maker - 测试生成器

可用命令:
  start/开始 [分类] [数量]      - 开始测验
  answer/答题 [题号] [选项]      - 提交答案
  categories/分类              - 查看分类
  add/添加                     - 添加题目
  stats/统计 [用户名]           - 查看统计
  practice/练习 [分类]          - 每日练习
  help/帮助                    - 显示帮助

示例:
  开始测验：start Python 5
  开始测验：start 5
  答题：answer 1 A
  查看分类：categories
  每日练习：practice
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
