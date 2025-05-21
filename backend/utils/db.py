"""
Database utility functions for the Resume Analyzer application.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from models.resume import Base

class Database:
    """Database connection and session management."""
    _instance = None
    
    def __new__(cls, database_uri=None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, database_uri=None):
        if self._initialized:
            return
            
        self.database_uri = database_uri
        self.engine = create_engine(
            database_uri,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
        )
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        self._initialized = True
    
    def create_tables(self):
        """Create all tables defined in models."""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Get a database session."""
        return self.Session()
    
    def close_session(self):
        """Close the scoped session."""
        self.Session.remove()