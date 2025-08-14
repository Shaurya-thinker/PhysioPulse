"""
Data models for PhysioPulse telerehabilitation system.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ExerciseType(str, Enum):
    """Supported exercise types."""
    ARM_EXTENSION = "arm_extension"
    SQUAT = "squat"
    SHOULDER_PRESS = "shoulder_press"

class AnalysisStatus(str, Enum):
    """Analysis processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class LandmarkPoint(BaseModel):
    """Individual pose landmark point."""
    id: int = Field(..., description="Landmark ID")
    name: str = Field(..., description="Landmark name")
    x: float = Field(..., description="X coordinate (0-1)")
    y: float = Field(..., description="Y coordinate (0-1)")
    z: float = Field(..., description="Z coordinate (depth)")
    visibility: float = Field(..., description="Visibility confidence (0-1)")

class FrameLandmarks(BaseModel):
    """Pose landmarks for a single frame."""
    frame: int = Field(..., description="Frame number")
    timestamp_sec: float = Field(..., description="Timestamp in seconds")
    landmarks: List[LandmarkPoint] = Field(..., description="List of pose landmarks")

class JointScore(BaseModel):
    """Score for a specific joint."""
    angle: float = Field(..., description="Calculated joint angle")
    score: int = Field(..., description="Score (0-100)")
    feedback: str = Field(..., description="Feedback message")
    confidence: float = Field(..., description="Detection confidence")

class FrameScore(BaseModel):
    """Score for a single frame."""
    frame: int = Field(..., description="Frame number")
    timestamp_sec: float = Field(..., description="Timestamp in seconds")
    left_arm: Optional[JointScore] = Field(None, description="Left arm score")
    right_arm: Optional[JointScore] = Field(None, description="Right arm score")
    left_knee: Optional[JointScore] = Field(None, description="Left knee score")
    right_knee: Optional[JointScore] = Field(None, description="Right knee score")
    left_shoulder: Optional[JointScore] = Field(None, description="Left shoulder score")
    right_shoulder: Optional[JointScore] = Field(None, description="Right shoulder score")

class AnalysisRequest(BaseModel):
    """Request model for video analysis."""
    exercise_type: ExerciseType = Field(..., description="Type of exercise to analyze")
    patient_id: Optional[str] = Field(None, description="Patient identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")

class AnalysisResponse(BaseModel):
    """Response model for video analysis."""
    status: str = Field(..., description="Analysis status")
    analysis_id: str = Field(..., description="Unique analysis identifier")
    video_file: str = Field(..., description="Original video filename")
    exercise_type: ExerciseType = Field(..., description="Analyzed exercise type")
    processing_time: float = Field(..., description="Processing time in seconds")
    total_frames: int = Field(..., description="Total frames processed")
    scores: List[FrameScore] = Field(..., description="Frame-by-frame scores")
    landmarks: List[FrameLandmarks] = Field(..., description="Frame-by-frame landmarks")
    summary: Dict[str, Any] = Field(..., description="Analysis summary")
    created_at: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")

class AnalysisSummary(BaseModel):
    """Summary statistics for analysis."""
    average_score: float = Field(..., description="Average score across all frames")
    best_score: int = Field(..., description="Best single frame score")
    worst_score: int = Field(..., description="Worst single frame score")
    total_frames: int = Field(..., description="Total frames analyzed")
    frames_with_pose: int = Field(..., description="Frames where pose was detected")
    detection_rate: float = Field(..., description="Pose detection rate")
    exercise_duration: float = Field(..., description="Exercise duration in seconds")

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")

class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    uptime: float = Field(..., description="Service uptime in seconds")

class PatientInfo(BaseModel):
    """Patient information model."""
    patient_id: str = Field(..., description="Unique patient identifier")
    name: Optional[str] = Field(None, description="Patient name")
    age: Optional[int] = Field(None, description="Patient age")
    condition: Optional[str] = Field(None, description="Medical condition")
    created_at: datetime = Field(default_factory=datetime.now, description="Record creation time")

class SessionInfo(BaseModel):
    """Session information model."""
    session_id: str = Field(..., description="Unique session identifier")
    patient_id: str = Field(..., description="Patient identifier")
    exercise_type: ExerciseType = Field(..., description="Exercise type")
    start_time: datetime = Field(..., description="Session start time")
    end_time: Optional[datetime] = Field(None, description="Session end time")
    status: str = Field(..., description="Session status")

class ProgressReport(BaseModel):
    """Progress report for a patient."""
    patient_id: str = Field(..., description="Patient identifier")
    period_start: datetime = Field(..., description="Report period start")
    period_end: datetime = Field(..., description="Report period end")
    total_sessions: int = Field(..., description="Total sessions in period")
    average_score: float = Field(..., description="Average score across sessions")
    improvement_rate: float = Field(..., description="Score improvement rate")
    exercises_completed: Dict[str, int] = Field(..., description="Exercises completed by type")
    recommendations: List[str] = Field(..., description="Recommendations for improvement")
