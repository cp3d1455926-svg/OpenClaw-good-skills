#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 OpenClaw 像素办公室 - Python 终端版
功能：技能可视化展示、实时状态看板
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 颜色定义
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # 前景色
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # 亮色
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    
    # 背景色
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"

# 技能数据
SKILLS = {
    "travel-planner": {
        "name": "旅行规划助手",
        "icon": "✈️",
        "version": "v2.0",
        "category": "生活",
        "codeSize": "19KB",
        "description": "行程规划、景点推荐、预算估算、打包清单",
        "features": [
            "🌍 12 个热门城市数据库",
            "🎯 10 种旅行模板",
            "🧳 个性化打包清单",
            "💡 旅行贴士"
        ]
    },
    "habit-tracker": {
        "name": "习惯养成助手",
        "icon": "🎯",
        "version": "v2.0",
        "category": "健康",
        "codeSize": "19KB",
        "description": "习惯打卡、统计分析、成就系统",
        "features": [
            "📚 20+ 习惯模板",
            "🏆 10 个成就徽章",
            "📊 统计报表",
            "⚡ 一键打卡"
        ]
    },
    "goal-manager": {
        "name": "目标管理助手",
        "icon": "🎯",
        "version": "v2.0",
        "category": "工作",
        "codeSize": "19KB",
        "description": "目标设定、SMART/OKR、进度跟踪",
        "features": [
            "📋 13 个目标模板",
            "📐 OKR+SMART 框架",
            "📝 5 种复盘模板",
            "📊 进度追踪"
        ]
    },
    "expense-tracker": {
        "name": "记账助手",
        "icon": "💰",
        "version": "v2.0",
        "category": "生活",
        "codeSize": "18KB",
        "description": "记账、统计、预算、储蓄",
        "features": [
            "📊 10 大类 20+ 子分类",
            "💰 预算预警",
            "🎯 储蓄目标",
            "🔍 消费分析"
        ]
    }
}

