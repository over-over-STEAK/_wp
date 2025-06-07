from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.main import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯使用者
    author = relationship('User', back_populates='posts')

    def __init__(self, title, content, user_id):
        self.title = title.strip()
        self.content = content.strip()
        self.user_id = user_id

    def __repr__(self):
        return f"<Post #{self.id} - {self.title}>"
