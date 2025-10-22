# 个人博客系统

基于Python Flask和MySQL 5.5开发的个人博客系统。

## 功能特性

- 用户注册和登录
- 文章发布和管理
- 分类和标签管理
- 评论功能
- 响应式设计

## 技术栈

- Python 3.7+
- Flask Web框架
- MySQL 5.5数据库
- Bootstrap 5前端框架

## 安装和配置

1. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```

2. 确保MySQL服务已启动，并创建数据库：
   ```sql
   CREATE DATABASE py_blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. 修改config.py中的数据库配置信息（如果需要）：
   ```python
   MYSQL_HOST = 'localhost'
   MYSQL_PORT = 3306
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = 'root'
   MYSQL_DB = 'py_blog'
   ```

4. 初始化数据库表：
   ```
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

5. 启动应用：
   ```
   python run.py
   ```

6. 访问博客：
   打开浏览器访问 http://127.0.0.1:5000

## 默认账户

- 管理员账户：admin
- 默认密码：admin123

## 目录结构

```
py_blog/
├── app/                 # 应用核心代码
│   ├── templates/       # HTML模板
│   ├── static/          # 静态文件
│   ├── main/            # 前台功能
│   │   ├── blog.py      # 博客核心功能
│   │   ├── weather.py   # 天气查询功能
│   │   ├── message_board.py  # 留言本功能
│   │   ├── article.py   # 知识库文章功能
│   │   ├── movies.py    # 电影清单功能
│   │   └── __init__.py  # 主蓝图初始化
│   ├── auth/            # 认证功能
│   ├── admin/           # 后台管理
│   ├── models/          # 数据模型包
│   │   ├── __init__.py  # 模型包初始化
│   │   ├── user_models.py    # 用户相关模型
│   │   ├── blog_models.py    # 博客相关模型
│   │   ├── message_models.py # 留言相关模型
│   │   └── movie_models.py   # 电影相关模型
│   ├── utils/           # 工具函数
│   └── __init__.py      # 应用初始化
├── config.py            # 配置文件
├── requirements.txt     # 依赖包列表
├── run.py               # 应用启动文件
└── README.md            # 说明文档
```

## 功能说明

### 前台功能
- 首页文章列表展示
- 文章详情查看
- 按分类浏览文章
- 按标签浏览文章
- 关于页面

### 后台管理
- 仪表板
- 文章管理（增删改查）
- 分类管理
- 评论管理
- 用户管理

## 开发说明

1. 数据模型定义在 `app/models/` 目录中，按业务领域拆分为多个文件
2. 路由和视图函数分别在 `app/main/`, `app/auth/`, `app/admin/` 目录中
3. 模板文件位于 `app/templates/` 目录中
4. 静态文件（CSS、JS、图片等）应放在 `app/static/` 目录中

## 注意事项

1. 本系统使用Flask内置服务器，仅适用于开发环境
2. 生产环境请使用专业的WSGI服务器如Gunicorn或uWSGI
3. 请定期备份数据库
4. 建议修改默认管理员密码