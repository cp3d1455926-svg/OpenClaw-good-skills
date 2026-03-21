#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 像素办公室后端 API
实时同步 OpenClaw 状态到前端看板
"""

import json
import os
import subprocess
import threading
import time
from datetime import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder='../')
CORS(app)

# 状态文件路径
STATE_FILE = os.path.join(os.path.dirname(__file__), 'state.json')
MEMORY_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'memory')

# 当前状态
current_state = {
    'status': 'idle',
    'status_text': '待命中...',
    'model': 'bailian/qwen3.5-plus',
    'tokens_in': 372000,
    'tokens_out': 12000,
    'cost': 0.0,
    'context_usage': 8,
    'last_activity': None,
    'updated_at': None
}

def get_openclaw_status():
    """获取 OpenClaw 当前状态"""
    print('[Status] Getting status...')
    
    # 直接返回模拟数据
    status = get_simulated_status()
    
    print(f'[Status] Returning: {status}')
    
    return status

def parse_status_output(status_text):
    """解析 openclaw status 输出"""
    status = {
        'raw': status_text,
        'model': 'unknown',
        'tokens_in': 0,
        'tokens_out': 0,
        'cost': 0.0,
        'context_usage': 0
    }
    
    for line in status_text.split('\n'):
        if 'Model:' in line:
            status['model'] = line.split('Model:')[1].split('·')[0].strip()
        elif 'Tokens:' in line:
            parts = line.split('Tokens:')[1].strip().split('/')
            if len(parts) >= 2:
                try:
                    in_str = parts[0].strip().replace('k', '000').replace(' ', '')
                    out_str = parts[1].strip().split()[0].replace('k', '000')
                    status['tokens_in'] = int(float(in_str))
                    status['tokens_out'] = int(float(out_str))
                except:
                    pass
        elif 'Cost:' in line:
            try:
                status['cost'] = float(line.split('Cost:')[1].replace('$', '').strip())
            except:
                pass
        elif 'Context:' in line:
            try:
                percent = line.split('(')[1].replace(')', '').replace('%', '').strip()
                status['context_usage'] = int(percent)
            except:
                pass
    
    return status

def get_simulated_status():
    """获取模拟状态（用于演示）"""
    # 返回硬编码的默认值，避免循环依赖
    return {
        'model': 'bailian/qwen3.5-plus',
        'tokens_in': 372000,
        'tokens_out': 12000,
        'cost': 0.0,
        'context_usage': 8,
        'status': 'idle'
    }

def get_yesterday_memo():
    """获取昨日记忆"""
    try:
        yesterday = datetime.now().strftime('%Y-%m-%d')
        memo_file = os.path.join(MEMORY_DIR, f'{yesterday}.md')
        
        if os.path.exists(memo_file):
            with open(memo_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取关键信息
            lines = content.split('\n')
            memo = {
                'date': yesterday,
                'title': '',
                'tasks': [],
                'highlights': []
            }
            
            for line in lines:
                if line.startswith('# '):
                    memo['title'] = line.replace('# ', '').strip()
                elif line.startswith('- [x]') or line.startswith('- ✅'):
                    memo['tasks'].append(line.strip())
                elif '✅' in line and '完成' in line:
                    memo['highlights'].append(line.strip())
            
            return memo
        else:
            # 查找最近的记忆文件
            import glob
            memo_files = glob.glob(os.path.join(MEMORY_DIR, '*.md'))
            if memo_files:
                memo_files.sort(reverse=True)
                with open(memo_files[0], 'r', encoding='utf-8') as f:
                    return {'content': f.read()[:500]}
            
            return None
    except Exception as e:
        return {'error': str(e)}

def determine_status_from_activity():
    """根据活动自动判断状态"""
    # 这里可以扩展更多逻辑
    # 例如：检查是否有命令在执行、是否有搜索请求等
    return 'idle'

@app.route('/')
def index():
    """返回前端页面"""
    return send_file(os.path.join(os.path.dirname(__file__), '..', 'index_v5.html'))

@app.route('/api/status')
def api_status():
    """获取当前状态"""
    return jsonify(current_state)

@app.route('/api/openclaw/status')
def api_openclaw_status():
    """获取 OpenClaw 实时状态"""
    status = get_openclaw_status()
    return jsonify(status)

@app.route('/api/set_state', methods=['POST'])
def api_set_state():
    """手动设置状态"""
    global current_state
    
    data = request.json
    status = data.get('status', 'idle')
    status_text = data.get('text', '')
    
    current_state['status'] = status
    current_state['status_text'] = status_text
    current_state['updated_at'] = datetime.now().isoformat()
    
    # 同步到状态文件
    save_state()
    
    return jsonify({'success': True, 'state': current_state})

@app.route('/api/yesterday-memo')
def api_yesterday_memo():
    """获取昨日小记"""
    memo = get_yesterday_memo()
    return jsonify(memo if memo else {})

@app.route('/api/skills')
def api_skills():
    """获取技能列表"""
    skills_file = os.path.join(os.path.dirname(__file__), 'skills.json')
    if os.path.exists(skills_file):
        with open(skills_file, 'r', encoding='utf-8') as f:
            skills = json.load(f)
        return jsonify(skills)
    else:
        return jsonify([])

def save_state():
    """保存状态到文件"""
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(current_state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f'Error saving state: {e}')

def load_state():
    """从文件加载状态"""
    global current_state
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                saved_state = json.load(f)
            # 只加载状态和文本，不覆盖 tokens 数据
            current_state['status'] = saved_state.get('status', 'idle')
            current_state['status_text'] = saved_state.get('status_text', '待命中...')
    except Exception as e:
        print(f'Error loading state: {e}')

def auto_update_loop():
    """自动更新状态循环（每 5 秒）"""
    global current_state
    
    print('[AutoUpdate] Loop started')
    
    while True:
        try:
            print('[AutoUpdate] Fetching status...')
            
            # 获取 OpenClaw 状态
            oc_status = get_openclaw_status()
            
            print(f'[AutoUpdate] Got status: {oc_status}')
            
            # 更新状态
            current_state['model'] = oc_status.get('model', 'unknown')
            current_state['tokens_in'] = oc_status.get('tokens_in', 0)
            current_state['tokens_out'] = oc_status.get('tokens_out', 0)
            current_state['cost'] = oc_status.get('cost', 0.0)
            current_state['context_usage'] = oc_status.get('context_usage', 0)
            current_state['last_activity'] = datetime.now().isoformat()
            current_state['updated_at'] = datetime.now().isoformat()
            
            print(f'[AutoUpdate] Updated state: tokens_in={current_state["tokens_in"]}, tokens_out={current_state["tokens_out"]}')
            
            # 自动判断状态
            if current_state['status'] == 'idle':
                # 可以根据 tokens 变化自动切换状态
                pass
            
            # 保存状态
            save_state()
            
        except Exception as e:
            print(f'[AutoUpdate] Error: {e}')
        
        time.sleep(5)

if __name__ == '__main__':
    # 加载状态
    load_state()
    
    # 启动自动更新线程
    update_thread = threading.Thread(target=auto_update_loop, daemon=True)
    update_thread.start()
    
    print('[Lobster] OpenClaw Pixel Office Backend Starting...')
    print('[Dashboard] URL: http://127.0.0.1:19000')
    print('[API] Endpoint: http://127.0.0.1:19000/api/status')
    
    app.run(host='127.0.0.1', port=19000, debug=False)
