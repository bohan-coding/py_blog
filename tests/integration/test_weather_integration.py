"""
天气功能集成测试
"""
import sys
import os
import unittest
import requests

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class TestWeatherIntegration(unittest.TestCase):
    
    def setUp(self):
        """测试前的准备工作"""
        self.base_url = 'http://127.0.0.1:5000'
    
    def test_weather_page_access(self):
        """测试天气页面访问"""
        try:
            response = requests.get(f'{self.base_url}/weather')
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.ConnectionError:
            # 如果服务未启动，跳过此测试
            self.skipTest("Flask服务未启动")
    
    def test_weather_form_exists(self):
        """测试天气表单存在"""
        try:
            response = requests.get(f'{self.base_url}/weather')
            self.assertIn('<form', response.text)
            self.assertIn('name="city"', response.text)
        except requests.exceptions.ConnectionError:
            self.skipTest("Flask服务未启动")
    
    def test_weather_search(self):
        """测试天气搜索功能"""
        try:
            # 先获取页面以获得CSRF令牌
            session = requests.Session()
            response = session.get(f'{self.base_url}/weather')
            
            # 检查是否有CSRF令牌
            self.assertIn('csrf_token', response.text)
            
        except requests.exceptions.ConnectionError:
            self.skipTest("Flask服务未启动")


if __name__ == '__main__':
    unittest.main()