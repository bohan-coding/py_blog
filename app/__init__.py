from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
import os

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录以访问此页面。'
csrf = CSRFProtect()

# 添加用户加载函数
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, 'static')
    
    app = Flask(__name__, 
                static_folder=static_dir,
                static_url_path='/static')
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # 注册蓝图
    # 移除旧的主蓝图注册
    # from app.main import bp as main_bp
    # app.register_blueprint(main_bp)
    
    # 注册新的蓝图
    from app.main.blog import bp as blog_bp
    app.register_blueprint(blog_bp)
    
    from app.main.weather import bp as weather_bp
    app.register_blueprint(weather_bp)
    
    from app.main.message_board import bp as message_board_bp
    app.register_blueprint(message_board_bp)
    
    from app.main.article import bp as article_bp
    app.register_blueprint(article_bp)
    
    from app.main.movies import bp as movies_bp
    app.register_blueprint(movies_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app