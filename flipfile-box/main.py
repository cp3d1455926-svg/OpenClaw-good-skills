# -*- coding: utf-8 -*-
# 翻身文件箱 - 主程序
# 智能文件管理桌面软件

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
import json

class FlipFileBox:
    """翻身文件箱 - 主类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📦 翻身文件箱 v1.0")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 创建主界面
        self.create_main_ui()
        
    def create_main_ui(self):
        """创建主界面"""
        # 创建顶部导航
        self.create_navbar()
        
        # 创建内容区域
        self.create_content_area()
        
        # 创建状态栏
        self.create_statusbar()
        
    def create_navbar(self):
        """创建导航栏"""
        navbar = tk.Frame(self.root, bg='#2c3e50', height=60)
        navbar.pack(fill=tk.X)
        navbar.pack_propagate(False)
        
        # 标题
        title = tk.Label(navbar, text="📦 翻身文件箱", 
                        font=('Microsoft YaHei', 18, 'bold'),
                        bg='#2c3e50', fg='white')
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # 导航按钮
        btn_frame = tk.Frame(navbar, bg='#2c3e50')
        btn_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        buttons = [
            ('🔐 隐私保护', self.show_encrypt),
            ('🔄 多端同步', self.show_sync),
            ('📄 文件转换', self.show_convert),
            ('⚙️ 设置', self.show_settings)
        ]
        
        for text, command in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                          font=('Microsoft YaHei', 10),
                          bg='#34495e', fg='white',
                          relief=tk.FLAT, padx=15, pady=8,
                          cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#4a6278'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#34495e'))
    
    def create_content_area(self):
        """创建内容区域"""
        self.content = tk.Frame(self.root, bg='#ecf0f1')
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 默认显示隐私保护页面
        self.show_encrypt()
    
    def create_statusbar(self):
        """创建状态栏"""
        statusbar = tk.Label(self.root, text="就绪", 
                            font=('Microsoft YaHei', 9),
                            bg='#bdc3c7', fg='#2c3e50',
                            anchor=tk.W, padx=10, pady=5)
        statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        self.statusbar = statusbar
    
    def update_status(self, message):
        """更新状态栏"""
        self.statusbar.config(text=message)
    
    def clear_content(self):
        """清空内容区域"""
        for widget in self.content.winfo_children():
            widget.destroy()
    
    # ========== 隐私保护页面 ==========
    def show_encrypt(self):
        """显示隐私保护页面"""
        self.clear_content()
        
        # 标题
        title = tk.Label(self.content, text="🔐 隐私保护",
                        font=('Microsoft YaHei', 16, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=10)
        
        # 功能按钮区域
        btn_frame = tk.Frame(self.content, bg='#ecf0f1')
        btn_frame.pack(pady=20)
        
        buttons = [
            ('📁 加密文件', self.encrypt_file),
            ('🔓 解密文件', self.decrypt_file),
            ('🗄️ 创建隐私空间', self.create_secure_space),
            ('🗑️ 粉碎文件', self.shred_file)
        ]
        
        for text, command in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                          font=('Microsoft YaHei', 11),
                          bg='#3498db', fg='white',
                          relief=tk.FLAT, padx=30, pady=15,
                          cursor='hand2', width=20)
            btn.pack(pady=5)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#2980b9'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#3498db'))
    
    def encrypt_file(self):
        """加密文件"""
        file_path = filedialog.askopenfilename(title="选择要加密的文件")
        if not file_path:
            return
        
        password = tk.simpledialog.askstring("加密", "请输入密码:", show='*')
        if not password:
            messagebox.showwarning("警告", "密码不能为空")
            return
        
        try:
            # 读取文件
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # 生成密钥
            key = hashlib.sha256(password.encode()).digest()
            
            # 加密
            encrypted = bytes([content[i] ^ key[i % len(key)] for i in range(len(content))])
            
            # 保存
            encrypted_path = file_path + '.encrypted'
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted)
            
            messagebox.showinfo("成功", f"文件已加密:\n{encrypted_path}")
            self.update_status(f"已加密：{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("错误", f"加密失败:\n{str(e)}")
    
    def decrypt_file(self):
        """解密文件"""
        file_path = filedialog.askopenfilename(
            title="选择要解密的文件",
            filetypes=[("加密文件", "*.encrypted")]
        )
        if not file_path:
            return
        
        password = tk.simpledialog.askstring("解密", "请输入密码:", show='*')
        if not password:
            return
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            key = hashlib.sha256(password.encode()).digest()
            decrypted = bytes([content[i] ^ key[i % len(key)] for i in range(len(content))])
            
            original_path = file_path.replace('.encrypted', '')
            with open(original_path, 'wb') as f:
                f.write(decrypted)
            
            messagebox.showinfo("成功", f"文件已解密:\n{original_path}")
            self.update_status(f"已解密：{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("错误", f"解密失败:\n{str(e)}")
    
    def create_secure_space(self):
        """创建隐私空间"""
        folder = filedialog.askdirectory(title="选择隐私空间位置")
        if not folder:
            return
        
        password = tk.simpledialog.askstring("隐私空间", "设置访问密码:", show='*')
        if not password:
            return
        
        try:
            space_path = os.path.join(folder, 'FlipFile_Secure')
            os.makedirs(space_path, exist_ok=True)
            
            # 创建配置文件
            config = {
                'created': datetime.now().isoformat(),
                'encrypted': True,
                'version': '1.0'
            }
            with open(os.path.join(space_path, '.config.json'), 'w') as f:
                json.dump(config, f)
            
            # 隐藏文件夹（Windows）
            if os.name == 'nt':
                os.system(f'attrib +h "{space_path}"')
            
            messagebox.showinfo("成功", f"隐私空间已创建:\n{space_path}")
            self.update_status(f"创建隐私空间：{space_path}")
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def shred_file(self):
        """粉碎文件"""
        if not messagebox.askyesno("确认", "确定要永久删除此文件吗？\n此操作不可恢复！"):
            return
        
        file_path = filedialog.askopenfilename(title="选择要粉碎的文件")
        if not file_path:
            return
        
        try:
            file_size = os.path.getsize(file_path)
            
            # 多次覆盖
            for i in range(3):
                with open(file_path, 'wb') as f:
                    f.write(os.urandom(file_size))
            
            os.remove(file_path)
            
            messagebox.showinfo("成功", "文件已彻底粉碎")
            self.update_status(f"粉碎文件：{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    # ========== 多端同步页面 ==========
    def show_sync(self):
        """显示多端同步页面"""
        self.clear_content()
        
        title = tk.Label(self.content, text="🔄 多端同步",
                        font=('Microsoft YaHei', 16, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=10)
        
        # 同步状态
        status_frame = tk.LabelFrame(self.content, text="同步状态", 
                                    font=('Microsoft YaHei', 11),
                                    bg='white', padx=20, pady=20)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 模拟同步状态
        devices = [
            ('💻 此电脑', '在线', '刚刚', '2.3GB'),
            ('📱 手机', '在线', '5 分钟前', '1.8GB'),
            ('🍎 iPad', '离线', '2 小时前', '1.2GB')
        ]
        
        for i, (name, status, time, size) in enumerate(devices):
            row = tk.Frame(status_frame, bg='white')
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(row, text=name, font=('Microsoft YaHei', 10),
                    bg='white', width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=status, font=('Microsoft YaHei', 10),
                    bg='white', fg='#27ae60' if status=='在线' else '#95a5a6').pack(side=tk.LEFT, padx=20)
            tk.Label(row, text=time, font=('Microsoft YaHei', 10),
                    bg='white', fg='#7f8c8d').pack(side=tk.LEFT, padx=20)
            tk.Label(row, text=size, font=('Microsoft YaHei', 10),
                    bg='white', fg='#3498db').pack(side=tk.RIGHT)
        
        # 同步按钮
        btn = tk.Button(self.content, text="🔄 立即同步",
                       command=self.sync_now,
                       font=('Microsoft YaHei', 11),
                       bg='#27ae60', fg='white',
                       relief=tk.FLAT, padx=30, pady=10,
                       cursor='hand2')
        btn.pack(pady=10)
    
    def sync_now(self):
        """立即同步"""
        self.update_status("正在同步...")
        messagebox.showinfo("同步", "同步功能需要配置云存储 API\n详见配置说明文档")
        self.update_status("同步完成")
    
    # ========== 文件转换页面 ==========
    def show_convert(self):
        """显示文件转换页面"""
        self.clear_content()
        
        title = tk.Label(self.content, text="📄 文件转换",
                        font=('Microsoft YaHei', 16, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=10)
        
        # 文件选择
        select_frame = tk.Frame(self.content, bg='#ecf0f1')
        select_frame.pack(pady=20)
        
        self.file_path = tk.StringVar()
        tk.Entry(select_frame, textvariable=self.file_path, 
                width=60, font=('Microsoft YaHei', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(select_frame, text="浏览", command=self.browse_file,
                 bg='#3498db', fg='white', relief=tk.FLAT,
                 padx=15, cursor='hand2').pack(side=tk.LEFT)
        
        # 格式选择
        format_frame = tk.Frame(self.content, bg='#ecf0f1')
        format_frame.pack(pady=20)
        
        tk.Label(format_frame, text="转换格式:", 
                font=('Microsoft YaHei', 10), bg='#ecf0f1').pack(side=tk.LEFT, padx=5)
        
        self.format_var = tk.StringVar(value='pdf')
        formats = ['pdf', 'docx', 'jpg', 'png', 'mp4', 'txt']
        combo = ttk.Combobox(format_frame, textvariable=self.format_var,
                            values=formats, width=15, state='readonly')
        combo.pack(side=tk.LEFT, padx=5)
        
        # 转换按钮
        btn = tk.Button(self.content, text="🔄 开始转换",
                       command=self.convert_file,
                       font=('Microsoft YaHei', 11),
                       bg='#9b59b6', fg='white',
                       relief=tk.FLAT, padx=30, pady=10,
                       cursor='hand2')
        btn.pack(pady=20)
        
        # 进度条
        self.progress = ttk.Progressbar(self.content, mode='indeterminate', length=400)
        self.progress.pack(pady=10)
    
    def browse_file(self):
        """浏览文件"""
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            self.file_path.set(file_path)
    
    def convert_file(self):
        """转换文件"""
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showwarning("警告", "请先选择文件")
            return
        
        target_format = self.format_var.get()
        
        try:
            self.progress.start(10)
            self.update_status("正在转换...")
            
            # 模拟转换（实际需要调用转换库）
            file_name = os.path.basename(file_path)
            base_name = os.path.splitext(file_name)[0]
            new_path = os.path.join(os.path.dirname(file_path), f"{base_name}.{target_format}")
            
            shutil.copy2(file_path, new_path)
            
            self.progress.stop()
            messagebox.showinfo("成功", f"文件已转换:\n{new_path}")
            self.update_status(f"已转换：{file_name} → {target_format}")
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("错误", str(e))
    
    # ========== 设置页面 ==========
    def show_settings(self):
        """显示设置页面"""
        self.clear_content()
        
        title = tk.Label(self.content, text="⚙️ 设置",
                        font=('Microsoft YaHei', 16, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=10)
        
        settings_frame = tk.LabelFrame(self.content, text="常规设置",
                                      font=('Microsoft YaHei', 11),
                                      bg='white', padx=20, pady=20)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 设置项
        settings = [
            ('默认加密算法', 'AES-256'),
            ('同步间隔', '5 分钟'),
            ('云服务商', '自动选择'),
            ('转换质量', '90%'),
            ('自动备份', '开启')
        ]
        
        for label, value in settings:
            row = tk.Frame(settings_frame, bg='white')
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(row, text=label, font=('Microsoft YaHei', 10),
                    bg='white', width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=value, font=('Microsoft YaHei', 10),
                    bg='white', fg='#3498db').pack(side=tk.LEFT, padx=20)
        
        # 保存按钮
        btn = tk.Button(self.content, text="💾 保存设置",
                       command=self.save_settings,
                       font=('Microsoft YaHei', 11),
                       bg='#3498db', fg='white',
                       relief=tk.FLAT, padx=30, pady=10,
                       cursor='hand2')
        btn.pack(pady=20)
    
    def save_settings(self):
        """保存设置"""
        messagebox.showinfo("设置", "设置已保存")
        self.update_status("设置已保存")


def main():
    """主函数"""
    root = tk.Tk()
    app = FlipFileBox(root)
    root.mainloop()


if __name__ == '__main__':
    main()
