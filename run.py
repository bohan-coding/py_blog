from app import create_app, db
from app.models import User, Post, Category, Tag, Comment

app = create_app()

@app.before_first_request
def create_tables():
    db.create_all()
    
    # 创建默认管理员用户（如果不存在）
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        # 创建示例分类
        default_category = Category(name='默认分类')
        db.session.add(default_category)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)