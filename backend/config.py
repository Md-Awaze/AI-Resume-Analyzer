"""
Configuration module for the Flask application.
Contains all configuration settings loaded from environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-for-development-only')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///data.db')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 10 * 1024 * 1024))  # Default 10MB
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 10))
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}

    @staticmethod
    def init_app(app):
        """Initialize the application with this configuration."""
        # Create upload folder if it doesn't exist
        os.makedirs(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), exist_ok=True)