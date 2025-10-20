from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 多对多关系
    posts = db.relationship('Post', secondary='post_tags', backref=db.backref('tags', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Tag {self.name}>'

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # 关系
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    
    def __repr__(self):
        return f'<Post {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(80))  # 非注册用户也可以评论
    author_email = db.Column(db.String(120))
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<Comment {self.id}>'


class Message(db.Model):
    """
    留言本模型
    """
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(80), nullable=False)
    author_email = db.Column(db.String(120))
    author_website = db.Column(db.String(200))  # 网站链接（可选）
    is_approved = db.Column(db.Boolean, default=True)  # 是否审核通过
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键（可选，如果注册用户留言）
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<Message {self.id}: {self.author_name}>'


class Movie(db.Model):
    """
    电影清单模型
    """
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # 电影标题
    description = db.Column(db.Text)  # 描述
    year = db.Column(db.Integer)  # 年份
    rating = db.Column(db.Float)  # 评分
    image_url = db.Column(db.String(500))  # 海报图片链接
    netflix_url = db.Column(db.String(500))  # 网飞链接
    category = db.Column(db.String(50))  # 分类（电影/电视剧）
    genre = db.Column(db.String(100))  # 类型（动作/喜剧等）
    is_featured = db.Column(db.Boolean, default=False)  # 是否推荐
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    reviews = db.relationship('MovieReview', backref='movie', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Movie {self.title}>'


class MovieReview(db.Model):
    """
    电影评分和评论模型
    """
    __tablename__ = 'movie_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)  # 用户评分（1-10）
    comment = db.Column(db.Text)  # 用户评论
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 关系
    author = db.relationship('User', backref=db.backref('movie_reviews', lazy='dynamic'))
    
    def __repr__(self):
        return f'<MovieReview {self.id} for Movie {self.movie_id}>'

