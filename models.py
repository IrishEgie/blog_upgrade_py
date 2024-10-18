from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Text, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db

class Base(DeclarativeBase):
    pass

class BlogPost(db.Model):
    __tablename__ = 'blog_post'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    author: Mapped['User'] = relationship('User', back_populates='blog_posts')

class Comment(db.Model):
    __tablename__ = 'comment'  # Ensure you have a table name

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('blog_post.id'), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Add this line

    post = relationship('BlogPost', back_populates='comments')
    author = relationship('User', back_populates='comments')


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    blog_posts: Mapped[list[BlogPost]] = relationship('BlogPost', back_populates='author')
    comments: Mapped[list[Comment]] = relationship('Comment', back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
