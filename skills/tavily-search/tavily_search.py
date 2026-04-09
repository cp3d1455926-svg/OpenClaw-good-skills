# -*- coding: utf-8 -*-
# Tavily Search - 主程序
# 使用 Tavily API 进行智能搜索

import requests
import sys
import json
import os
from typing import List, Dict

class TavilySearch:
    def __init__(self):
        # 优先从环境变量读取，其次从 skill.json 读取
        self.api_key = os.getenv('TAVILY_API_KEY', '')
        if not self.api_key:
            try:
                with open(os.path.join(os.path.dirname(__file__), 'skill.json'), 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.api_key = config.get('config', {}).get('apiKey', '')
            except:
                pass
        self.base_url = 'https://api.tavily.com/search'
        
    def search(self, query: str, search_depth: str = 'basic', 
               max_results: int = 10, include_images: bool = False) -> Dict:
        """
        Tavily 智能搜索
        
        Args:
            query: 搜索关键词
            search_depth: basic 或 advanced
            max_results: 最大结果数
            include_images: 是否包含图片
            
        Returns:
            搜索结果字典
        """
        if not self.api_key:
            return {
                'error': '缺少 TAVILY_API_KEY 环境变量',
                'message': '请配置 Tavily API 密钥'
            }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        payload = {
            'query': query,
            'search_depth': search_depth,
            'max_results': max_results,
            'include_images': include_images,
            'include_answer': True,
            'include_raw_content': False
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                'error': '搜索失败',
                'message': str(e)
            }
    
    def format_results(self, results: Dict) -> str:
        """格式化搜索结果"""
        if 'error' in results:
            return f"❌ {results['error']}: {results['message']}"
        
        output = "🔍 搜索结果\n\n"
        
        # AI 生成的答案
        if 'answer' in results:
            output += f"💡 AI 摘要:\n{results['answer']}\n\n"
            output += "━" * 50 + "\n\n"
        
        # 搜索结果
        if 'results' in results:
            for i, result in enumerate(results['results'], 1):
                output += f"{i}. **{result.get('title', '无标题')}**\n"
                output += f"   🔗 {result.get('url', '')}\n"
                output += f"   📝 {result.get('content', '')[:200]}...\n"
                
                if result.get('score'):
                    output += f"   ⭐ 相关度：{result['score']:.2f}\n"
                
                output += "\n"
        
        # 图片
        if 'images' in results and results['images']:
            output += "\n🖼️ 相关图片:\n"
            for img in results['images'][:5]:
                output += f"• {img}\n"
        
        return output
    
    def news_search(self, query: str, days: int = 7) -> Dict:
        """新闻搜索"""
        return self.search(
            query=f"{query} 新闻",
            search_depth='advanced',
            max_results=10
        )
    
    def deep_search(self, query: str) -> Dict:
        """深度搜索"""
        return self.search(
            query=query,
            search_depth='advanced',
            max_results=15,
            include_images=True
        )


# 命令行使用示例
if __name__ == '__main__':
    import sys
    
    # 设置控制台输出为 UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    
    search = TavilySearch()
    
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        results = search.search(query)
        print(search.format_results(results))
    else:
        print("用法：python tavily_search.py <搜索关键词>")
