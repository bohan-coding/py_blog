"""
清理数据库中的占位符图片URL并重新爬取真实数据
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Movie
from app.utils.netflix_scraper import NetflixScraper

def clean_placeholder_images():
    """清理数据库中的占位符图片URL"""
    app = create_app()
    
    with app.app_context():
        # 获取所有电影
        movies = Movie.query.all()
        print(f"数据库中共有 {len(movies)} 部电影")
        
        # 清理占位符图片URL
        cleaned_count = 0
        for movie in movies:
            # 如果图片URL是示例URL或占位符，则清空
            if movie.image_url and ('example.com' in movie.image_url or 'placeholder.com' in movie.image_url):
                print(f"清理 {movie.title} 的占位符图片URL")
                movie.image_url = ''
                cleaned_count += 1
        
        # 提交更改
        if cleaned_count > 0:
            try:
                db.session.commit()
                print(f"成功清理 {cleaned_count} 部电影的占位符图片URL")
            except Exception as e:
                db.session.rollback()
                print(f"清理占位符图片URL时出错: {e}")
                return False
        else:
            print("没有需要清理的占位符图片URL")
        
        return True

def update_movie_images():
    """更新电影图片"""
    app = create_app()
    
    with app.app_context():
        print("正在更新电影图片...")
        scraper = NetflixScraper()
        
        # 获取所有没有图片URL的电影
        movies = Movie.query.filter_by(image_url='').all()
        print(f"需要更新图片的电影数量: {len(movies)}")
        
        # 更新没有图片URL的电影
        updated_count = 0
        for movie in movies:
            if movie.netflix_url and 'douban.com' in movie.netflix_url:
                print(f"正在更新 {movie.title} 的图片URL...")
                image_url = scraper.get_movie_poster_from_detail_page(movie.netflix_url)
                if image_url:
                    movie.image_url = image_url
                    updated_count += 1
                    print(f"  成功更新 {movie.title} 的图片URL")
                else:
                    print(f"  未能获取 {movie.title} 的图片URL")
                
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
                return False
        else:
            print("没有需要更新的电影图片")
        
        return True

def main():
    print("开始清理和更新电影图片数据...")
    
    # 清理占位符图片URL
    if clean_placeholder_images():
        # 更新电影图片
        update_movie_images()
    
    print("电影图片数据清理和更新完成")

if __name__ == "__main__":
    main()