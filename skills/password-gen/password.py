#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Password Generator - 密码生成器
安全密码生成、强度检查、密码管理
"""

import json
import os
import random
import string
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
PASSWORDS_FILE = os.path.join(DATA_DIR, 'passwords.json')


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_passwords() -> List[Dict]:
    ensure_data_dir()
    if os.path.exists(PASSWORDS_FILE):
        try:
            with open(PASSWORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_passwords(passwords: List[Dict]):
    ensure_data_dir()
    with open(PASSWORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(passwords, f, indent=2, ensure_ascii=False)


def generate_password(length: int = 16, use_upper: bool = True, 
                      use_lower: bool = True, use_digits: bool = True, 
                      use_special: bool = True) -> str:
    """生成随机密码"""
    chars = ''
    
    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    if not chars:
        chars = string.ascii_lowercase + string.digits
    
    # 确保至少包含每种类型的一个字符
    password = []
    if use_lower:
        password.append(random.choice(string.ascii_lowercase))
    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice('!@#$%^&*()_+-=[]{}|;:,.<>?'))
    
    # 填充剩余长度
    remaining = length - len(password)
    password.extend(random.choice(chars) for _ in range(remaining))
    
    # 打乱顺序
    random.shuffle(password)
    
    return ''.join(password)


def check_strength(password: str) -> Dict:
    """检查密码强度"""
    score = 0
    feedback = []
    
    # 长度检查
    if len(password) >= 16:
        score += 3
    elif len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ 密码太短，建议至少 12 位")
    
    # 字符类型检查
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("⚠️ 缺少小写字母")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("⚠️ 缺少大写字母")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("⚠️ 缺少数字")
    
    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        score += 2
    else:
        feedback.append("⚠️ 缺少特殊字符")
    
    # 常见模式检查
    common_patterns = ['123', 'abc', 'password', 'admin', 'qwerty']
    for pattern in common_patterns:
        if pattern in password.lower():
            score -= 1
            feedback.append(f"⚠️ 包含常见模式 '{pattern}'")
    
    # 重复字符检查
    if len(set(password)) < len(password) * 0.6:
        score -= 1
        feedback.append("⚠️ 重复字符过多")
    
    # 评级
    if score >= 8:
        level = "💪 非常强"
        color = "🟢"
    elif score >= 6:
        level = "👍 强"
        color = "🟡"
    elif score >= 4:
        level = "⚠️ 中等"
        color = "🟠"
    else:
        level = "❌ 弱"
        color = "🔴"
    
    return {
        'score': score,
        'level': level,
        'color': color,
        'feedback': feedback if feedback else ["✅ 密码强度良好"]
    }


def save_password(service: str, username: str, password: str, notes: str = '') -> Dict:
    """保存密码（加密存储）"""
    passwords = load_passwords()
    
    # 检查是否已存在
    for p in passwords:
        if p.get('service') == service and p.get('username') == username:
            p['password_hash'] = hashlib.sha256(password.encode()).hexdigest()
            p['notes'] = notes
            p['updated_at'] = datetime.now().isoformat()
            save_passwords(passwords)
            return p
    
    # 新建
    entry = {
        'id': len(passwords) + 1,
        'service': service,
        'username': username,
        'password_hash': hashlib.sha256(password.encode()).hexdigest(),
        'password_hint': password[:2] + '*' * (len(password) - 2) if len(password) > 2 else '**',
        'notes': notes,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    passwords.append(entry)
    save_passwords(passwords)
    
    return entry


def get_password(service: str) -> Dict:
    """获取密码"""
    passwords = load_passwords()
    
    for p in passwords:
        if p.get('service', '').lower() == service.lower():
            return p
    
    return None


def list_passwords() -> List[Dict]:
    """列出所有密码（不显示完整密码）"""
    passwords = load_passwords()
    
    return [
        {
            'id': p['id'],
            'service': p['service'],
            'username': p['username'],
            'password_hint': p.get('password_hint', '***'),
            'updated_at': p.get('updated_at')
        }
        for p in passwords
    ]


def verify_password(service: str, password: str) -> bool:
    """验证密码"""
    entry = get_password(service)
    
    if not entry:
        return False
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return entry.get('password_hash') == password_hash


def run(command: str = '', args: List[str] = None) -> str:
    """主入口"""
    args = args or []
    
    if command == 'generate' or command == '生成':
        length = 16
        
        # 解析参数
        for arg in args:
            if arg.isdigit():
                length = int(arg)
        
        password = generate_password(length)
        strength = check_strength(password)
        
        return f"""
