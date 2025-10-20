import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class WeatherScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 常用城市中英文映射
        self.city_mapping = {
            '北京': '101010100',
            '上海': '101020100',
            '广州': '101280101',
            '深圳': '101280601',
            '西安': '101110101',
            '成都': '101270101',
            '武汉': '101200101',
            '杭州': '101210101',
            '南京': '101190101',
            '天津': '101030100',
            '重庆': '101040100',
            '苏州': '101190401',
            '长沙': '101250101',
            '昆明': '101290101',
            '大连': '101070201',
            '青岛': '101120201',
            '厦门': '101230201',
            '宁波': '101210401',
            '无锡': '101190201',
            '郑州': '101180101',
            '南昌': '101240101'
        }
    
    def get_weather_data(self, city):
        """
        从天气网站获取城市天气数据
        支持中文城市名和城市代码
        """
        try:
            # 判断输入的是中文城市名还是城市代码
            if city in self.city_mapping:
                # 如果是中文城市名，转换为城市代码
                city_code = self.city_mapping[city]
            else:
                # 否则直接使用输入的值作为城市代码
                city_code = city
            
            # 构造URL
            search_url = f"http://www.weather.com.cn/weather1d/{city_code}.shtml"
            
            # 发送请求
            response = self.session.get(search_url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取城市名称
                city_name_element = soup.find('div', class_='crumbs fl')
                if city_name_element:
                    # 从面包屑中提取城市名
                    city_links = city_name_element.find_all('a')
                    if len(city_links) >= 2:
                        city_name = city_links[1].text.strip()
                    else:
                        # 如果无法从面包屑获取，使用映射表或输入值
                        city_name = self._get_city_name_from_code(city_code) or city
                else:
                    city_name = self._get_city_name_from_code(city_code) or city
                
                # 提取天气信息
                weather_data = self._parse_weather_data(soup, city_name)
                return weather_data
            else:
                return self._get_default_data(city)
                
        except Exception as e:
            print(f"获取天气数据时出错: {e}")
            # 返回默认数据
            return self._get_default_data(city)
    
    def _parse_weather_data(self, soup, city_name):
        """解析天气页面数据"""
        try:
            # 提取温度
            temp_element = soup.find('p', class_='tem')
            temperature = "未知"
            if temp_element:
                temp_value = temp_element.find('span')
                if temp_value:
                    temperature = temp_value.text.strip() + "°C"
                else:
                    temp_value = temp_element.find('i')
                    if temp_value:
                        temperature = temp_value.text.strip()
            
            # 提取天气状况
            weather_element = soup.find('p', class_='wea')
            weather_status = "未知"
            if weather_element:
                weather_status = weather_element.text.strip()
            
            # 提取风力
            wind_element = soup.find('p', class_='win')
            wind = "未知"
            if wind_element:
                wind_value = wind_element.find('span')
                if wind_value and wind_value.get('title'):
                    wind = wind_value.get('title')
                elif wind_element.find('i'):
                    wind = wind_element.find('i').text.strip()
            
            # 提取湿度
            humidity = "未知"
            
            # 提取更新时间
            update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                "city": city_name,
                "temperature": temperature,
                "weather_status": weather_status,
                "wind": wind,
                "humidity": humidity,
                "update_time": update_time,
                "source": "中国天气网"
            }
        except Exception as e:
            print(f"解析天气数据时出错: {e}")
            return self._get_default_data(city_name)
    
    def _get_city_name_from_code(self, city_code):
        """根据城市代码获取城市名称"""
        # 反向查找城市代码映射
        for city_name, code in self.city_mapping.items():
            if code == city_code:
                return city_name
        return None
    
    def _get_default_data(self, city):
        """获取默认天气数据"""
        # 如果输入的是中文城市名，直接使用
        # 否则尝试从映射中查找
        city_name = city
        if city not in self.city_mapping and city in self.city_mapping.values():
            city_name = self._get_city_name_from_code(city) or city
        
        return {
            "city": city_name,
            "temperature": "未知",
            "weather_status": "未知",
            "wind": "未知",
            "humidity": "未知",
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "默认数据"
        }

