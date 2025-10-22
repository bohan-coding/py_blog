from flask import Blueprint, render_template, request, flash
from flask_login import current_user
from app.utils.weather_crawler import WeatherCrawler
import os

bp = Blueprint('weather', __name__, url_prefix='/weather')

@bp.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            # 默认使用网页爬虫，无需API密钥
            api_type = os.environ.get('WEATHER_API_TYPE') or 'scraper'
            api_key = os.environ.get('WEATHER_API_KEY')
            
            # 创建天气爬虫实例
            crawler = WeatherCrawler(api_key=api_key, api_type=api_type)
            
            # 获取当前天气
            weather_data = crawler.get_weather_by_city(city)
            
            # 获取天气预报
            forecast_data = crawler.get_forecast_by_city(city, 3)
        else:
            flash('请输入城市名称')
    
    return render_template('main/weather.html', 
                         weather_data=weather_data,
                         forecast_data=forecast_data)