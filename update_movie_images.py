"""
更新数据库中电影的图片URL
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
        print("正在更新数据库中的电影图片...")
        scraper = NetflixScraper()
        
        # 获取所有电影
        movies = Movie.query.all()
        print(f"数据库中共有 {len(movies)} 部电影")
        
        # 更新没有真实图片URL的电影
        updated_count = 0
        for movie in movies:
            # 如果图片URL是示例URL，则更新
            if movie.image_url and ('example.com' in movie.image_url or 'placeholder.com' in movie.image_url):
                print(f"正在更新 {movie.title} 的图片URL...")
                
                # 如果有豆瓣链接，尝试从详情页获取图片
                if movie.netflix_url and 'douban.com' in movie.netflix_url:
                    image_url = scraper.get_movie_poster_from_detail_page(movie.netflix_url)
                    if image_url:
                        movie.image_url = image_url
                        updated_count += 1
                        print(f"  成功更新 {movie.title} 的图片URL")
                    else:
                        print(f"  未能获取 {movie.title} 的图片URL")
                else:
                    print(f"  {movie.title} 没有豆瓣链接，跳过")
                
                # 添加延时避免请求过快
                import time
                time.sleep(1)
        
        # 提交更改
        if updated_count > 0:
            try:
                db.session.commit()
                print(f"成功更新 {updated_count} 部电影的图片URL")
            except Exception as e:
                db.session.rollback()
                print(f"更新图片URL时出错: {e}")
        else:
            print("没有需要更新的电影图片")

if __name__ == "__main__":
    main()