🔐 生成的密码:

{password}

强度：{strength['color']} {strength['level']}
长度：{len(password)} 位

💡 建议：保存到密码管理器或安全的地方
        """.strip()
    
    elif command == 'check' or command == '检查':
        password = ' '.join(args) if args else ''
        
        if not password:
            return "❌ 请提供要检查的密码"
        
        strength = check_strength(password)
        
        lines = [
            f"🔍 密码强度检查:",
            "",
            f"密码：{password[:2]}{'*' * (len(password) - 2)}",
            f"长度：{len(password)} 位",
            f"强度：{strength['color']} {strength['level']}",
            f"评分：{strength['score']}/10",
            "",
            "反馈:"
        ]
        
        for f in strength['feedback']:
            lines.append(f"├─ {f}")
        
        return '\n'.join(lines)
    
    elif command == 'save' or command == '保存':
        if len(args) < 3:
            return "❌ 用法：save [服务名] [用户名] [密码]"
        
        service = args[0]
        username = args[1]
        password = args[2]
        notes = ' '.join(args[3:]) if len(args) > 3 else ''
        
        entry = save_password(service, username, password, notes)
        
        return f"""
✅ 密码已保存

服务：{entry['service']}
用户名：{entry['username']}
提示：{entry['password_hint']}

⚠️ 注意：密码已加密存储，无法直接查看
        """.strip()
    
    elif command == 'list' or command == '列表':
        passwords = list_passwords()
        
        if not passwords:
            return "📭 暂无保存的密码"
        
        lines = [f"🔐 已保存的密码 ({len(passwords)} 个):"]
        
        for p in passwords:
            updated = datetime.fromisoformat(p['updated_at']).strftime('%Y-%m-%d') if p.get('updated_at') else '未知'
            lines.append(f"├─ #{p['id']} {p['service']} ({p['username']})")
            lines.append(f"│  提示：{p['password_hint']} | 更新：{updated}")
        
        return '\n'.join(lines)
    
    elif command == 'get' or command == '获取':
        if not args:
            return "❌ 请提供服务名"
        
        service = args[0]
        entry = get_password(service)
        
        if entry:
            return f"""
🔐 密码信息

服务：{entry['service']}
用户名：{entry['username']}
提示：{entry['password_hint']}
备注：{entry.get('notes', '无')}
            """.strip()
        else:
            return f"❌ 未找到服务 '{service}' 的密码"
    
    elif command == 'verify' or command == '验证':
        if len(args) < 2:
            return "❌ 用法：verify [服务名] [密码]"
        
        service = args[0]
        password = args[1]
        
        if verify_password(service, password):
            return "✅ 密码正确"
        else:
            return "❌ 密码错误或服务不存在"
    
    elif command == 'stats' or command == '统计':
        passwords = load_passwords()
        
        return f"""
📊 密码管理统计:
├─ 已保存：{len(passwords)} 个密码
└─ 服务数：{len(set(p['service'] for p in passwords))} 个服务
        """.strip()
    
    elif command == 'help' or command == '帮助':
        return """
🔐 Password Generator - 密码生成器

可用命令:
  generate/生成 [长度]          - 生成随机密码 (默认 16 位)
  check/检查 [密码]             - 检查密码强度
  save/保存 [服务] [用户] [密码]  - 保存密码
  list/列表                    - 列出所有密码
  get/获取 [服务]               - 获取密码信息
  verify/验证 [服务] [密码]      - 验证密码
  stats/统计                   - 查看统计
  help/帮助                    - 显示帮助

示例:
  生成密码：generate 20
  检查强度：check MyP@ssw0rd
  保存密码：save github myuser MyP@ss123
  查看列表：list
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
