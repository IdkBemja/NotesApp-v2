import os
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

note_category = Table('note_category', Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(45))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    notes = relationship('Note', back_populates='user')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    notes = relationship(
        'Note',
        secondary=note_category,
        backref=backref('categories')
    )

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String(45))
    content = Column(String(255))
    # status = Column(String(8))
    # category = Column(String(45))
    # tags = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='notes')

class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

def init_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("La variable de entorno DATABASE_URL no está configurada.")
    
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    return Session()

session = init_db()