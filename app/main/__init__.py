from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Post, Category, Tag, Comment, Message
# 导入天气爬虫类
from app.utils.weather_crawler import WeatherCrawler
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=5, error_out=False)
    
    # 获取侧边栏数据
    recent_posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).limit(5).all()
    categories = Category.query.all()
    tags = Tag.query.all()
    
    return render_template('main/index.html', posts=posts, 
                          recent_posts=recent_posts, 
                          categories=categories, 
                          tags=tags)

@bp.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    if not post.is_published and (not current_user.is_authenticated or not current_user.is_admin):
        flash('该文章未发布')
        return redirect(url_for('main.index'))
    
    comments = Comment.query.filter_by(post_id=id, is_approved=True).all()
    
    # 获取相关文章
    related_posts = Post.query.filter(
        Post.category_id == post.category_id, 
        Post.id != post.id, 
        Post.is_published == True
    ).order_by(Post.created_at.desc()).limit(5).all()
    
    return render_template('main/post.html', post=post, comments=comments, related_posts=related_posts)

@bp.route('/category/<int:id>')
def category(id):
    category = Category.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category_id=id, is_published=True).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=5, error_out=False)
    
    # 获取侧边栏数据
    categories = Category.query.all()
    
    return render_template('main/category.html', category=category, posts=posts, categories=categories)

@bp.route('/tag/<int:id>')
def tag(id):
    tag = Tag.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    posts = tag.posts.filter_by(is_published=True).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=5, error_out=False)
    
    # 获取侧边栏数据
    tags = Tag.query.all()
    
    return render_template('main/tag.html', tag=tag, posts=posts, tags=tags)

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/weather', methods=['GET', 'POST'])
def weather():
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


@bp.route('/message_board', methods=['GET', 'POST'])
def message_board():
    if request.method == 'POST':
        # 处理留言提交
        author_name = request.form.get('author_name', '').strip()
        author_email = request.form.get('author_email', '').strip()
        author_website = request.form.get('author_website', '').strip()
        content = request.form.get('content', '').strip()
        
        # 验证必填字段
        if not author_name or not content:
            flash('姓名和留言内容不能为空')
            return redirect(url_for('main.message_board'))
        
        # 创建留言对象
        message = Message(
            author_name=author_name,
            content=content,
            is_approved=False  # 默认不审核通过，需要管理员审核
        )
        
        # 设置可选字段
        if author_email:
            message.author_email = author_email
        if author_website:
            message.author_website = author_website
        if current_user.is_authenticated:
            message.author_id = current_user.id
            
        # 保存到数据库
        try:
            db.session.add(message)
            db.session.commit()
            flash('留言提交成功，等待管理员审核后显示')
        except Exception as e:
            db.session.rollback()
            flash('留言提交失败，请稍后重试')
        
        return redirect(url_for('main.message_board'))
    
    # 处理GET请求，显示留言页面
    page = request.args.get('page', 1, type=int)
    # 只显示已审核通过的留言
    messages = Message.query.filter_by(is_approved=True).order_by(Message.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('main/message_board.html', messages=messages.items, pagination=messages)
