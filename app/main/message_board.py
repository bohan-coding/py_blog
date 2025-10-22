from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app import db
from app.models import Message

bp = Blueprint('message_board', __name__, url_prefix='/message_board')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 处理留言提交
        author_name = request.form.get('author_name', '').strip()
        author_email = request.form.get('author_email', '').strip()
        author_website = request.form.get('author_website', '').strip()
        content = request.form.get('content', '').strip()
        
        # 验证必填字段
        if not author_name or not content:
            flash('姓名和留言内容不能为空')
            return redirect(url_for('message_board.index'))
        
        # 创建留言对象
        message = Message(
            author_name=author_name,
            content=content,
            is_approved=False  # 默认不审核通过，需要管理员审核
        )
        
        # 设置可选字段
        if author_email:
            message.author_email = author_email
        if author_website:
            message.author_website = author_website
        if current_user.is_authenticated:
            message.author_id = current_user.id
            
        # 保存到数据库
        try:
            db.session.add(message)
            db.session.commit()
            flash('留言提交成功，等待管理员审核后显示')
        except Exception as e:
            db.session.rollback()
            flash('留言提交失败，请稍后重试')
        
        return redirect(url_for('message_board.index'))
    
    # 处理GET请求，显示留言页面
    page = request.args.get('page', 1, type=int)
    # 只显示已审核通过的留言
    messages = Message.query.filter_by(is_approved=True).order_by(Message.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('main/message_board.html', messages=messages.items, pagination=messages)