"""
Enhanced video analysis pipeline for PhysioPulse telerehabilitation system.
"""
import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import uuid
import json

from src.pose_detector import PoseDetector
from src.pose_scorer import PoseScorer
from src.config import settings
from src.models import AnalysisSummary, ExerciseType
from src.utils import (
    logger, 
    save_json_file, 
    ensure_directory_exists, 
    calculate_processing_time,
    get_file_size_mb,
    cleanup_temp_files
)

class VideoAnalyzer:
    """Enhanced video analysis class with comprehensive pipeline."""
    
    def __init__(self):
        """Initialize video analyzer."""
        self.pose_detector = PoseDetector(
            min_detection_confidence=settings.POSE_CONFIDENCE_THRESHOLD,
            min_tracking_confidence=settings.POSE_TRACKING_CONFIDENCE
        )
        self.pose_scorer = PoseScorer()
        logger.info("Video analyzer initialized")
    
    def run_pipeline(self, 
                    video_path: str, 
                    output_dir: str,
                    exercise_type: str = "arm_extension",
                    patient_id: Optional[str] = None,
                    session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Run complete video analysis pipeline.
        
        Args:
            video_path: Path to input video file
            output_dir: Output directory for results
            exercise_type: Type of exercise to analyze
            patient_id: Patient identifier
            session_id: Session identifier
            
        Returns:
            Dictionary containing analysis results and file paths
        """
        start_time = datetime.now()
        analysis_id = str(uuid.uuid4())
        
        try:
            logger.info(f"Starting analysis pipeline for video: {video_path}")
            logger.info(f"Exercise type: {exercise_type}")
            logger.info(f"Analysis ID: {analysis_id}")
            
            # Validate input
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Create output directory
            ensure_directory_exists(output_dir)
            
            # Generate output file paths
            landmarks_path = os.path.join(output_dir, f"{analysis_id}_landmarks.json")
            scores_path = os.path.join(output_dir, f"{analysis_id}_scores.json")
            summary_path = os.path.join(output_dir, f"{analysis_id}_summary.json")
            
            # Step 1: Extract pose landmarks
            logger.info("Step 1: Extracting pose landmarks...")
            self.pose_detector.extract_pose_landmarks(video_path, landmarks_path)
            
            # Step 2: Score poses
            logger.info("Step 2: Scoring poses...")
            self.pose_scorer.score_from_landmarks(landmarks_path, scores_path, exercise_type)
            
            # Step 3: Generate analysis summary
            logger.info("Step 3: Generating analysis summary...")
            summary = self._generate_analysis_summary(
                landmarks_path, scores_path, video_path, exercise_type, analysis_id
            )
            
            # Save summary
            save_json_file(summary.dict(), summary_path)
            
            # Calculate processing time
            processing_time = calculate_processing_time(start_time)
            
            # Prepare results
            results = {
                "analysis_id": analysis_id,
                "status": "completed",
                "processing_time": processing_time,
                "exercise_type": exercise_type,
                "patient_id": patient_id,
                "session_id": session_id,
                "files": {
                    "landmarks_file": landmarks_path,
                    "scores_file": scores_path,
                    "summary_file": summary_path
                },
                "summary": summary.dict()
            }
            
            logger.info(f"Analysis pipeline completed successfully in {processing_time:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"❌ Analysis pipeline failed: {str(e)}")
            
            # Clean up any partial files
            temp_files = [
                os.path.join(output_dir, f"{analysis_id}_landmarks.json"),
                os.path.join(output_dir, f"{analysis_id}_scores.json"),
                os.path.join(output_dir, f"{analysis_id}_summary.json")
            ]
            cleanup_temp_files(temp_files)
            
            raise RuntimeError(f"Analysis pipeline failed: {str(e)}")
    
    def _generate_analysis_summary(self, 
                                 landmarks_path: str, 
                                 scores_path: str,
                                 video_path: str,
                                 exercise_type: str,
                                 analysis_id: str) -> AnalysisSummary:
        """
        Generate comprehensive analysis summary.
        
        Args:
            landmarks_path: Path to landmarks file
            scores_path: Path to scores file
            video_path: Path to original video
            exercise_type: Type of exercise analyzed
            analysis_id: Analysis identifier
            
        Returns:
            Analysis summary object
        """
        try:
            # Load landmarks and scores data
            with open(landmarks_path, 'r', encoding='utf-8') as f:
                landmarks_data = json.load(f)
            
            with open(scores_path, 'r', encoding='utf-8') as f:
                scores_data = json.load(f)
            
            # Calculate statistics
            total_frames = len(landmarks_data)
            frames_with_pose = len(scores_data)
            detection_rate = frames_with_pose / total_frames if total_frames > 0 else 0.0
            
            # Calculate exercise duration
            if landmarks_data:
                exercise_duration = landmarks_data[-1]["timestamp_sec"] - landmarks_data[0]["timestamp_sec"]
            else:
                exercise_duration = 0.0
            
            # Calculate score statistics
            all_scores = []
            for frame_score in scores_data:
                for joint_name, joint_data in frame_score.items():
                    if isinstance(joint_data, dict) and "score" in joint_data:
                        all_scores.append(joint_data["score"])
            
            if all_scores:
                average_score = sum(all_scores) / len(all_scores)
                best_score = max(all_scores)
                worst_score = min(all_scores)
            else:
                average_score = 0.0
                best_score = 0
                worst_score = 0
            
            # Get video file size
            video_size_mb = get_file_size_mb(video_path)
            
            return AnalysisSummary(
                average_score=average_score,
                best_score=best_score,
                worst_score=worst_score,
                total_frames=total_frames,
                frames_with_pose=frames_with_pose,
                detection_rate=detection_rate,
                exercise_duration=exercise_duration
            )
            
        except Exception as e:
            logger.error(f"Error generating analysis summary: {str(e)}")
            return AnalysisSummary(
                average_score=0.0,
                best_score=0,
                worst_score=0,
                total_frames=0,
                frames_with_pose=0,
                detection_rate=0.0,
                exercise_duration=0.0
            )
    
    def validate_video(self, video_path: str) -> Dict[str, Any]:
        """
        Validate video file for analysis.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Validation results
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "video_info": {}
        }
        
        try:
            # Check file exists
            if not os.path.exists(video_path):
                validation_result["valid"] = False
                validation_result["errors"].append("Video file not found")
                return validation_result
            
            # Check file size
            file_size_mb = get_file_size_mb(video_path)
            validation_result["video_info"]["file_size_mb"] = file_size_mb
            
            if file_size_mb > settings.MAX_VIDEO_SIZE_MB:
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"File size ({file_size_mb:.1f}MB) exceeds limit ({settings.MAX_VIDEO_SIZE_MB}MB)"
                )
            
            # Check file extension
            file_extension = Path(video_path).suffix.lower()
            validation_result["video_info"]["file_extension"] = file_extension
            
            if file_extension not in settings.SUPPORTED_VIDEO_FORMATS:
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"Unsupported file format: {file_extension}"
                )
            
            # Try to open video with OpenCV
            import cv2
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                validation_result["valid"] = False
                validation_result["errors"].append("Cannot open video file with OpenCV")
            else:
                # Get video properties
                fps = cap.get(cv2.CAP_PROP_FPS)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                duration = total_frames / fps if fps > 0 else 0
                
                validation_result["video_info"].update({
                    "fps": fps,
                    "total_frames": total_frames,
                    "width": width,
                    "height": height,
                    "duration_seconds": duration
                })
                
                # Check video duration
                if duration < 1.0:
                    validation_result["warnings"].append("Video duration is very short (< 1 second)")
                elif duration > 300:  # 5 minutes
                    validation_result["warnings"].append("Video duration is very long (> 5 minutes)")
                
                # Check resolution
                if width < 320 or height < 240:
                    validation_result["warnings"].append("Video resolution is very low")
                
                cap.release()
            
        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Validation error: {str(e)}")
        
        return validation_result


