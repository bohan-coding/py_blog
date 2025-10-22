from app import db
from datetime import datetime

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