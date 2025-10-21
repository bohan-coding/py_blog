"""
测试爬虫并保存数据
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Movie
from app.utils.netflix_scraper import NetflixScraper

def main():
    app = create_app()
    
    with app.app_context():
        print("正在测试爬虫并保存数据...")
        scraper = NetflixScraper()
        
        # 爬取少量电影数据进行测试
        movies = scraper.scrape_douban_top_movies(5)
        print(f"成功爬取到 {len(movies)} 部电影")
        
        # 保存到数据库
        added_count = 0
        for movie_data in movies:
            # 检查电影是否已存在
            existing_movie = Movie.query.filter_by(title=movie_data['title']).first()
            if not existing_movie:
                movie = Movie(
                    title=movie_data['title'],
                    description=movie_data['description'],
                    year=movie_data['year'],
                    rating=movie_data['rating'],
                    image_url=movie_data['image_url'],
                    netflix_url=movie_data['netflix_url'],
                    category=movie_data['category'],
                    genre=movie_data['genre']
                )
                db.session.add(movie)
                added_count += 1
                print(f"添加电影: {movie.title}")
                print(f"  图片URL: {movie.image_url}")
        
        try:
            db.session.commit()
            print(f"成功添加 {added_count} 部新电影")
        except Exception as e:
            db.session.rollback()
            print(f"保存电影数据时出错: {e}")

if __name__ == "__main__":
    main()