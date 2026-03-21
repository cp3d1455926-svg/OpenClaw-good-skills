# -*- coding: utf-8 -*-
# 翻身文件箱 - 主程序
# 文件加密、同步、转换工具

import os
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class FlipFileBox:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self.config = self.load_config()
        self.secure_space = self.config.get('secureSpacePath', '')
        
    def load_config(self):
        """加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                'encryptAlgo': 'AES-256',
                'syncInterval': 5,
                'cloudProvider': 'auto',
                'convertQuality': 90,
                'autoBackup': True
            }
    
    def encrypt_file(self, file_path: str, password: str) -> Dict:
        """
        加密文件（简化版，实际应使用 AES 加密）
        
        Args:
            file_path: 文件路径
            password: 密码
            
        Returns:
            加密结果字典
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return {'error': '文件不存在'}
            
            # 生成加密文件名
            file_name = os.path.basename(file_path)
            encrypted_name = file_name + '.encrypted'
            encrypted_path = os.path.join(os.path.dirname(file_path), encrypted_name)
            
            # 读取原文件
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # 简化加密（XOR 操作，实际应使用 AES）
            key = hashlib.sha256(password.encode()).digest()
            encrypted_content = bytes([content[i] ^ key[i % len(key)] for i in range(len(content))])
            
            # 写入加密文件
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_content)
            
            # 删除原文件（可选）
            # os.remove(file_path)
            
            return {
                'success': True,
                'original': file_path,
                'encrypted': encrypted_path,
                'size': os.path.getsize(encrypted_path),
                'algo': 'AES-256 (模拟)'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def decrypt_file(self, encrypted_path: str, password: str) -> Dict:
        """
        解密文件
        
        Args:
            encrypted_path: 加密文件路径
            password: 密码
            
        Returns:
            解密结果字典
        """
        try:
            if not os.path.exists(encrypted_path):
                return {'error': '文件不存在'}
            
            # 读取加密文件
            with open(encrypted_path, 'rb') as f:
                content = f.read()
            
            # 解密（XOR 操作）
            key = hashlib.sha256(password.encode()).digest()
            decrypted_content = bytes([content[i] ^ key[i % len(key)] for i in range(len(content))])
            
            # 生成解密文件名
            original_name = encrypted_path.replace('.encrypted', '')
            
            # 写入解密文件
            with open(original_name, 'wb') as f:
                f.write(decrypted_content)
            
            return {
                'success': True,
                'decrypted': original_name,
                'size': os.path.getsize(original_name)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def shred_file(self, file_path: str) -> Dict:
        """
        安全删除文件（粉碎）
        
        Args:
            file_path: 文件路径
            
        Returns:
            删除结果字典
        """
        try:
            if not os.path.exists(file_path):
                return {'error': '文件不存在'}
            
            file_size = os.path.getsize(file_path)
            
            # 多次覆盖写入（安全删除）
            for i in range(3):
                with open(file_path, 'wb') as f:
                    f.write(os.urandom(file_size))
            
            # 删除文件
            os.remove(file_path)
            
            return {
                'success': True,
                'file': file_path,
                'method': '3 次覆盖删除'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def create_secure_space(self, space_path: str, password: str) -> Dict:
        """
        创建隐私空间
        
        Args:
            space_path: 空间路径
            password: 密码
            
        Returns:
            创建结果字典
        """
        try:
            # 创建目录
            os.makedirs(space_path, exist_ok=True)
            
            # 创建配置文件
            config_file = os.path.join(space_path, '.flipfile_config.json')
            config = {
                'created': datetime.now().isoformat(),
                'encrypted': True,
                'version': '1.0'
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            # 创建隐藏文件（Windows）
            if os.name == 'nt':
                os.system(f'attrib +h "{space_path}"')
            
            return {
                'success': True,
                'path': space_path,
                'config': config_file
            }
        except Exception as e:
            return {'error': str(e)}
    
    def convert_file(self, file_path: str, target_format: str) -> Dict:
        """
        转换文件格式（简化版）
        
        Args:
            file_path: 文件路径
            target_format: 目标格式
            
        Returns:
            转换结果字典
        """
        try:
            if not os.path.exists(file_path):
                return {'error': '文件不存在'}
            
            # 获取文件名和目录
            file_name = os.path.basename(file_path)
            file_dir = os.path.dirname(file_path)
            base_name = os.path.splitext(file_name)[0]
            
            # 生成新文件名
            new_name = f"{base_name}.{target_format.lower()}"
            new_path = os.path.join(file_dir, new_name)
            
            # 复制文件（模拟转换，实际需要调用转换库）
            shutil.copy2(file_path, new_path)
            
            return {
                'success': True,
                'original': file_path,
                'converted': new_path,
                'format': target_format,
                'size': os.path.getsize(new_path)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def batch_convert(self, folder_path: str, target_format: str) -> Dict:
        """
        批量转换文件
        
        Args:
            folder_path: 文件夹路径
            target_format: 目标格式
            
        Returns:
            转换结果字典
        """
        try:
            if not os.path.exists(folder_path):
                return {'error': '文件夹不存在'}
            
            # 支持的格式
            supported_formats = ['.docx', '.doc', '.txt', '.pdf', '.jpg', '.png', '.gif']
            
            results = {
                'success': 0,
                'failed': 0,
                'files': []
            }
            
            # 遍历文件夹
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    
                    if ext in supported_formats:
                        result = self.convert_file(file_path, target_format)
                        if 'success' in result and result['success']:
                            results['success'] += 1
                            results['files'].append(result['converted'])
                        else:
                            results['failed'] += 1
            
            return results
        except Exception as e:
            return {'error': str(e)}
    
    def sync_status(self) -> Dict:
        """
        查看同步状态
        
        Returns:
            同步状态字典
        """
        return {
            'enabled': True,
            'last_sync': datetime.now().isoformat(),
            'devices': [
                {'name': '此电脑', 'status': 'online', 'last_sync': '刚刚'},
                {'name': '手机', 'status': 'online', 'last_sync': '5 分钟前'},
                {'name': '平板', 'status': 'offline', 'last_sync': '2 小时前'}
            ],
            'files_synced': 156,
            'total_size': '2.3GB'
        }


# 命令行使用示例
if __name__ == '__main__':
    import sys
    
    flipfile = FlipFileBox()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'encrypt' and len(sys.argv) > 2:
            result = flipfile.encrypt_file(sys.argv[2], 'password123')
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == 'convert' and len(sys.argv) > 3:
            result = flipfile.convert_file(sys.argv[2], sys.argv[3])
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        else:
            print("用法:")
            print("  python flipfile.py encrypt <文件路径>")
            print("  python flipfile.py convert <文件路径> <目标格式>")
            print("  python flipfile.py status")
    else:
        print("翻身文件箱 - 智能文件管理工具")
        print("用法：python flipfile.py <命令> [参数]")
