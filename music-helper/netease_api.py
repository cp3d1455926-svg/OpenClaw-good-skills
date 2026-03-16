#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 Music Helper - 网易云音乐 API 对接
功能：搜索歌曲、获取歌词、推荐歌单
"""

import requests
import json
from pathlib import Path

# 网易云音乐 API（使用第三方开源 API）
# 参考：https://github.com/Binaryify/NeteaseCloudMusicApi
NETEASE_BASE_URL = "http://music.163.com/api"
NETEASE_SEARCH_URL = "https://music.163.com/api/search/get"
NETEASE_LYRIC_URL = "https://music.163.com/api/song/lyric"


def search_song_netease(keyword, limit=10):
    """
    搜索网易云音乐
    返回歌曲列表
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://music.163.com/"
        }
        
        params = {
            "s": keyword,
            "type": 1,  # 1=单曲，10=专辑，100=歌手
            "limit": limit,
            "offset": 0
        }
        
        response = requests.get(NETEASE_SEARCH_URL, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200 and data.get("result"):
                return data["result"].get("songs", [])
        
        return []
    
    except Exception as e:
        print(f"搜索失败：{e}")
        return []


def get_lyric_netease(song_id):
    """
    获取歌词
    song_id: 网易云音乐歌曲 ID
    """
    try:
        params = {
            "id": song_id,
            "lv": 1,
            "tv": -1
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://music.163.com/"
        }
        
        response = requests.get(NETEASE_LYRIC_URL, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200 and data.get("lrc"):
                lyric = data["lrc"].get("lyric", "")
                # 清理歌词（去除时间戳）
                return clean_lyric(lyric)
        
        return "暂无歌词"
    
    except Exception as e:
        print(f"获取歌词失败：{e}")
        return "暂无歌词"


def clean_lyric(lyric_text):
    """
    清理歌词，去除时间戳
    """
    import re
    
    # 去除时间戳 [00:00.00]
    cleaned = re.sub(r'\[\d{2}:\d{2}\.\d+\]', '', lyric_text)
    # 去除空行
    lines = [line.strip() for line in cleaned.split('\n') if line.strip()]
    
    # 返回前 8 行（避免太长）
    return '\n'.join(lines[:8])


def get_song_detail(song_id):
    """
    获取歌曲详情
    """
    try:
        url = f"{NETEASE_BASE_URL}/song/detail"
        params = {
            "ids": f"[{song_id}]"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://music.163.com/"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200 and data.get("songs"):
                song = data["songs"][0]
                return {
                    "id": song["id"],
                    "name": song["name"],
                    "artists": ", ".join([a["name"] for a in song.get("artists", [])]),
                    "album": song.get("album", {}).get("name", ""),
                    "duration": song.get("duration", 0) // 1000,  # 秒
                }
        
        return None
    
    except Exception as e:
        print(f"获取详情失败：{e}")
        return None


def get_playlist_recommend(limit=10):
    """
    获取推荐歌单
    """
    try:
        url = f"{NETEASE_BASE_URL}/personalized"
        params = {
            "limit": limit
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://music.163.com/"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                return data.get("result", [])
        
        return []
    
    except Exception as e:
        print(f"获取推荐失败：{e}")
        return []


def format_song_info(song):
    """格式化歌曲信息"""
    info = f"🎵 《{song.get('name', '未知')}》"
    
    if song.get('artists'):
        info += f" - {song['artists']}"
    
    if song.get('album'):
        info += f"\n📀 专辑：{song['album']}"
    
    if song.get('duration'):
        minutes = song['duration'] // 60
        seconds = song['duration'] % 60
        info += f"\n⏱️ 时长：{minutes}:{seconds:02d}"
    
    return info


# 测试
if __name__ == "__main__":
    print("测试网易云 API 对接...")
    
    # 测试搜索
    result = search_song_netease("晴天", limit=5)
    print(f"搜索结果：{len(result)} 条")
    
    if result:
        song = result[0]
        print(format_song_info({
            "name": song.get("name"),
            "artists": ", ".join([a["name"] for a in song.get("artists", [])]),
            "album": song.get("album", {}).get("name", ""),
            "duration": song.get("duration", 0) // 1000
        }))
        
        # 测试歌词
        lyric = get_lyric_netease(song["id"])
        print(f"\n📝 歌词：\n{lyric}")
