from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Movie, MovieReview

bp = Blueprint('movies', __name__, url_prefix='/movies')

@bp.route('/')
def index():
    """电影清单首页"""
    # 获取推荐电影
    featured_movies = Movie.query.filter_by(is_featured=True).order_by(Movie.created_at.desc()).limit(5).all()
    
    # 获取最新添加的电影
    latest_movies = Movie.query.order_by(Movie.created_at.desc()).limit(10).all()
    
    # 获取高分电影
    top_rated_movies = Movie.query.filter(Movie.rating.isnot(None)).order_by(Movie.rating.desc()).limit(10).all()
    
    return render_template('movies/index.html', 
                         featured_movies=featured_movies,
                         latest_movies=latest_movies,
                         top_rated_movies=top_rated_movies)

@bp.route('/list')
def movie_list():
    """电影列表页面"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    genre = request.args.get('genre', '')
    sort_by = request.args.get('sort_by', 'created_at')
    
    query = Movie.query
    
    # 根据分类筛选
    if category:
        query = query.filter_by(category=category)
    
    # 根据类型筛选
    if genre:
        query = query.filter(Movie.genre.like(f'%{genre}%'))
    
    # 排序
    if sort_by == 'rating':
        query = query.order_by(Movie.rating.desc().nulls_last())
    elif sort_by == 'year':
        query = query.order_by(Movie.year.desc())
    else:
        query = query.order_by(Movie.created_at.desc())
    
    movies = query.paginate(page=page, per_page=12, error_out=False)
    
    # 获取所有分类和类型用于筛选
    categories = db.session.query(Movie.category).distinct().all()
    genres = db.session.query(Movie.genre).distinct().all()
    
    return render_template('movies/list.html', 
                         movies=movies,
                         categories=categories,
                         genres=genres,
                         current_category=category,
                         current_genre=genre,
                         current_sort=sort_by)

@bp.route('/<int:id>')
def detail(id):
    """电影详情页面"""
    movie = Movie.query.get_or_404(id)
    
    # 获取该电影的评论
    reviews = MovieReview.query.filter_by(movie_id=id).order_by(MovieReview.created_at.desc()).all()
    
    # 计算平均评分
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        avg_rating = 0
    
    return render_template('movies/detail.html', 
                         movie=movie,
                         reviews=reviews,
                         avg_rating=avg_rating)

@bp.route('/<int:id>/review', methods=['POST'])
@login_required
def add_review(id):
    """添加电影评论"""
    movie = Movie.query.get_or_404(id)
    
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()
    
    # 验证数据
    if not rating or rating < 1 or rating > 10:
        flash('请选择有效的评分（1-10分）')
        return redirect(url_for('movies.detail', id=id))
    
    if not comment:
        flash('请填写评论内容')
        return redirect(url_for('movies.detail', id=id))
    
    # 检查用户是否已经评论过这部电影
    existing_review = MovieReview.query.filter_by(movie_id=id, author_id=current_user.id).first()
    if existing_review:
        flash('您已经评论过这部电影了')
        return redirect(url_for('movies.detail', id=id))
    
    # 创建新评论
    review = MovieReview(
        rating=rating,
        comment=comment,
        movie_id=id,
        author_id=current_user.id
    )
    
    try:
        db.session.add(review)
        db.session.commit()
        flash('评论添加成功')
    except Exception as e:
        db.session.rollback()
        flash('评论添加失败，请稍后重试')
    
    return redirect(url_for('movies.detail', id=id))

@bp.route('/<int:id>/toggle_featured', methods=['POST'])
@login_required
def toggle_featured(id):
    """切换电影推荐状态（仅管理员）"""
    if not current_user.is_admin:
        flash('您没有权限执行此操作')
        return redirect(url_for('movies.index'))
    
    movie = Movie.query.get_or_404(id)
    movie.is_featured = not movie.is_featured
    
    try:
        db.session.commit()
        status = "推荐" if movie.is_featured else "取消推荐"
        flash(f'电影已{status}')
    except Exception as e:
        db.session.rollback()
        flash('操作失败，请稍后重试')
    
    return redirect(url_for('movies.detail', id=id))