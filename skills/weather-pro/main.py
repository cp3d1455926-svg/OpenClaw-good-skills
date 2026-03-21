# Weather Pro - 专业天气预报
# 主程序

import requests
import json
from datetime import datetime, timedelta

class WeatherPro:
    def __init__(self):
        self.api_key = "your_api_key"  # 可配置天气 API
        self.default_city = "北京"
        
    def get_weather(self, city):
        """获取城市天气"""
        # 模拟天气数据（实际使用时接入 API）
        weather_data = self._get_mock_weather(city)
        
        return self._format_weather(weather_data)
    
    def compare_weather(self, cities):
        """多城市天气对比"""
        city_list = cities.split()
        result = "🌍 多城市天气对比\n\n"
        
        for city in city_list:
            weather = self._get_mock_weather(city)
            result += f"{city}: {weather['condition']} {weather['temp']}°C\n"
        
        return result
    
    def get_alerts(self, city):
        """获取天气预警"""
        # 模拟预警数据
        alerts = [
            {"type": "大风", "level": "蓝色", "desc": "预计未来 24 小时内有 6-7 级大风"},
            {"type": "雾霾", "level": "黄色", "desc": "能见度低于 1000 米"}
        ]
        
        if not alerts:
            return f"✅ {city}暂无天气预警"
        
        result = f"⚠️ {city}天气预警\n\n"
        for alert in alerts:
            result += f"{alert['type']}预警 ({alert['level']}): {alert['desc']}\n"
        
        return result
    
    def get_detailed_weather(self, city):
        """获取详细天气信息"""
        weather = self._get_mock_weather(city)
        
        result = f"""🌤️ {city}详细天气

━━━ 当前数据 ━━━

🌡️ 温度：{weather['temp']}°C (体感{weather['feels_like']}°C)
☁️ 天气：{weather['condition']}
💨 风力：{weather['wind']}
💧 湿度：{weather['humidity']}%
👁️ 能见度：{weather['visibility']}km
🌫️ 气压：{weather['pressure']}hPa
🌧️ 降水概率：{weather['precip']}%

━━━ 日出日落 ━━━

🌅 日出：{weather['sunrise']}
🌇 日落：{weather['sunset']}
🌙 月出：{weather['moonrise']}
🌕 月落：{weather['moonset']}

━━━ 空气质量 ━━━

🌫️ AQI: {weather['aqi']} ({weather['aqi_level']})
PM2.5: {weather['pm25']}
PM10: {weather['pm10']}
CO: {weather['co']}mg/m³

━━━ 生活指数 ━━━

👕 穿衣：{weather['dress_index']}
🚗 出行：{weather['car_washing']}
🏃 运动：{weather['sport']}
😷 感冒：{weather['cold']}
☀️ 紫外线：{weather['uv']}
"""
        return result
    
    def get_7day_forecast(self, city):
        """7 天天气预报"""
        weather = self._get_mock_weather(city)
        
        result = f"📅 {city}7 天天气预报\n\n"
        
        forecasts = [
            {"date": "今天", "condition": "晴", "high": 22, "low": 8, "wind": "北风 2-3 级"},
            {"date": "明天", "condition": "多云", "high": 20, "low": 10, "wind": "东北风 3 级"},
            {"date": "后天", "condition": "小雨", "high": 16, "low": 8, "wind": "北风 4 级"},
            {"date": "大后天", "condition": "阴", "high": 18, "low": 9, "wind": "西北风 3 级"},
            {"date": "周四", "condition": "晴", "high": 21, "low": 10, "wind": "西风 2 级"},
            {"date": "周五", "condition": "多云", "high": 23, "low": 12, "wind": "西南风 2 级"},
            {"date": "周六", "condition": "晴", "high": 25, "low": 13, "wind": "南风 3 级"}
        ]
        
        for fc in forecasts:
            result += f"{fc['date']}: {fc['condition']} {fc['high']}°C~{fc['low']}°C {fc['wind']}\n"
        
        return result
    
    def send_daily_weather(self, city=None):
        """发送每日天气"""
        if not city:
            city = self.default_city
        
        weather = self._get_mock_weather(city)
        date = datetime.now().strftime("%Y-%m-%d")
        
        return f"""🌤️ 每日天气播报 #{date}

📍 城市：{city}
🕐 时间：{datetime.now().strftime("%H:%M")}

━━━ 今日天气 ━━━

🌡️ 温度：{weather['temp']}°C~{weather['temp_high']}°C
☁️ 天气：{weather['condition']}
💨 风力：{weather['wind']}
🌧️ 降水：{weather['precip']}%

━━━ 温馨提示 ━━━

{weather['tip']}

👕 穿衣建议：{weather['dress_index']}
🚗 出行建议：{weather['car_washing']}

祝你有美好的一天！😊
"""
    
    def _get_mock_weather(self, city):
        """获取模拟天气数据"""
        # 实际使用时替换为真实 API 调用
        return {
            "city": city,
            "temp": 18,
            "temp_high": 22,
            "temp_low": 8,
            "feels_like": 16,
            "condition": "晴转多云",
            "wind": "北风 2-3 级",
            "humidity": 45,
            "visibility": 15,
            "pressure": 1013,
            "precip": 0,
            "sunrise": "06:12",
            "sunset": "18:25",
            "moonrise": "19:30",
            "moonset": "07:15",
            "aqi": 75,
            "aqi_level": "良",
            "pm25": 35,
            "pm10": 68,
            "co": 0.8,
            "dress_index": "建议穿薄外套",
            "car_washing": "适宜",
            "sport": "适宜户外运动",
            "cold": "低发期",
            "uv": "中等",
            "tip": "今日天气较好，适宜外出活动。早晚温差较大，注意添衣。"
        }
    
    def _format_weather(self, weather):
        """格式化天气输出"""
        return f"""🌤️ {weather['city']}天气

🌡️ 温度：{weather['temp']}°C
☁️ 天气：{weather['condition']}
💨 风力：{weather['wind']}
💧 湿度：{weather['humidity']}%

最高：{weather['temp_high']}°C  最低：{weather['temp_low']}°C
"""

# 导出类
module.exports = WeatherPro