class PixelOffice:
    """像素办公室主类"""
    
    def __init__(self):
        self.width = 80
        self.height = 40
        self.selected_index = 0
        
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_header(self):
        """绘制头部"""
        print(f"{Colors.BG_CYAN}{Colors.BLACK}", end="")
        print("🦞 OpenClaw 像素办公室 ".center(self.width), end="")
        print(f"{Colors.RESET}")
        
        print(f"{Colors.CYAN}", end="")
        print("技能可视化展示中心 ".center(self.width), end="")
        print(f"{Colors.RESET}\n")
    
    def draw_lobster(self):
        """绘制像素龙虾"""
        lobster_art = """
    🦞
   ╱|
  | |  像素龙虾工作中...
  | |
  |/
        """
        print(f"{Colors.BRIGHT_CYAN}{lobster_art}{Colors.RESET}")
    
    def draw_divider(self, char="═"):
        """绘制分隔线"""
        print(f"{Colors.DIM}{char * self.width}{Colors.RESET}")
    
    def draw_skill_card(self, key, skill, index, selected=False):
        """绘制技能卡片"""
        border_color = Colors.BRIGHT_YELLOW if selected else Colors.DIM
        name_color = Colors.BRIGHT_GREEN if selected else Colors.WHITE
        
        # 标题栏
        print(f"{border_color}╔════════════════════════════════════════╗{Colors.RESET}")
        
        # 技能图标和名称
        version_tag = f" {skill['version']} " if skill.get('version') == 'v2.0' else ""
        title = f"  {skill['icon']} {skill['name']}{version_tag}"
        print(f"{border_color}║{Colors.RESET}{name_color}{title:<38}{border_color}║{Colors.RESET}")
        
        # 描述
        desc = f"  {skill['description'][:36]}"
        print(f"{border_color}║{Colors.RESET}{Colors.DIM}{desc:<38}{border_color}║{Colors.RESET}")
        
        # 代码量和分类
        info = f"  💾 {skill['codeSize']} | 📂 {skill['category']}"
        print(f"{border_color}║{Colors.RESET}{Colors.DIM}{info:<38}{border_color}║{Colors.RESET}")
        
        # 底栏
        print(f"{border_color}╚════════════════════════════════════════╝{Colors.RESET}")
        
        if selected:
            print(f"\n  {Colors.BRIGHT_CYAN}功能特性:{Colors.RESET}")
            for feature in skill.get('features', [])[:3]:
                print(f"    {feature}")
            print()
    
    def draw_status_board(self):
        """绘制状态看板"""
        print(f"\n{Colors.BG_BLUE}{Colors.WHITE}  📊 实时状态看板 {Colors.RESET}\n")
        
        # 模拟数据
        stats = {
            "今日打卡": 15,
            "目标进度": 67,
            "本月支出": 3580,
            "技能总数": 43
        }
        
        for label, value in stats.items():
            if label == "目标进度":
                bar_len = value // 10
                bar = "█" * bar_len + "░" * (10 - bar_len)
                print(f"  {label}: [{Colors.GREEN}{bar}{Colors.RESET}] {value}%")
            elif label == "本月支出":
                print(f"  {label}: {Colors.YELLOW}¥{value}{Colors.RESET}")
            else:
                print(f"  {label}: {Colors.BRIGHT_CYAN}{value}{Colors.RESET}")
        
        print()
    
    def draw_menu(self):
        """绘制菜单"""
        print(f"\n{Colors.DIM}  按 1-4 查看技能详情 | Q 退出 | R 刷新{Colors.RESET}\n")
    
    def show_skill_detail(self, key, skill):
        """显示技能详情"""
        self.clear_screen()
        
        print(f"\n{Colors.BRIGHT_YELLOW}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}  {skill['icon']} {skill['name']} {skill.get('version', '')}{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}{'═' * 60}{Colors.RESET}\n")
        
        print(f"  {Colors.WHITE}📝 描述:{Colors.RESET} {skill['description']}")
        print(f"  {Colors.WHITE}💾 代码量:{Colors.RESET} {skill['codeSize']}")
        print(f"  {Colors.WHITE}📂 分类:{Colors.RESET} {skill['category']}\n")
        
        print(f"  {Colors.BRIGHT_CYAN}✨ 功能特性:{Colors.RESET}")
        for feature in skill.get('features', []):
            print(f"    {feature}")
        
        print(f"\n{Colors.DIM}  按任意键返回...{Colors.RESET}")
        input()
    
    def main_menu(self):
        """主菜单"""
        while True:
            self.clear_screen()
            
            self.draw_header()
            self.draw_lobster()
            self.draw_divider()
            
            print(f"\n{Colors.BRIGHT_YELLOW}  ⭐ v2.0 优化技能{Colors.RESET}\n")
            
            # 显示技能列表
            skill_keys = list(SKILLS.keys())
            for i, (key, skill) in enumerate(SKILLS.items()):
                self.draw_skill_card(key, skill, i, i == self.selected_index)
            
            self.draw_status_board()
            self.draw_menu()
            
            # 处理输入
            choice = input(f"{Colors.BRIGHT_CYAN}  选择：{Colors.RESET}").strip().lower()
            
            if choice == 'q':
                print(f"\n{Colors.GREEN}  再见！👋{Colors.RESET}\n")
                break
            elif choice == 'r':
                continue
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(skill_keys):
                    key = skill_keys[idx]
                    self.show_skill_detail(key, SKILLS[key])
    
    def run(self):
        """运行"""
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print(f"\n{Colors.GREEN}  再见！👋{Colors.RESET}\n")
            sys.exit(0)


# 网页服务器版本
def run_web_server():
    """运行简单的 HTTP 服务器"""
    import http.server
    import socketserver
    
    os.chdir(Path(__file__).parent.parent)
    
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"{Colors.BRIGHT_CYAN}🦞 OpenClaw 像素办公室 Web 版{Colors.RESET}")
        print(f"\n  访问地址：{Colors.GREEN}http://localhost:{PORT}{Colors.RESET}")
        print(f"\n  按 Ctrl+C 停止服务\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n{Colors.GREEN}  服务已停止{Colors.RESET}\n")


def main():
    """主函数"""
    print(f"""
{Colors.BRIGHT_CYAN}
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║     🦞 OpenClaw 像素办公室                            ║
║                                                       ║
║     请选择运行模式：                                  ║
║                                                       ║
║     1. 终端版 (Terminal)                              ║
║     2. 网页版 (Web)                                   ║
║     3. 直接打开浏览器                                 ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
{Colors.RESET}
    """)
    
    choice = input(f"{Colors.BRIGHT_CYAN}选择 (1/2/3): {Colors.RESET}").strip()
    
    if choice == '1':
        office = PixelOffice()
        office.run()
    elif choice == '2':
        run_web_server()
    elif choice == '3':
        import webbrowser
        webbrowser.open('file://' + str(Path(__file__).parent.parent / 'index.html'))
    else:
        print(f"{Colors.RED}无效选择{Colors.RESET}")


if __name__ == "__main__":
    main()
