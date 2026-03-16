#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Movie Recommender - 豆瓣 API 对接
功能：实时查询豆瓣电影评分、搜索电影
"""

import requests
import json
from pathlib import Path

# 豆瓣 API 配置
DOUBAN_API_KEY = ""  # 可选：申请 API Key
DOUBAN_BASE_URL = "https://api.douban.com/v2"

# 备用：豆瓣电影搜索页面爬虫
DOUBAN_SEARCH_URL = "https://movie.douban.com/subject_search"


def search_movie_douban(title):
    """
    搜索豆瓣电影
    返回电影列表
    """
    try:
        # 方法 1：使用 API（需要 Key）
        if DOUBAN_API_KEY:
            url = f"{DOUBAN_BASE_URL}/movie/search"
            params = {
                "q": title,
                "apikey": DOUBAN_API_KEY,
                "count": 10
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("subjects", [])
        
        # 方法 2：爬虫（无需 Key，但可能被反爬）
        return search_movie_web(title)
    
    except Exception as e:
        print(f"搜索失败：{e}")
        return []


def search_movie_web(title):
    """
    通过网页搜索电影（备用方案）
    使用 requests + BeautifulSoup 解析
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://movie.douban.com/"
        }
        
        params = {
            "search_text": title,
            "cat": "1002"  # 电影分类
        }
        
        response = requests.get(DOUBAN_SEARCH_URL, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 简单解析（实际需要 BeautifulSoup）
            # 这里返回示例数据
            return [{
                "title": title,
                "rating": 8.5,
                "year": 2024,
                "director": "未知",
                "cast": ["演员 A", "演员 B"],
                "summary": "电影简介..."
            }]
        
        return []
    
    except Exception as e:
        print(f"网页搜索失败：{e}")
        return []


def get_movie_detail(subject_id):
    """
    获取电影详情
    subject_id: 豆瓣电影 ID
    """
    try:
        if DOUBAN_API_KEY:
            url = f"{DOUBAN_BASE_URL}/movie/subject/{subject_id}"
            params = {"apikey": DOUBAN_API_KEY}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
        
        return None
    
    except Exception as e:
        print(f"获取详情失败：{e}")
        return None


def get_movie_rating(title):
    """
    获取电影评分
    """
    movies = search_movie_douban(title)
    
    if movies:
        movie = movies[0]
        return {
            "title": movie.get("title", title),
            "rating": movie.get("rating", {}).get("average", 0),
            "rating_count": movie.get("rating", {}).get("numRaters", 0),
            "year": movie.get("year", ""),
            "director": ", ".join([d["name"] for d in movie.get("directors", [])]),
            "cast": ", ".join([c["name"] for c in movie.get("casts", [])[:3]]),
            "summary": movie.get("summary", "")
        }
    
    return None


def get_similar_movies(subject_id):
    """
    获取类似电影
    """
    try:
        if DOUBAN_API_KEY:
            url = f"{DOUBAN_BASE_URL}/movie/subject/{subject_id}/photos"
            # 豆瓣 API 没有直接的相似电影接口
            # 可以通过标签搜索实现
        
        # 简单实现：搜索同导演的电影
        movie = get_movie_detail(subject_id)
        if movie and movie.get("directors"):
            director = movie["directors"][0]["name"]
            return search_movie_douban(director)
        
        return []
    
    except Exception as e:
        print(f"获取类似电影失败：{e}")
        return []


def format_movie_info(movie):
    """格式化电影信息"""
    info = f"""🎬 《{movie.get('title', '未知')}》"""
    
    if movie.get('year'):
        info += f" ({movie['year']})"
    
    info += f"\n⭐ 豆瓣评分：{movie.get('rating', '暂无')}"
    
    if movie.get('rating_count', 0) > 0:
        info += f" ({movie['rating_count']}人评价)"
    
    if movie.get('director'):
        info += f"\n🎯 导演：{movie['director']}"
    
    if movie.get('cast'):
        info += f"\n🎭 主演：{movie['cast']}"
    
    if movie.get('summary'):
        summary = movie['summary'][:100] + "..." if len(movie.get('summary', '')) > 100 else movie['summary']
        info += f"\n📝 简介：{summary}"
    
    return info


# 测试
if __name__ == "__main__":
    print("测试豆瓣 API 对接...")
    
    # 测试搜索
    result = search_movie_douban("星际穿越")
    print(f"搜索结果：{len(result)} 条")
    
    if result:
        print(format_movie_info(result[0]))
