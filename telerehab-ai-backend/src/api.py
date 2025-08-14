"""
Enhanced FastAPI application for PhysioPulse telerehabilitation system.
"""
import os
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

from src.config import settings
from src.models import (
    AnalysisResponse, AnalysisRequest, ErrorResponse, HealthCheckResponse,
    ExerciseType, AnalysisStatus, PatientInfo, SessionInfo, ProgressReport
)
from src.video_analyzer import VideoAnalyzer
from src.utils import (
    logger, validate_video_file, generate_unique_filename, save_uploaded_file,
    load_json_file, calculate_processing_time, get_file_size_mb
)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Initialize components
video_analyzer = VideoAnalyzer()

# Create required directories
settings.create_directories()

# In-memory storage for demo (replace with database in production)
analysis_results: Dict[str, Dict[str, Any]] = {}
patients: Dict[str, PatientInfo] = {}
sessions: Dict[str, SessionInfo] = {}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("🚀 PhysioPulse API starting up...")
    logger.info(f"API Version: {settings.API_VERSION}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"Upload Directory: {settings.UPLOAD_DIR}")
    logger.info(f"Output Directory: {settings.OUTPUT_DIR}")


# Dependency for authentication (simplified for demo)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from token (simplified authentication)."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # In production, validate JWT token here
    # For demo, accept any valid token format
    if not credentials.credentials or len(credentials.credentials) < 10:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    return {"user_id": "demo_user", "token": credentials.credentials}


# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        version=settings.API_VERSION,
        uptime=time.time()  # In production, track actual uptime
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to PhysioPulse Telerehabilitation API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Video analysis endpoint
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_video(
    video: UploadFile = File(...),
    exercise_type: ExerciseType = ExerciseType.ARM_EXTENSION,
    patient_id: Optional[str] = None,
    session_id: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Analyze uploaded video for pose detection and exercise scoring.
    
    Args:
        video: Video file to analyze
        exercise_type: Type of exercise to analyze
        patient_id: Patient identifier
        session_id: Session identifier
        current_user: Authenticated user
        
    Returns:
        Analysis results with scores and landmarks
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Starting video analysis for user: {current_user['user_id']}")
        logger.info(f"File: {video.filename}, Exercise: {exercise_type}")
        
        # Validate video file
        is_valid, error_message = validate_video_file(video)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Generate unique filename and save video
        unique_filename = generate_unique_filename(video.filename)
        video_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        try:
            save_uploaded_file(video, video_path)
        except Exception as e:
            logger.error(f"Failed to save uploaded file: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save uploaded file"
            )
        
        # Run analysis pipeline
        try:
            results = video_analyzer.run_pipeline(
                video_path=video_path,
                output_dir=settings.OUTPUT_DIR,
                exercise_type=exercise_type.value,
                patient_id=patient_id,
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"Analysis pipeline failed: {str(e)}")
            # Clean up uploaded file
            if os.path.exists(video_path):
                os.remove(video_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Analysis failed: {str(e)}"
            )
        
        # Load analysis results
        try:
            scores_data = load_json_file(results["files"]["scores_file"])
            landmarks_data = load_json_file(results["files"]["landmarks_file"])
            summary_data = load_json_file(results["files"]["summary_file"])
        except Exception as e:
            logger.error(f"Failed to load analysis results: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to load analysis results"
            )
        
        # Store results in memory (replace with database in production)
        analysis_results[results["analysis_id"]] = {
            "results": results,
            "user_id": current_user["user_id"],
            "created_at": datetime.now().isoformat()
        }
        
        # Calculate processing time
        processing_time = calculate_processing_time(start_time)
        
        # Prepare response
        response = AnalysisResponse(
            status="completed",
            analysis_id=results["analysis_id"],
            video_file=video.filename,
            exercise_type=exercise_type,
            processing_time=processing_time,
            total_frames=summary_data.get("total_frames", 0),
            scores=scores_data,
            landmarks=landmarks_data,
            summary=summary_data
        )
        
        logger.info(f"Analysis completed successfully in {processing_time:.2f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Get analysis results endpoint
@app.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_results(
    analysis_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get analysis results by ID.
    
    Args:
        analysis_id: Analysis identifier
        current_user: Authenticated user
        
    Returns:
        Analysis results
    """
    if analysis_id not in analysis_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Check if user has access to this analysis
    analysis_data = analysis_results[analysis_id]
    if analysis_data["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        results = analysis_data["results"]
        
        # Load current data from files
        scores_data = load_json_file(results["files"]["scores_file"])
        landmarks_data = load_json_file(results["files"]["landmarks_file"])
        summary_data = load_json_file(results["files"]["summary_file"])
        
        return AnalysisResponse(
            status="completed",
            analysis_id=analysis_id,
            video_file=results.get("video_file", "unknown"),
            exercise_type=ExerciseType(results.get("exercise_type", "arm_extension")),
            processing_time=results.get("processing_time", 0.0),
            total_frames=summary_data.get("total_frames", 0),
            scores=scores_data,
            landmarks=landmarks_data,
            summary=summary_data
        )
        
    except Exception as e:
        logger.error(f"Error loading analysis {analysis_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load analysis results"
        )


# List analyses endpoint
@app.get("/analyses")
async def list_analyses(
    current_user: Dict[str, Any] = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
    """
    List user's analyses.
    
    Args:
        current_user: Authenticated user
        limit: Maximum number of results
        offset: Number of results to skip
        
    Returns:
        List of analysis summaries
    """
    user_analyses = [
        {
            "analysis_id": analysis_id,
            "created_at": data["created_at"],
            "exercise_type": data["results"].get("exercise_type", "unknown"),
            "processing_time": data["results"].get("processing_time", 0.0),
            "status": data["results"].get("status", "unknown")
        }
        for analysis_id, data in analysis_results.items()
        if data["user_id"] == current_user["user_id"]
    ]
    
    # Sort by creation time (newest first)
    user_analyses.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Apply pagination
    paginated_analyses = user_analyses[offset:offset + limit]
    
    return {
        "analyses": paginated_analyses,
        "total": len(user_analyses),
        "limit": limit,
        "offset": offset
    }


# Download analysis files endpoint
@app.get("/analysis/{analysis_id}/download/{file_type}")
async def download_analysis_file(
    analysis_id: str,
    file_type: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Download analysis files (landmarks, scores, or summary).
    
    Args:
        analysis_id: Analysis identifier
        file_type: Type of file to download (landmarks, scores, summary)
        current_user: Authenticated user
        
    Returns:
        File download response
    """
    if analysis_id not in analysis_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Check access
    analysis_data = analysis_results[analysis_id]
    if analysis_data["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get file path
    file_mapping = {
        "landmarks": "landmarks_file",
        "scores": "scores_file",
        "summary": "summary_file"
    }
    
    if file_type not in file_mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Supported: {', '.join(file_mapping.keys())}"
        )
    
    file_path = analysis_data["results"]["files"][file_mapping[file_type]]
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return FileResponse(
        path=file_path,
        filename=f"{analysis_id}_{file_type}.json",
        media_type="application/json"
    )


# Patient management endpoints
@app.post("/patients", response_model=PatientInfo)
async def create_patient(
    patient: PatientInfo,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new patient."""
    if patient.patient_id in patients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient ID already exists"
        )
    
    patients[patient.patient_id] = patient
    logger.info(f"Created patient: {patient.patient_id}")
    
    return patient


@app.get("/patients/{patient_id}", response_model=PatientInfo)
async def get_patient(
    patient_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get patient information."""
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return patients[patient_id]


@app.get("/patients")
async def list_patients(
    current_user: Dict[str, Any] = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
    """List all patients."""
    patient_list = list(patients.values())
    paginated_patients = patient_list[offset:offset + limit]
    
    return {
        "patients": paginated_patients,
        "total": len(patient_list),
        "limit": limit,
        "offset": offset
    }


# Session management endpoints
@app.post("/sessions", response_model=SessionInfo)
async def create_session(
    session: SessionInfo,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new session."""
    if session.session_id in sessions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID already exists"
        )
    
    sessions[session.session_id] = session
    logger.info(f"Created session: {session.session_id}")
    
    return session


@app.get("/sessions/{session_id}", response_model=SessionInfo)
async def get_session(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get session information."""
    if session_id not in sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return sessions[session_id]


# Progress report endpoint
@app.get("/patients/{patient_id}/progress", response_model=ProgressReport)
async def get_patient_progress(
    patient_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get patient progress report."""
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # In a real implementation, calculate progress from database
    # For demo, return mock data
    return ProgressReport(
        patient_id=patient_id,
        period_start=datetime.now(),
        period_end=datetime.now(),
        total_sessions=5,
        average_score=85.5,
        improvement_rate=12.3,
        exercises_completed={"arm_extension": 3, "squat": 2},
        recommendations=["Continue with current exercises", "Focus on form improvement"]
    )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            timestamp=datetime.now()
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.DEBUG else None,
            timestamp=datetime.now()
        ).dict()
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
