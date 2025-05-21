"""
File handling utilities for parsing and extracting text from different file formats.
"""
import os
import re
import PyPDF2
from werkzeug.utils import secure_filename
from typing import Tuple, Optional
import docx

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, upload_folder: str) -> Tuple[bool, str]:
    """
    Save uploaded file to the specified folder.
    
    Args:
        file: The file object from request
        upload_folder: The folder to save the file
        
    Returns:
        Tuple containing success status and filename/error message
    """
    if file.filename == '':
        return False, "No file selected"
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    
    # If filename already exists, add timestamp to make it unique
    if os.path.exists(file_path):
        name, extension = os.path.splitext(filename)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{name}_{timestamp}{extension}"
        file_path = os.path.join(upload_folder, filename)
    
    try:
        file.save(file_path)
        return True, filename
    except Exception as e:
        return False, str(e)

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as string
    """
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        text = f"Error extracting PDF text: {str(e)}"
    return text

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text content from DOCX file.
    
    Args:
        file_path: Path to the DOCX file
        
    Returns:
        Extracted text as string
    """
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        text = f"Error extracting DOCX text: {str(e)}"
    return text

def get_file_extension(filename: str) -> str:
    """Get the file extension from filename."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ""

def extract_text(file_path: str, file_type: str) -> str:
    """
    Extract text based on file type.
    
    Args:
        file_path: Path to the file
        file_type: Type of the file (pdf, docx)
        
    Returns:
        Extracted text as string
    """
    if file_type == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_type == 'docx':
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file type"

def sanitize_text(text: str) -> str:
    """
    Sanitize extracted text.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s.\-,;:()\[\]{}\'\"?!@#$%^&*+=]', '', text)
    return text.strip()