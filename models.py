from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Text
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db  # Use absolute import

class Base(DeclarativeBase):
    pass

class BlogPost(db.Model):
    __tablename__ = 'blog_post'  # Specify table name if desired

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    
    # Foreign key to link to the User table
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    # Relationship back to the User
    author: Mapped['User'] = relationship('User', back_populates='blog_posts')

class User(UserMixin, db.Model):
    __tablename__ = 'user'  # Specify table name if desired

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    # Relationship to access all BlogPosts by this User
    blog_posts: Mapped[list[BlogPost]] = relationship('BlogPost', back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Pass the password here