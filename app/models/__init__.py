# 导入所有模型类，保持与原来相同的接口
from .user_models import User
from .blog_models import Category, Tag, Post, Comment, post_tags
from .message_models import Message
from .movie_models import Movie, MovieReview

# 为了保持向后兼容性，导出所有模型类
__all__ = [
    'User',
    'Category',
    'Tag',
    'Post',
    'Comment',
    'post_tags',
    'Message',
    'Movie',
    'MovieReview'
]