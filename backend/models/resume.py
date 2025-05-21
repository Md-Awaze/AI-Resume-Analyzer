"""
Database models for the Resume Analyzer application.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Index, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Resume(Base):
    """Resume model for storing uploaded resume information."""
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)
    upload_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    raw_text = Column(Text, nullable=False)
    status = Column(String(20), default='pending')
    resume_metadata = Column(JSON)

    # Create indexes for frequently queried columns
    __table_args__ = (
        Index('idx_filename', filename),
        Index('idx_upload_date', upload_date),
    )

    def __repr__(self):
        return f"<Resume(id={self.id}, filename='{self.filename}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'filename': self.filename,
            'file_type': self.file_type,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'status': self.status,
            'text_preview': (self.raw_text[:150] + '...') if self.raw_text and len(self.raw_text) > 150 else self.raw_text,
            'metadata': self.resume_metadata
        }