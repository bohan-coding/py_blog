"""
初始化电影数据脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.utils.netflix_scraper import NetflixScraper

def main():
    app = create_app()
    
    with app.app_context():
        # 创建所有表（如果不存在）
        db.create_all()
        
        # 初始化电影数据
        print("正在初始化电影数据...")
        scraper = NetflixScraper()
        success = scraper.update_movie_database(20)
        
        if success:
            print("电影数据初始化成功！")
        else:
            print("电影数据初始化失败！")

if __name__ == "__main__":
    main()