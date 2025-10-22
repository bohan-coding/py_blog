from app import db
from datetime import datetime

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