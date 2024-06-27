import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, create_engine
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)

    # Relationship
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='author')
    followers = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='follower')
    followed = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='followed')

class Follower(Base):
    __tablename__ = 'follower'
    
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    # Relationships
    follower = relationship('User', foreign_keys=[user_from_id], back_populates='followers')
    followed = relationship('User', foreign_keys=[user_to_id], back_populates='followed')

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Relationship
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'
  
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(500))
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    # Relationships
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Media(Base):
    __tablename__ = 'media'
  
    id = Column(Integer, primary_key=True)
    type = Column(Enum('mp4', 'mp3', 'video', name='type_enum'))
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    # Relationship
    post = relationship('Post', back_populates='media')
    
    def to_dict(self):
        return {}

try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
