#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💰 Price Tracker - 电商价格爬虫
功能：京东/淘宝/拼多多价格抓取
"""

import requests
import re
import json
from pathlib import Path

# 电商平台 URL 模板
JD_PRODUCT_URL = "https://item.jd.com/{}.html"
TB_PRODUCT_URL = "https://item.taobao.com/item.htm?id={}"
PDD_PRODUCT_URL = "https://mobile.yangkeduo.com/goods.html?goods_id={}"

# 价格查询 API（第三方）
# 注意：实际使用需要找稳定的价格 API
PRICE_API_URL = "https://api.example.com/price"  # 示例


def get_jd_price(product_id):
    """
    获取京东商品价格
    使用京东价格查询接口
    """
    try:
        # 京东价格接口
        price_url = f"https://p.3.cn/prices/mgets?skuIds=J_{product_id}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://item.jd.com/"
        }
        
        response = requests.get(price_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                price = data[0].get("p", "")
                if price:
                    return {
                        "platform": "jd",
                        "product_id": product_id,
                        "price": float(price),
                        "original_price": float(data[0].get("m", price)),
                        "currency": "CNY"
                    }
        
        return None
    
    except Exception as e:
        print(f"获取京东价格失败：{e}")
        return None


def get_tb_price(product_id):
    """
    获取淘宝商品价格
    需要解析页面（简单实现）
    """
    try:
        url = f"https://item.taobao.com/item.htm?id={product_id}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 简单正则提取价格（实际需要更复杂的解析）
            price_match = re.search(r'"price":"(\d+\.?\d*)"', response.text)
            if price_match:
                return {
                    "platform": "tb",
                    "product_id": product_id,
                    "price": float(price_match.group(1)),
                    "currency": "CNY"
                }
        
        return None
    
    except Exception as e:
        print(f"获取淘宝价格失败：{e}")
        return None


def get_pdd_price(product_id):
    """
    获取拼多多商品价格
    拼多多反爬较严，建议用第三方 API
    """
    try:
        # 拼多多价格较难直接获取，返回示例数据
        # 实际可用：慢慢买 API、什么值得买 API 等
        return {
            "platform": "pdd",
            "product_id": product_id,
            "price": 0,  # 需要第三方 API
            "note": "拼多多价格需要第三方 API"
        }
    
    except Exception as e:
        print(f"获取拼多多价格失败：{e}")
        return None


def parse_product_url(url):
    """
    解析商品 URL，提取平台和产品 ID
    """
    # 京东
    jd_match = re.search(r'jd\.com/(\d+)\.html', url)
    if jd_match:
        return {"platform": "jd", "product_id": jd_match.group(1)}
    
    # 淘宝
    tb_match = re.search(r'taobao\.com.*?id=(\d+)', url)
    if tb_match:
        return {"platform": "tb", "product_id": tb_match.group(1)}
    
    # 天猫
    tmall_match = re.search(r'tmall\.com.*?id=(\d+)', url)
    if tmall_match:
        return {"platform": "tmall", "product_id": tmall_match.group(1)}
    
    # 拼多多
    pdd_match = re.search(r'yangkeduo\.com.*?goods_id=(\d+)', url)
    if pdd_match:
        return {"platform": "pdd", "product_id": pdd_match.group(1)}
    
    return None


def get_price(url):
    """
    获取商品价格（自动识别平台）
    """
    parsed = parse_product_url(url)
    
    if not parsed:
        return {"error": "无法识别商品链接"}
    
    platform = parsed["platform"]
    product_id = parsed["product_id"]
    
    if platform == "jd":
        return get_jd_price(product_id)
    elif platform in ["tb", "tmall"]:
        return get_tb_price(product_id)
    elif platform == "pdd":
        return get_pdd_price(product_id)
    else:
        return {"error": f"不支持的平台：{platform}"}


def compare_prices_across_platforms(product_name):
    """
    跨平台比价
    需要已知各平台的产品 ID
    """
    results = []
    
    # 示例：假设已知各平台 ID
    # 实际需要通过搜索 API 获取
    platforms = {
        "jd": "100012345",
        "tb": "628394756",
        "pdd": "394857261"
    }
    
    for platform, product_id in platforms.items():
        if platform == "jd":
            price_info = get_jd_price(product_id)
        elif platform == "tb":
            price_info = get_tb_price(product_id)
        elif platform == "pdd":
            price_info = get_pdd_price(product_id)
        else:
            continue
        
        if price_info and "error" not in price_info:
            results.append(price_info)
    
    # 按价格排序
    results.sort(key=lambda x: x.get("price", float('inf')))
    
    return results


# 测试
if __name__ == "__main__":
    print("测试价格爬虫...")
    
    # 测试京东价格
    jd_result = get_jd_price("100012345")
    print(f"京东价格：{jd_result}")
    
    # 测试 URL 解析
    url = "https://item.jd.com/100012345.html"
    parsed = parse_product_url(url)
    print(f"解析结果：{parsed}")
