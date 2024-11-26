from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Table, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy.sql import func

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

class AnalyzedPaper(Base):
    """Model for storing analyzed papers."""
    __tablename__ = 'analyzed_papers'

    id = Column(Integer, primary_key=True)
    source_id = Column(String(255), unique=True, nullable=False)  # arxiv_ID or semantic_scholar_ID
    title = Column(String(500), nullable=False)
    abstract = Column(Text)
    authors = Column(JSON)  # Store as JSON array
    year = Column(Integer)
    venue = Column(String(255))
    url = Column(String(500))
    citations = Column(Integer)
    source = Column(String(50))  # "arXiv" or "Semantic Scholar"
    
    # Analysis results
    summary = Column(Text)
    key_findings = Column(JSON)  # Store as JSON array
    methodology = Column(Text)
    applications = Column(JSON)  # Store as JSON array
    future_work = Column(JSON)  # Store as JSON array
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "source_id": self.source_id,
            "title": self.title,
            "abstract": self.abstract,
            "authors": self.authors,
            "year": self.year,
            "venue": self.venue,
            "url": self.url,
            "citations": self.citations,
            "source": self.source,
            "analysis": {
                "summary": self.summary,
                "key_findings": self.key_findings,
                "methodology": self.methodology,
                "applications": self.applications,
                "future_work": self.future_work
            },
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 