def run_pipeline(video_path: str, output_dir: str) -> Dict[str, str]:
    """
    Legacy function for backward compatibility.
    
    Args:
        video_path: Path to input video file
        output_dir: Output directory for results
        
    Returns:
        Dictionary with file paths
    """
    analyzer = VideoAnalyzer()
    results = analyzer.run_pipeline(video_path, output_dir)
    
    return {
        "landmarks_file": results["files"]["landmarks_file"],
        "scores_file": results["files"]["scores_file"]
    }


if __name__ == "__main__":
    # Test the video analyzer
    video_path = "input_videos/sample.mp4"
    output_dir = "output_data"
    
    try:
        analyzer = VideoAnalyzer()
        
        # Validate video first
        validation = analyzer.validate_video(video_path)
        print(f"Video validation: {'Valid' if validation['valid'] else 'Invalid'}")
        
        if validation["errors"]:
            print("Errors:", validation["errors"])
        
        if validation["warnings"]:
            print("Warnings:", validation["warnings"])
        
        if validation["valid"]:
            # Run analysis
            results = analyzer.run_pipeline(video_path, output_dir)
            print("Video analysis test completed successfully")
            print(f"Analysis ID: {results['analysis_id']}")
            print(f"Processing time: {results['processing_time']:.2f}s")
        else:
            print("❌ Video validation failed, skipping analysis")
            
    except Exception as e:
        print(f"❌ Video analysis test failed: {str(e)}")
