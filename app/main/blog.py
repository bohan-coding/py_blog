from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app import db
from app.models import Post, Category, Tag, Comment

bp = Blueprint('blog', __name__)

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
        return redirect(url_for('blog.index'))
    
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