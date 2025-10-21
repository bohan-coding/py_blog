"""
检查数据库中的电影图片URL
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Movie

def main():
    app = create_app()
    
    with app.app_context():
        # 获取所有电影
        movies = Movie.query.all()
        print(f"数据库中共有 {len(movies)} 部电影")
        
        # 显示每部电影的图片URL
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie.title}")
            print(f"   图片URL: {movie.image_url}")
            print(f"   详情页: {movie.netflix_url}")
            print()

if __name__ == "__main__":
    main()