"""
重置并更新电影数据
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Movie
from app.utils.netflix_scraper import init_movie_data

def reset_movies():
    """删除所有现有电影数据"""
    app = create_app()
    
    with app.app_context():
        # 删除所有电影数据
        count = Movie.query.delete()
        db.session.commit()
        print(f"已删除 {count} 部电影")
        
        return True

def main():
    print("开始重置并更新电影数据...")
    
    # 删除现有电影数据
    if reset_movies():
        # 重新爬取电影数据
        print("正在重新爬取电影数据...")
        success = init_movie_data(20)
        
        if success:
            print("电影数据更新成功")
        else:
            print("电影数据更新失败")
    
    print("电影数据重置和更新完成")

if __name__ == "__main__":
    main()