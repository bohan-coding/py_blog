from app import create_app, db
from app.models import User, Post, Category, Tag, Comment

app = create_app()

@app.before_first_request
def create_tables():
    db.create_all()
    
    # 创建默认管理员用户（如果不存在）
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User()
        admin.username = 'admin'
        admin.email = 'admin@example.com'
        admin.is_admin = True
        admin.set_password('admin123')
        db.session.add(admin)  # type: ignore
        db.session.commit()  # type: ignore
        
        # 创建示例分类
        default_category = Category()
        default_category.name = '默认分类'
        db.session.add(default_category)  # type: ignore
        db.session.commit()  # type: ignore

if __name__ == '__main__':
    app.run(debug=True)