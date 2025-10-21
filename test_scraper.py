"""
测试豆瓣电影爬虫脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.utils.netflix_scraper import NetflixScraper

def main():
    app = create_app()
    
    with app.app_context():
        print("测试豆瓣电影爬虫...")
        scraper = NetflixScraper()
        
        # 测试爬取豆瓣Top250的前5部电影
        print("正在测试爬取豆瓣Top250前5部电影...")
        movies = scraper.scrape_douban_top_movies(5)
        print(f"成功爬取到 {len(movies)} 部电影")
        
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie['title']} ({movie['year']}) - 评分: {movie['rating']}")
            print(f"   类型: {movie['genre']}")
            print(f"   图片URL: {movie['image_url']}")
            print(f"   简介: {movie['description'][:50]}...")
            print()

if __name__ == "__main__":
    main()