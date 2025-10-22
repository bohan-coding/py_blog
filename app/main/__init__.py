from flask import Blueprint

# 创建主蓝图
bp = Blueprint('main', __name__)

# 注意：具体的功能路由已拆分到以下独立的蓝图文件中：
# 1. app/main/blog.py - 博客相关功能（首页、文章、分类、标签等）
# 2. app/main/weather.py - 天气查询功能
# 3. app/main/message_board.py - 留言本功能
# 4. app/main/article.py - 知识库文章功能

# 如果需要添加新的全局路由或处理逻辑，可以在这里添加
