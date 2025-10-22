from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Post, Category, Tag, Comment, Message, Movie

bp = Blueprint('admin', __name__)

@bp.before_request
@login_required
def before_request():
    if not current_user.is_admin:
        flash('您没有权限访问该页面')
        return redirect(url_for('blog.index'))

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    post_count = Post.query.count()
    comment_count = Comment.query.count()
    return render_template('admin/dashboard.html', post_count=post_count, comment_count=comment_count)

@bp.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/posts.html', posts=posts)

@bp.route('/post/new', methods=['GET', 'POST'])
@bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id=None):
    post = Post() if id is None else Post.query.get_or_404(id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.summary = request.form['summary'][:500] if request.form['summary'] else ''
        post.category_id = request.form.get('category', type=int)
        post.is_published = bool(request.form.get('is_published'))
        
        if id is None:
            post.author_id = current_user.id
            db.session.add(post)  # type: ignore
        
        # 处理标签
        tag_names = [tag.strip() for tag in request.form['tags'].split(',') if tag.strip()]
        post.tags.clear()
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag()
                tag.name = tag_name
                db.session.add(tag)  # type: ignore
            post.tags.append(tag)
        
        db.session.commit()  # type: ignore
        flash('文章保存成功')
        return redirect(url_for('admin.posts'))
    
    tag_list = ','.join([tag.name for tag in post.tags])
    return render_template('admin/edit_post.html', post=post, categories=categories, tag_list=tag_list)

@bp.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)  # type: ignore
    db.session.commit()  # type: ignore
    flash('文章删除成功')
    return redirect(url_for('admin.posts'))

@bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@bp.route('/category/new', methods=['POST'])
def new_category():
    name = request.form['name']
    if name:
        category = Category()
        category.name = name
        db.session.add(category)  # type: ignore
        db.session.commit()  # type: ignore
        flash('分类创建成功')
    return redirect(url_for('admin.categories'))

@bp.route('/category/<int:id>/delete', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)  # type: ignore
    db.session.commit()  # type: ignore
    flash('分类删除成功')
    return redirect(url_for('admin.categories'))

@bp.route('/comments')
def comments():
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.order_by(Comment.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/comments.html', comments=comments)

@bp.route('/comment/<int:id>/toggle', methods=['POST'])
def toggle_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.is_approved = not comment.is_approved
    db.session.commit()  # type: ignore
    status = "已批准" if comment.is_approved else "未批准"
    flash(f'评论状态已更新为{status}')
    return redirect(url_for('admin.comments'))


@bp.route('/messages')
def messages():
    page = request.args.get('page', 1, type=int)
    messages = Message.query.order_by(Message.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/messages.html', messages=messages)


@bp.route('/message/<int:id>/toggle', methods=['POST'])
def toggle_message(id):
    message = Message.query.get_or_404(id)
    message.is_approved = not message.is_approved
    db.session.commit()  # type: ignore
    status = "已批准" if message.is_approved else "未批准"
    flash(f'留言状态已更新为{status}')
    return redirect(url_for('admin.messages'))


@bp.route('/message/<int:id>/delete', methods=['POST'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)  # type: ignore
    db.session.commit()  # type: ignore
    flash('留言删除成功')
    return redirect(url_for('admin.messages'))


@bp.route('/movies')
def movies():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.order_by(Movie.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/movies.html', movies=movies)


@bp.route('/movie/new', methods=['GET', 'POST'])
@bp.route('/movie/<int:id>/edit', methods=['GET', 'POST'])
def edit_movie(id=None):
    movie = Movie() if id is None else Movie.query.get_or_404(id)
    
    if request.method == 'POST':
        movie.title = request.form['title']
        movie.description = request.form['description']
        movie.year = request.form.get('year', type=int)
        movie.rating = request.form.get('rating', type=float)
        movie.image_url = request.form['image_url']
        movie.netflix_url = request.form['netflix_url']
        movie.category = request.form['category']
        movie.genre = request.form['genre']
        movie.is_featured = bool(request.form.get('is_featured'))
        
        if id is None:
            db.session.add(movie)  # type: ignore
        
        try:
            db.session.commit()  # type: ignore
            flash('电影信息保存成功')
        except Exception as e:
            db.session.rollback()  # type: ignore
            flash('电影信息保存失败，请稍后重试')
        
        return redirect(url_for('admin.movies'))
    
    return render_template('admin/edit_movie.html', movie=movie)


@bp.route('/movie/<int:id>/delete', methods=['POST'])
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)  # type: ignore
    db.session.commit()  # type: ignore
    flash('电影删除成功')
    return redirect(url_for('admin.movies'))