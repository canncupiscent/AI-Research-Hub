from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between users and projects
project_users = Table(
    'project_users',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('project_id', Integer, ForeignKey('projects.id'))
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    projects = relationship('Project', secondary=project_users, back_populates='users')
    owned_datasets = relationship('Dataset', back_populates='owner')

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship('User', secondary=project_users, back_populates='projects')
    datasets = relationship('Dataset', back_populates='project')

class Dataset(Base):
    __tablename__ = 'datasets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    file_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    
    # Relationships
    owner = relationship('User', back_populates='owned_datasets')
    project = relationship('Project', back_populates='datasets') 