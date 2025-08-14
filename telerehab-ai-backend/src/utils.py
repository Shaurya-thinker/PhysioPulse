"""
Utility functions for PhysioPulse telerehabilitation system.
"""
import os
import logging
import json
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import mimetypes
from fastapi import HTTPException, UploadFile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('physiopulse.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration constants
ALLOWED_VIDEO_TYPES = {
    'video/mp4', 'video/avi', 'video/mov', 'video/wmv', 
    'video/flv', 'video/webm', 'video/mkv'
}
MAX_VIDEO_SIZE_MB = 100
SUPPORTED_VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'}

def validate_video_file(file: UploadFile) -> Tuple[bool, str]:
    """
    Validate uploaded video file.
    
    Args:
        file: Uploaded file object
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > MAX_VIDEO_SIZE_MB * 1024 * 1024:
        return False, f"File size exceeds {MAX_VIDEO_SIZE_MB}MB limit"
    
    # Check file extension
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in SUPPORTED_VIDEO_EXTENSIONS:
        return False, f"Unsupported file format. Supported: {', '.join(SUPPORTED_VIDEO_EXTENSIONS)}"
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type not in ALLOWED_VIDEO_TYPES:
        return False, f"Invalid MIME type: {mime_type}"
    
    return True, ""

def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename with UUID.
    
    Args:
        original_filename: Original file name
        
    Returns:
        Unique filename with UUID prefix
    """
    file_extension = Path(original_filename).suffix
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{file_extension}"

def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory_path: Path to directory
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def save_uploaded_file(file: UploadFile, destination_path: str) -> str:
    """
    Save uploaded file to destination.
    
    Args:
        file: Uploaded file object
        destination_path: Destination file path
        
    Returns:
        Saved file path
    """
    try:
        ensure_directory_exists(os.path.dirname(destination_path))
        
        with open(destination_path, "wb") as buffer:
            # Read file in chunks to handle large files
            chunk_size = 1024 * 1024  # 1MB chunks
            while chunk := file.file.read(chunk_size):
                buffer.write(chunk)
        
        logger.info(f"File saved successfully: {destination_path}")
        return destination_path
        
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")

def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load JSON file safely.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Loaded JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="Analysis results not found")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid analysis data format")

def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data to JSON file safely.
    
    Args:
        data: Data to save
        file_path: Destination file path
    """
    try:
        ensure_directory_exists(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"JSON data saved to: {file_path}")
    except Exception as e:
        logger.error(f"Error saving JSON file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save analysis results")

def calculate_processing_time(start_time: datetime) -> float:
    """
    Calculate processing time in seconds.
    
    Args:
        start_time: Start time
        
    Returns:
        Processing time in seconds
    """
    return (datetime.now() - start_time).total_seconds()

def format_timestamp(timestamp: float) -> str:
    """
    Format timestamp for display.
    
    Args:
        timestamp: Timestamp in seconds
        
    Returns:
        Formatted timestamp string
    """
    return f"{timestamp:.2f}s"

def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except OSError:
        return 0.0

def cleanup_temp_files(file_paths: list[str]) -> None:
    """
    Clean up temporary files.
    
    Args:
        file_paths: List of file paths to delete
    """
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except OSError as e:
            logger.warning(f"Failed to clean up file {file_path}: {str(e)}")