class WeatherCrawler:
    """
    天气爬虫类，用于从公开API获取天气信息
    支持心知天气、和风天气API以及网页爬虫
    """
    
    def __init__(self, api_key=None, api_type="scraper"):
        self.api_type = api_type
        
        if api_type == "seniverse":
            # 心知天气API
            self.api_key = api_key or "YOUR_API_KEY_HERE"
            self.base_url = "https://api.seniverse.com/v3/weather"
        elif api_type == "qweather":
            # 和风天气API
            self.api_key = api_key or "YOUR_API_KEY_HERE"
            self.base_url = "https://devapi.qweather.com/v7/weather"
        else:
            # 默认使用网页爬虫
            self.scraper = WeatherScraper()
        
    def get_weather_by_city(self, city_name):
        """
        根据城市名获取天气信息
        
        Args:
            city_name (str): 城市名称
            
        Returns:
            dict: 包含天气信息的字典
        """
        try:
            if self.api_type == "qweather":
                return self._get_qweather_now(city_name)
            elif self.api_type == "seniverse":
                return self._get_seniverse_now(city_name)
            else:
                # 使用网页爬虫
                scraper_data = self.scraper.get_weather_data(city_name)
                return {
                    'city': scraper_data['city'],
                    'temperature': scraper_data['temperature'].replace('°C', ''),
                    'text': scraper_data['weather_status'],
                    'last_update': scraper_data['update_time'],
                    'wind': scraper_data['wind']
                }
                
        except requests.exceptions.RequestException as e:
            return {'error': f'网络请求错误: {str(e)}'}
        except json.JSONDecodeError as e:
            return {'error': f'JSON解析错误: {str(e)}'}
        except Exception as e:
            return {'error': f'未知错误: {str(e)}'}
            
    def _get_seniverse_now(self, city_name):
        """获取心知天气当前天气"""
        # 构建请求URL
        url = f"{self.base_url}/now.json"
        params = {
            'key': self.api_key,
            'location': city_name,
            'language': 'zh-Hans',
            'unit': 'c'
        }
        
        # 发送请求
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        # 解析JSON响应
        data = response.json()
        
        if 'results' in data and len(data['results']) > 0:
            weather_info = data['results'][0]
            return {
                'city': weather_info['location']['name'],
                'temperature': weather_info['now']['temperature'],
                'text': weather_info['now']['text'],
                'last_update': weather_info['last_update'],
                'code': weather_info['now']['code']
            }
        else:
            return {'error': '未找到指定城市的天气信息'}
            
    def _get_qweather_now(self, city_name):
        """获取和风天气当前天气"""
        # 首先通过城市名获取位置ID
        location_url = "https://geoapi.qweather.com/v2/city/lookup"
        location_params = {
            'key': self.api_key,
            'location': city_name
        }
        
        location_response = requests.get(location_url, params=location_params, timeout=10)
        location_response.raise_for_status()
        location_data = location_response.json()
        
        if location_data.get('code') != '200' or not location_data.get('location'):
            return {'error': '未找到指定城市的位置信息'}
            
        # 获取第一个匹配城市的ID
        city_id = location_data['location'][0]['id']
        
        # 获取天气信息
        url = f"{self.base_url}/now"
        params = {
            'key': self.api_key,
            'location': city_id
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('code') == '200' and data.get('now'):
            weather_info = data['now']
            location_info = location_data['location'][0]
            return {
                'city': location_info['name'],
                'temperature': weather_info['temp'],
                'text': weather_info['text'],
                'last_update': data['updateTime'],
                'code': weather_info['icon']
            }
        else:
            return {'error': '获取天气信息失败'}
            
    def get_forecast_by_city(self, city_name, days=3):
        """
        获取城市未来几天的天气预报
        
        Args:
            city_name (str): 城市名称
            days (int): 预报天数，默认3天
            
        Returns:
            dict: 包含天气预报信息的字典
        """
        try:
            if self.api_type == "qweather":
                return self._get_qweather_forecast(city_name, days)
            elif self.api_type == "seniverse":
                return self._get_seniverse_forecast(city_name, days)
            else:
                # 网页爬虫不支持预报功能，返回默认数据
                return {
                    'city': city_name,
                    'forecasts': [
                        {'date': '今天', 'text_day': '未知', 'low': '未知', 'high': '未知'},
                        {'date': '明天', 'text_day': '未知', 'low': '未知', 'high': '未知'},
                        {'date': '后天', 'text_day': '未知', 'low': '未知', 'high': '未知'}
                    ]
                }
                
        except requests.exceptions.RequestException as e:
            return {'error': f'网络请求错误: {str(e)}'}
        except json.JSONDecodeError as e:
            return {'error': f'JSON解析错误: {str(e)}'}
        except Exception as e:
            return {'error': f'未知错误: {str(e)}'}
            
    def _get_seniverse_forecast(self, city_name, days):
        """获取心知天气预报"""
        # 构建请求URL
        url = f"{self.base_url}/daily.json"
        params = {
            'key': self.api_key,
            'location': city_name,
            'language': 'zh-Hans',
            'unit': 'c',
            'start': 0,
            'days': min(days, 15)  # 心知天气最多支持15天预报
        }
        
        # 发送请求
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        # 解析JSON响应
        data = response.json()
        
        if 'results' in data and len(data['results']) > 0:
            forecast_info = data['results'][0]
            forecasts = []
            
            for daily in forecast_info['daily']:
                forecasts.append({
                    'date': daily['date'],
                    'high': daily['high'],
                    'low': daily['low'],
                    'text_day': daily['text_day'],
                    'text_night': daily['text_night'],
                    'code_day': daily['code_day'],
                    'code_night': daily['code_night']
                })
            
            return {
                'city': forecast_info['location']['name'],
                'forecasts': forecasts
            }
        else:
            return {'error': '未找到指定城市的天气预报信息'}
            
    def _get_qweather_forecast(self, city_name, days):
        """获取和风天气预报"""
        # 首先通过城市名获取位置ID
        location_url = "https://geoapi.qweather.com/v2/city/lookup"
        location_params = {
            'key': self.api_key,
            'location': city_name
        }
        
        location_response = requests.get(location_url, params=location_params, timeout=10)
        location_response.raise_for_status()
        location_data = location_response.json()
        
        if location_data.get('code') != '200' or not location_data.get('location'):
            return {'error': '未找到指定城市的位置信息'}
            
        # 获取第一个匹配城市的ID
        city_id = location_data['location'][0]['id']
        
        # 获取天气预报信息 (和风天气免费版最多支持7天预报)
        url = f"{self.base_url}/7d"
        params = {
            'key': self.api_key,
            'location': city_id
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('code') == '200' and data.get('daily'):
            forecasts = []
            for daily in data['daily'][:min(days, 7)]:
                forecasts.append({
                    'date': daily['fxDate'],
                    'high': daily['tempMax'],
                    'low': daily['tempMin'],
                    'text_day': daily['textDay'],
                    'text_night': daily['textNight'],
                    'code_day': daily['iconDay'],
                    'code_night': daily['iconNight']
                })
            
            location_info = location_data['location'][0]
            return {
                'city': location_info['name'],
                'forecasts': forecasts
            }
        else:
            return {'error': '获取天气预报信息失败'}