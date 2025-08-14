"""
Configuration settings for PhysioPulse telerehabilitation system.
"""
import os
from pathlib import Path
from typing import Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Settings
    API_TITLE: str = "PhysioPulse Telerehabilitation API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered telerehabilitation system for pose analysis and exercise scoring"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # File Storage Settings
    UPLOAD_DIR: str = Field(default="input_videos", env="UPLOAD_DIR")
    OUTPUT_DIR: str = Field(default="output_data", env="OUTPUT_DIR")
    TEMP_DIR: str = Field(default="temp", env="TEMP_DIR")
    
    # Video Processing Settings
    MAX_VIDEO_SIZE_MB: int = Field(default=100, env="MAX_VIDEO_SIZE_MB")
    FRAME_SKIP: int = Field(default=5, env="FRAME_SKIP")
    SUPPORTED_VIDEO_FORMATS: list[str] = Field(
        default=[".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mkv"],
        env="SUPPORTED_VIDEO_FORMATS"
    )
    
    # Pose Detection Settings
    POSE_CONFIDENCE_THRESHOLD: float = Field(default=0.5, env="POSE_CONFIDENCE_THRESHOLD")
    POSE_TRACKING_CONFIDENCE: float = Field(default=0.5, env="POSE_TRACKING_CONFIDENCE")
    
    # Scoring Settings
    PERFECT_ANGLE_RANGE: tuple[int, int] = Field(default=(150, 180), env="PERFECT_ANGLE_RANGE")
    GOOD_ANGLE_RANGE: tuple[int, int] = Field(default=(120, 149), env="GOOD_ANGLE_RANGE")
    PERFECT_SCORE: int = Field(default=100, env="PERFECT_SCORE")
    GOOD_SCORE: int = Field(default=75, env="GOOD_SCORE")
    NEEDS_IMPROVEMENT_SCORE: int = Field(default=50, env="NEEDS_IMPROVEMENT_SCORE")
    
    # Firebase Settings (for future integration)
    FIREBASE_PROJECT_ID: str = Field(default="", env="FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY_ID: str = Field(default="", env="FIREBASE_PRIVATE_KEY_ID")
    FIREBASE_PRIVATE_KEY: str = Field(default="", env="FIREBASE_PRIVATE_KEY")
    FIREBASE_CLIENT_EMAIL: str = Field(default="", env="FIREBASE_CLIENT_EMAIL")
    FIREBASE_CLIENT_ID: str = Field(default="", env="FIREBASE_CLIENT_ID")
    
    # Logging Settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="physiopulse.log", env="LOG_FILE")
    
    # Security Settings
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Performance Settings
    MAX_CONCURRENT_ANALYSES: int = Field(default=5, env="MAX_CONCURRENT_ANALYSES")
    ANALYSIS_TIMEOUT_SECONDS: int = Field(default=300, env="ANALYSIS_TIMEOUT_SECONDS")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_directories(self) -> Dict[str, str]:
        """Get all required directories."""
        base_dir = Path.cwd()
        return {
            "upload": str(base_dir / self.UPLOAD_DIR),
            "output": str(base_dir / self.OUTPUT_DIR),
            "temp": str(base_dir / self.TEMP_DIR),
            "logs": str(base_dir / "logs")
        }
    
    def create_directories(self) -> None:
        """Create all required directories."""
        directories = self.get_directories()
        for dir_path in directories.values():
            Path(dir_path).mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()

# Exercise configurations
EXERCISE_CONFIGS = {
    "arm_extension": {
        "name": "Arm Extension Exercise",
        "description": "Extend arms fully for proper form",
        "target_joints": ["left_elbow", "right_elbow"],
        "perfect_angle_range": (150, 180),
        "good_angle_range": (120, 149),
        "feedback_messages": {
            "perfect": "Perfect arm extension!",
            "good": "Almost there, extend a bit more",
            "needs_improvement": "Bend your arm more for proper form"
        }
    },
    "squat": {
        "name": "Squat Exercise",
        "description": "Perform proper squat form",
        "target_joints": ["left_knee", "right_knee"],
        "perfect_angle_range": (90, 120),
        "good_angle_range": (70, 89),
        "feedback_messages": {
            "perfect": "Perfect squat depth!",
            "good": "Go a bit deeper for better form",
            "needs_improvement": "Squat deeper for proper form"
        }
    },
    "shoulder_press": {
        "name": "Shoulder Press Exercise",
        "description": "Press weights overhead with proper form",
        "target_joints": ["left_shoulder", "right_shoulder"],
        "perfect_angle_range": (160, 180),
        "good_angle_range": (140, 159),
        "feedback_messages": {
            "perfect": "Perfect shoulder press!",
            "good": "Almost fully extended",
            "needs_improvement": "Extend your arms more"
        }
    }
}

# MediaPipe pose landmarks mapping
POSE_LANDMARKS = {
    "nose": 0,
    "left_eye_inner": 1,
    "left_eye": 2,
    "left_eye_outer": 3,
    "right_eye_inner": 4,
    "right_eye": 5,
    "right_eye_outer": 6,
    "left_ear": 7,
    "right_ear": 8,
    "mouth_left": 9,
    "mouth_right": 10,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_pinky": 17,
    "right_pinky": 18,
    "left_index": 19,
    "right_index": 20,
    "left_thumb": 21,
    "right_thumb": 22,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
    "left_heel": 29,
    "right_heel": 30,
    "left_foot_index": 31,
    "right_foot_index": 32
}
