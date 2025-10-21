import requests
from bs4 import BeautifulSoup
import json
import time
import random
from app.models import Movie
from app import db
import re
from urllib.parse import urljoin

class NetflixScraper:
    """
    电影数据爬虫（主要从豆瓣电影获取数据）
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_douban_top_movies(self, limit=20):
        """
        从豆瓣电影Top250爬取高分电影数据，包括真实图片链接
        """
        try:
            movies = []
            start = 0
            per_page = 25
            
            while len(movies) < limit:
                # 豆瓣电影Top250分页URL
                url = f"https://movie.douban.com/top250?start={start}&filter="
                print(f"正在爬取豆瓣电影Top250第{start//per_page + 1}页...")
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 查找电影列表项
                movie_items = soup.select('ol.grid_view li')
                
                if not movie_items:
                    print("未找到电影列表项，可能已到达最后一页")
                    break
                
                for item in movie_items:
                    try:
                        # 获取电影标题
                        title_element = item.select_one('.hd a span')
                        if not title_element:
                            continue
                            
                        title = title_element.text.strip()
                        
                        # 获取图片链接
                        img_element = item.select_one('.pic img')
                        image_url = ''
                        if img_element and img_element.get('src'):
                            image_url = img_element['src']
                            # 转换为较大尺寸的图片
                            image_url = image_url.replace('/s_ratio_poster/', '/l_ratio_poster/')
                            image_url = image_url.replace('/m_ratio_poster/', '/l_ratio_poster/')
                        
                        # 获取其他信息
                        info_text = item.select_one('.bd p').text.strip()
                        
                        # 提取年份
                        year_match = re.search(r'(\d{4})', info_text)
                        year = int(year_match.group(1)) if year_match else None
                        
                        # 提取国家/地区和类型
                        info_lines = info_text.split('\n')
                        if len(info_lines) >= 2:
                            second_line = info_lines[1].strip()
                            # 简单提取类型信息
                            genre_match = re.search(r'(剧情|喜剧|动作|爱情|科幻|动画|悬疑|惊悚|恐怖|犯罪|同性|音乐|歌舞|传记|历史|战争|西部|奇幻|冒险|灾难|武侠|古装)', second_line)
                            genre = genre_match.group(1) if genre_match else "剧情"
                        else:
                            genre = "剧情"
                        
                        # 获取豆瓣评分
                        rating_element = item.select_one('.rating_num')
                        rating = float(rating_element.text) if rating_element else None
                        
                        # 获取简介
                        quote_element = item.select_one('.inq')
                        description = quote_element.text if quote_element else f"这是一部备受好评的{genre}电影。"
                        
                        # 获取电影详情页链接
                        detail_link = item.select_one('.hd a')['href'] if item.select_one('.hd a') else ""
                        
                        movie_data = {
                            'title': title,
                            'description': description,
                            'year': year,
                            'rating': rating,
                            'image_url': image_url,
                            'netflix_url': detail_link or f'https://movie.douban.com/subject/movie-{len(movies)+1}',
                            'category': '电影',
                            'genre': genre
                        }
                        
                        movies.append(movie_data)
                        
                        # 如果已达到限制数量，退出循环
                        if len(movies) >= limit:
                            break
                            
                    except Exception as e:
                        print(f"解析单个电影信息时出错: {e}")
                        continue
                
                # 如果没有更多电影，退出循环
                if len(movie_items) < per_page:
                    break
                
                start += per_page
                time.sleep(random.uniform(1, 2))  # 随机延时，避免请求过快
                
            return movies[:limit]
            
        except Exception as e:
            print(f"爬取豆瓣电影Top250数据时出错: {e}")
            return []
    
    def scrape_douban_nowplaying(self, limit=20):
        """
        从豆瓣电影正在热映爬取最新电影数据，包括真实图片链接
        """
        try:
            url = "https://movie.douban.com/cinema/nowplaying/beijing/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            movies = []
            
            # 查找正在上映的电影
            movie_items = soup.select('#nowplaying .lists .list-item')
            
            for i, item in enumerate(movie_items[:limit]):
                try:
                    # 获取电影ID和标题
                    movie_id = item.get('data-subject')
                    title = item.get('data-title', '')
                    
                    if not title or not movie_id:
                        continue
                    
                    # 获取评分
                    rating = item.get('data-score')
                    rating = float(rating) if rating else None
                    
                    # 获取年份
                    year = item.get('data-release', '')
                    year = int(year) if year and year.isdigit() else None
                    
                    # 获取类型
                    genre = item.get('data-category', '电影')
                    
                    # 获取简介
                    description = f"正在热映的{genre}作品。"
                    
                    # 获取图片URL
                    image_url = ''
                    img_element = item.select_one('img')
                    if img_element and img_element.get('src'):
                        image_url = img_element['src']
                        # 转换为较大尺寸的图片
                        image_url = image_url.replace('/s_ratio_poster/', '/l_ratio_poster/')
                        image_url = image_url.replace('/m_ratio_poster/', '/l_ratio_poster/')
                    
                    movie_data = {
                        'title': title,
                        'description': description,
                        'year': year,
                        'rating': rating,
                        'image_url': image_url,
                        'netflix_url': f'https://movie.douban.com/subject/{movie_id}/',
                        'category': genre,
                        'genre': genre
                    }
                    
                    movies.append(movie_data)
                    time.sleep(0.5)  # 避免请求过快
                    
                except Exception as e:
                    print(f"解析正在热映电影信息时出错: {e}")
                    continue
            
            return movies
            
        except Exception as e:
            print(f"爬取豆瓣正在热映电影数据时出错: {e}")
            return []
    
    def scrape_douban_coming_soon(self, limit=20):
        """
        从豆瓣电影即将上映爬取即将上映的电影数据
        """
        try:
            url = "https://movie.douban.com/coming"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            movies = []
            
            # 查找即将上映的电影
            movie_rows = soup.select('table.coming_list tbody tr')
            
            for i, row in enumerate(movie_rows[:limit]):
                try:
                    # 获取日期
                    date_element = row.select_one('td:nth-child(1)')
                    date = date_element.text.strip() if date_element else ''
                    
                    # 获取电影标题
                    title_element = row.select_one('td:nth-child(2) a')
                    if not title_element:
                        continue
                        
                    title = title_element.text.strip()
                    detail_link = title_element['href']
                    
                    # 获取图片链接（从详情页链接中提取）
                    image_url = ''
                    
                    # 获取类型
                    genre_element = row.select_one('td:nth-child(3)')
                    genre = genre_element.text.strip() if genre_element else '电影'
                    
                    # 获取地区
                    region_element = row.select_one('td:nth-child(4)')
                    region = region_element.text.strip() if region_element else '未知'
                    
                    # 获取期待人数
                    wish_element = row.select_one('td:nth-child(5)')
                    wish_count = wish_element.text.strip() if wish_element else ''
                    
                    # 构造简介
                    description = f"即将上映的{genre}电影，来自{region}。期待人数：{wish_count}"
                    
                    movie_data = {
                        'title': title,
                        'description': description,
                        'year': None,  # 即将上映，暂无年份
                        'rating': None,  # 未上映，暂无评分
                        'image_url': image_url,
                        'netflix_url': detail_link,
                        'category': '电影',
                        'genre': genre
                    }
                    
                    movies.append(movie_data)
                    time.sleep(0.5)  # 避免请求过快
                    
                except Exception as e:
                    print(f"解析即将上映电影信息时出错: {e}")
                    continue
            
            return movies
            
        except Exception as e:
            print(f"爬取豆瓣即将上映电影数据时出错: {e}")
            return []
    
    def get_movie_poster_from_detail_page(self, detail_url):
        """
        从电影详情页获取海报图片
        """
        try:
            print(f"正在从详情页获取海报图片: {detail_url}")
            response = self.session.get(detail_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找海报图片
            poster_element = soup.select_one('#mainpic img')
            if poster_element and poster_element.get('src'):
                image_url = poster_element['src']
                # 转换为较大尺寸的图片
                image_url = image_url.replace('/s_ratio_poster/', '/l_ratio_poster/')
                image_url = image_url.replace('/m_ratio_poster/', '/l_ratio_poster/')
                print(f"成功获取海报图片: {image_url}")
                return image_url
            
            print("未找到海报图片")
            return ''
        except Exception as e:
            print(f"从详情页获取海报图片时出错: {e}")
            return ''
    
    def scrape_multiple_douban_sources(self, limit=30):
        """
        从豆瓣多个数据源爬取电影数据
        """
        all_movies = []
        
        # 从豆瓣Top250爬取高分电影
        print("正在从豆瓣电影Top250爬取数据...")
        top_movies = self.scrape_douban_top_movies(min(limit, 15))
        all_movies.extend(top_movies)
        
        # 从正在热映爬取最新电影
        print("正在从豆瓣正在热映爬取数据...")
        now_playing = self.scrape_douban_nowplaying(min(limit//2, 10))
        all_movies.extend(now_playing)
        
        # 从即将上映爬取未来电影
        print("正在从豆瓣即将上映爬取数据...")
        coming_soon = self.scrape_douban_coming_soon(min(limit//3, 5))
        all_movies.extend(coming_soon)
        
        # 对于没有图片的电影，尝试从详情页获取
        for movie in all_movies:
            if not movie['image_url'] and movie['netflix_url']:
                print(f"正在从详情页获取 {movie['title']} 的海报图片...")
                movie['image_url'] = self.get_movie_poster_from_detail_page(movie['netflix_url'])
                time.sleep(1)  # 避免请求过快
        
        # 去重处理
        unique_movies = []
        seen_titles = set()
        
        for movie in all_movies:
            if movie['title'] not in seen_titles:
                unique_movies.append(movie)
                seen_titles.add(movie['title'])
        
        return unique_movies[:limit]
    
    def save_movies_to_db(self, movies_data):
        """
        将电影数据保存到数据库
        """
        added_count = 0
        updated_count = 0
        
        # 确保在应用上下文中运行
        from app import db
        
        for movie_data in movies_data:
            # 检查电影是否已存在（通过标题）
            existing_movie = Movie.query.filter_by(title=movie_data['title']).first()
            
            if existing_movie:
                # 更新现有电影信息
                existing_movie.description = movie_data['description']
                existing_movie.year = movie_data['year']
                existing_movie.rating = movie_data['rating']
                # 只有当新图片URL不为空且不是占位符时才更新
                if movie_data['image_url'] and 'example.com' not in movie_data['image_url'] and 'placeholder.com' not in movie_data['image_url']:
                    existing_movie.image_url = movie_data['image_url']
                existing_movie.netflix_url = movie_data['netflix_url']
                existing_movie.category = movie_data['category']
                existing_movie.genre = movie_data['genre']
                updated_count += 1
            else:
                # 添加新电影
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
        
        try:
            db.session.commit()
            print(f"成功添加 {added_count} 部新电影，更新 {updated_count} 部电影")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"保存电影数据时出错: {e}")
            return False
    
    def update_movie_database(self, limit=30):
        """
        更新电影数据库
        """
        print("开始从豆瓣电影爬取数据...")
        movies = self.scrape_multiple_douban_sources(limit)
        print(f"共爬取到 {len(movies)} 部电影")
        
        if movies:
            return self.save_movies_to_db(movies)
        return False

def init_movie_data(limit=30):
    """
    初始化电影数据
    """
    scraper = NetflixScraper()
    return scraper.update_movie_database(limit)

if __name__ == "__main__":
    # 可以直接运行此脚本来更新电影数据
    success = init_movie_data()
    if success:
        print("电影数据更新成功")
    else:
        print("电影数据更新失败")