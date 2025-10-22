from app import create_app, db
from app.models import User, Category, Tag, Post, Comment
from werkzeug.security import generate_password_hash

def init_test_data():
    app = create_app()
    with app.app_context():
        # 清空现有数据
        db.session.query(Post).delete()  # type: ignore
        db.session.query(Category).delete()  # type: ignore
        db.session.query(Tag).delete()  # type: ignore
        db.session.query(Comment).delete()  # type: ignore
        db.session.commit()  # type: ignore
        
        # 创建用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User()
            admin.username = 'admin'
            admin.email = 'admin@example.com'
            admin.is_admin = True
            admin.set_password('admin123')
            db.session.add(admin)  # type: ignore
        
        user1 = User()
        user1.username = 'user1'
        user1.email = 'user1@example.com'
        user1.set_password('password123')
        db.session.add(user1)  # type: ignore
        
        # 创建分类
        categories_data = [
            {'name': '技术分享'},
            {'name': '生活随笔'},
            {'name': '旅行日记'},
            {'name': '读书笔记'}
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category()
                category.name = cat_data['name']
                db.session.add(category)  # type: ignore
            categories.append(category)
        
        db.session.commit()  # type: ignore
        
        # 创建标签
        tags_data = ['Python', 'Flask', 'MySQL', 'Web开发', '生活', '旅行', '读书']
        tags = []
        for tag_name in tags_data:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag()
                tag.name = tag_name
                db.session.add(tag)  # type: ignore
            tags.append(tag)
        
        db.session.commit()  # type: ignore
        
        # 创建文章
        posts_data = [
            {
                'title': 'Flask入门教程',
                'content': '<p>Flask是一个使用Python编写的轻量级Web应用框架。基于Werkzeug WSGI工具箱和Jinja2模板引擎。</p><p>Flask被称为"microframework"，因为它使用简单的核心，用extension增加其他功能。Flask没有默认使用的数据库、窗体验证工具。</p>',
                'summary': 'Flask是一个使用Python编写的轻量级Web应用框架。本文介绍了Flask的基本概念和使用方法。',
                'author': admin,
                'category': categories[0],  # 技术分享
                'tags': [tags[0], tags[1], tags[3]],  # Python, Flask, Web开发
                'is_published': True
            },
            {
                'title': 'MySQL数据库优化技巧',
                'content': '<p>MySQL是世界上最流行的开源关系型数据库管理系统之一。在实际应用中，数据库性能优化是非常重要的。</p><p>本文将介绍几种常见的MySQL优化技巧：</p><ul><li>索引优化</li><li>查询优化</li><li>表结构设计</li><li>配置参数调整</li></ul>',
                'summary': 'MySQL是世界上最流行的开源关系型数据库管理系统之一。本文介绍了几种常见的MySQL优化技巧。',
                'author': admin,
                'category': categories[0],  # 技术分享
                'tags': [tags[2], tags[3]],  # MySQL, Web开发
                'is_published': True
            },
            {
                'title': '周末的悠闲时光',
                'content': '<p>忙碌了一周，终于迎来了周末。阳光透过窗帘洒在桌面上，一切都显得那么宁静美好。</p><p>泡一壶茶，拿起一本喜欢的书，享受这难得的悠闲时光。生活不只有工作，还有诗和远方。</p>',
                'summary': '忙碌了一周，终于迎来了周末。享受这难得的悠闲时光，感受生活的美好。',
                'author': user1,
                'category': categories[1],  # 生活随笔
                'tags': [tags[4]],  # 生活
                'is_published': True
            },
            {
                'title': '春天的旅行计划',
                'content': '<p>春天是旅行的好季节，万物复苏，景色宜人。计划一次说走就走的旅行，去感受大自然的美好。</p><p>推荐几个适合春季旅行的地方：</p><ol><li>江南水乡</li><li>云南大理</li><li>桂林山水</li><li>杭州西湖</li></ol>',
                'summary': '春天是旅行的好季节，推荐几个适合春季旅行的地方，计划一次说走就走的旅行。',
                'author': user1,
                'category': categories[2],  # 旅行日记
                'tags': [tags[5]],  # 旅行
                'is_published': True
            },
            {
                'title': '《Python编程：从入门到实践》读后感',
                'content': '<p>最近读完了《Python编程：从入门到实践》这本书，收获颇丰。这本书非常适合Python初学者，内容循序渐进，实例丰富。</p><p>书中主要涵盖了以下几个方面的内容：</p><ul><li>Python基础知识</li><li>数据可视化</li><li>Web开发</li><li>项目实战</li></ul><p>通过这本书的学习，我对Python有了更深入的理解，也激发了我继续深入学习的兴趣。</p>',
                'summary': '《Python编程：从入门到实践》是一本非常适合Python初学者的书籍，内容循序渐进，实例丰富。',
                'author': admin,
                'category': categories[3],  # 读书笔记
                'tags': [tags[0], tags[6]],  # Python, 读书
                'is_published': True
            }
        ]
        
        posts = []
        for post_data in posts_data:
            post = Post()
            post.title = post_data['title']
            post.content = post_data['content']
            post.summary = post_data['summary']
            post.author = post_data['author']
            post.category = post_data['category']
            post.is_published = post_data['is_published']
            db.session.add(post)  # type: ignore
            posts.append(post)
        
        db.session.commit()  # type: ignore
        
        # 关联文章和标签
        for i, post_data in enumerate(posts_data):
            for tag in post_data['tags']:
                posts[i].tags.append(tag)
        
        db.session.commit()  # type: ignore
        
        # 创建评论
        comments_data = [
            {
                'content': '这篇文章写得很好，对我学习Flask帮助很大！',
                'author': user1,
                'post': posts[0]
            },
            {
                'content': '感谢分享，MySQL优化确实很重要。',
                'author': user1,
                'post': posts[1]
            },
            {
                'content': '生活需要这样的慢时光，很治愈。',
                'author_name': '游客',
                'author_email': 'visitor@example.com',
                'post': posts[2]
            }
        ]
        
        for comment_data in comments_data:
            comment = Comment()
            comment.content = comment_data['content']
            comment.post = comment_data['post']
            if 'author' in comment_data:
                comment.author = comment_data['author']
            else:
                comment.author_name = comment_data['author_name']
                comment.author_email = comment_data['author_email']
            db.session.add(comment)  # type: ignore
        
        db.session.commit()  # type: ignore
        
        print("测试数据初始化完成！")
        print(f"创建了 {len(categories)} 个分类")
        print(f"创建了 {len(tags)} 个标签")
        print(f"创建了 {len(posts)} 篇文章")
        print(f"创建了 {len(comments_data)} 条评论")

if __name__ == '__main__':
    init_test_data()