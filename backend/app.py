"""
Main Flask application file for the AI Resume Analyzer.
"""
import os
import time
import logging
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge

from config import Config
from utils.file_handlers import (
    allowed_file, 
    save_file, 
    extract_text, 
    get_file_extension, 
    sanitize_text
)
from utils.rate_limiter import RateLimiter, rate_limit
from utils.db import Database
from models.resume import Resume

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Enable CORS for all routes
CORS(app)

# Initialize rate limiter
rate_limiter = RateLimiter(app.config['RATE_LIMIT_PER_MINUTE'])

# Initialize database
db = Database(app.config['DATABASE_URI'])
db.create_tables()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Resource not found'
    }), 404

@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    return jsonify({
        'status': 'error',
        'message': f'File too large. Maximum allowed size is {app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024)}MB'
    }), 413

@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

# Routes
@app.route('/', methods=['GET'])
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/upload_resume', methods=['POST'])
@rate_limit(rate_limiter)
def upload_resume():
    """
    Upload and process a resume file.
    
    Accepts PDF or DOCX files, extracts text, and stores in database.
    """
    # Check if file is in request
    if 'file' not in request.files:
        logger.warning("No file part in request")
        return jsonify({
            'status': 'error',
            'message': 'No file part in the request'
        }), 400
    
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        logger.warning("No file selected")
        return jsonify({
            'status': 'error',
            'message': 'No file selected'
        }), 400
    
    # Check if file type is allowed
    if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
        logger.warning(f"File type not allowed: {file.filename}")
        return jsonify({
            'status': 'error',
            'message': 'File type not allowed. Allowed types: PDF, DOCX'
        }), 415
    
    # Save file
    success, result = save_file(file, app.config['UPLOAD_FOLDER'])
    if not success:
        logger.error(f"Error saving file: {result}")
        return jsonify({
            'status': 'error',
            'message': f"Error saving file: {result}"
        }), 500
    
    filename = result
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_type = get_file_extension(filename)
    
    # Extract text from file
    raw_text = extract_text(file_path, file_type)
    if raw_text.startswith('Error'):
        logger.error(raw_text)
        return jsonify({
            'status': 'error',
            'message': raw_text
        }), 500
    
    # Sanitize text
    sanitized_text = sanitize_text(raw_text)
    
    # Store in database
    try:
        session = db.get_session()
        new_resume = Resume(
            filename=filename,
            file_type=file_type,
            upload_date=datetime.utcnow(),
            raw_text=sanitized_text,
            status='uploaded',
            metadata={}
        )
        session.add(new_resume)
        session.commit()
        resume_id = new_resume.id
        session.close()
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error storing resume data',
            'details': str(e)
        }), 500
    
    # Return response
    return jsonify({
        'status': 'success',
        'resume_id': resume_id,
        'filename': filename,
        'file_type': file_type,
        'upload_timestamp': datetime.utcnow().isoformat(),
        'text_preview': sanitized_text[:150] + '...' if len(sanitized_text) > 150 else sanitized_text
    }), 201

@app.route('/resumes', methods=['GET'])
def get_resumes():
    """Get all resumes."""
    try:
        session = db.get_session()
        resumes = session.query(Resume).all()
        result = [resume.to_dict() for resume in resumes]
        session.close()
        return jsonify({
            'status': 'success',
            'count': len(result),
            'resumes': result
        })
    except Exception as e:
        logger.error(f"Error retrieving resumes: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error retrieving resumes',
            'details': str(e)
        }), 500

@app.route('/resume/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get a specific resume by ID."""
    try:
        session = db.get_session()
        resume = session.query(Resume).filter(Resume.id == resume_id).first()
        session.close()
        
        if resume is None:
            return jsonify({
                'status': 'error',
                'message': f'Resume with ID {resume_id} not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'resume': resume.to_dict()
        })
    except Exception as e:
        logger.error(f"Error retrieving resume {resume_id}: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving resume {resume_id}',
            'details': str(e)
        }), 500

@app.route('/resume/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    """Delete a resume by ID."""
    try:
        session = db.get_session()
        resume = session.query(Resume).filter(Resume.id == resume_id).first()
        
        if resume is None:
            session.close()
            return jsonify({
                'status': 'error',
                'message': f'Resume with ID {resume_id} not found'
            }), 404
        
        # Delete file from filesystem
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from database
        session.delete(resume)
        session.commit()
        session.close()
        
        return jsonify({
            'status': 'success',
            'message': f'Resume with ID {resume_id} deleted successfully'
        })
    except Exception as e:
        logger.error(f"Error deleting resume {resume_id}: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error deleting resume {resume_id}',
            'details': str(e)
        }), 500

@app.route('/resume/<int:resume_id>/update_status', methods=['PUT'])
def update_resume_status(resume_id):
    """Update the status of a resume."""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Status field is required'
            }), 400
        
        new_status = data['status']
        
        session = db.get_session()
        resume = session.query(Resume).filter(Resume.id == resume_id).first()
        
        if resume is None:
            session.close()
            return jsonify({
                'status': 'error',
                'message': f'Resume with ID {resume_id} not found'
            }), 404
        
        resume.status = new_status
        if 'metadata' in data:
            resume.metadata = data['metadata']
        
        session.commit()
        session.close()
        
        return jsonify({
            'status': 'success',
            'message': f'Resume status updated to {new_status}'
        })
    except Exception as e:
        logger.error(f"Error updating resume {resume_id} status: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error updating resume status',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)