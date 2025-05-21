# AI Resume Analyzer Backend

A Flask-based backend system for analyzing and extracting information from resume files.

## Features

- Upload and process PDF/DOCX resume files
- Extract and sanitize text from resumes
- Store resume data in SQLite database
- Rate limiting to prevent API abuse
- CORS support for cross-origin requests
- Health check endpoint for monitoring

## Setup and Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Set up environment variables (or modify the `.env` file):
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   UPLOAD_FOLDER=uploads
   DATABASE_URI=sqlite:///data.db
   MAX_CONTENT_LENGTH=10485760
   RATE_LIMIT_PER_MINUTE=10
   ```

4. Run the application:
   ```bash
   cd backend
   python app.py
   ```

## API Endpoints

### Health Check
```
GET /health
```
Checks if the API is running correctly.

### Upload Resume
```
POST /upload_resume
```
Upload a resume file (PDF or DOCX) for processing.

### Get All Resumes
```
GET /resumes
```
Retrieve a list of all uploaded resumes.

### Get Resume by ID
```
GET /resume/{id}
```
Retrieve details of a specific resume.

### Delete Resume
```
DELETE /resume/{id}
```
Delete a specific resume.

### Update Resume Status
```
PUT /resume/{id}/update_status
```
Update the status of a resume.

## Rate Limiting

API endpoints are rate-limited to 10 requests per minute per IP address.

## File Size Limit

The maximum file size for uploads is 10MB.

## Database

SQLite database with SQLAlchemy ORM:
- Table: `resumes`
  - `id`: Integer, primary key
  - `filename`: String, not null
  - `file_type`: String, not null
  - `upload_date`: DateTime, not null
  - `raw_text`: Text, not null
  - `status`: String, default 'pending'
  - `metadata`: JSON

## Directory Structure

```
backend/
├── app.py                   # Main Flask application
├── config.py                # Configuration settings
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── data.db                  # SQLite database
├── uploads/                 # Folder for uploaded files
├── models/                  # Database models
│   ├── __init__.py
│   └── resume.py            # Resume model
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── db.py                # Database utilities
│   ├── file_handlers.py     # File handling utilities
│   └── rate_limiter.py      # Rate limiting
└── templates/               # HTML templates
    └── index.html           # API documentation page
```