"""
天气功能相关的工具函数测试
"""
import sys
import os
import unittest

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.utils.weather_crawler import WeatherScraper, WeatherCrawler


class TestWeatherUtils(unittest.TestCase):
    
    def setUp(self):
        """测试前的准备工作"""
        self.scraper = WeatherScraper()
        self.crawler = WeatherCrawler()
    
    def test_city_mapping(self):
        """测试城市映射"""
        # 测试北京的映射
        self.assertEqual(self.scraper.city_mapping['北京'], '101010100')
        # 测试上海的映射
        self.assertEqual(self.scraper.city_mapping['上海'], '101020100')
    
    def test_get_city_name_from_code(self):
        """测试通过城市代码获取城市名称"""
        city_name = self.scraper._get_city_name_from_code('101010100')
        self.assertEqual(city_name, '北京')
        
        # 测试不存在的城市代码
        city_name = self.scraper._get_city_name_from_code('999999999')
        self.assertIsNone(city_name)
    
    def test_get_default_data(self):
        """测试默认数据生成"""
        default_data = self.scraper._get_default_data('测试城市')
        self.assertIn('city', default_data)
        self.assertIn('temperature', default_data)
        self.assertIn('weather_status', default_data)
        self.assertEqual(default_data['city'], '测试城市')
    
    def test_weather_crawler_initialization(self):
        """测试天气爬虫初始化"""
        # 测试默认初始化（网页爬虫）
        crawler = WeatherCrawler()
        self.assertEqual(crawler.api_type, 'scraper')
        
        # 测试API初始化
        crawler = WeatherCrawler(api_key='test_key', api_type='seniverse')
        self.assertEqual(crawler.api_type, 'seniverse')
        self.assertEqual(crawler.api_key, 'test_key')


if __name__ == '__main__':
    unittest.main()