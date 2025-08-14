"""
Enhanced pose scoring module for PhysioPulse telerehabilitation system.
"""
import json
import math
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import numpy as np

# Try to import mediapipe, fallback to mock if not available
try:
    from mediapipe.python.solutions.pose import PoseLandmark
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logging.warning("MediaPipe not available. Using mock implementation for testing.")

from src.config import settings, EXERCISE_CONFIGS, POSE_LANDMARKS
from src.models import FrameScore, JointScore, AnalysisSummary
from src.utils import logger, save_json_file, ensure_directory_exists

class PoseScorer:
    """Enhanced pose scoring class with multiple exercise support."""
    
    def __init__(self):
        """Initialize pose scorer."""
        logger.info("Pose scorer initialized")
    
    def score_from_landmarks(self, 
                           landmarks_json_path: str, 
                           output_json_path: str,
                           exercise_type: str = "arm_extension") -> str:
        """
        Score poses from landmarks data.
        
        Args:
            landmarks_json_path: Path to landmarks JSON file
            output_json_path: Path to output scores JSON file
            exercise_type: Type of exercise to score
            
        Returns:
            Path to saved scores file
        """
        try:
            # Load landmarks data
            with open(landmarks_json_path, 'r', encoding='utf-8') as f:
                frames_data = json.load(f)
            
            if not frames_data:
                raise ValueError("No landmarks data found")
            
            logger.info(f"Scoring {len(frames_data)} frames for exercise: {exercise_type}")
            
            # Get exercise configuration
            exercise_config = EXERCISE_CONFIGS.get(exercise_type)
            if not exercise_config:
                raise ValueError(f"Unsupported exercise type: {exercise_type}")
            
            # Score each frame
            scores = []
            for frame_data in frames_data:
                frame_score = self._score_frame(frame_data, exercise_config)
                if frame_score:
                    scores.append(frame_score)
            
            if not scores:
                raise RuntimeError("No valid scores generated")
            
            # Save scores
            ensure_directory_exists(os.path.dirname(output_json_path))
            save_json_file(scores, output_json_path)
            
            logger.info(f"Scoring complete. Results saved to {output_json_path}")
            logger.info(f"Processed {len(scores)} scored frames")
            
            return output_json_path
            
        except Exception as e:
            logger.error(f"Error during pose scoring: {str(e)}")
            raise RuntimeError(f"Pose scoring failed: {str(e)}")
    
    def _score_frame(self, frame_data: Dict[str, Any], exercise_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Score a single frame.
        
        Args:
            frame_data: Frame landmarks data
            exercise_config: Exercise configuration
            
        Returns:
            Frame score data or None if scoring failed
        """
        try:
            landmarks = frame_data["landmarks"]
            
            # Extract joint positions
            joint_positions = self._extract_joint_positions(landmarks)
            
            # Calculate scores based on exercise type
            frame_score = {
                "frame": frame_data["frame"],
                "timestamp_sec": frame_data.get("timestamp_sec", 0.0)
            }
            
            # Score different joints based on exercise type
            if exercise_config["name"] == "Arm Extension Exercise":
                frame_score.update(self._score_arm_extension(joint_positions, exercise_config))
            elif exercise_config["name"] == "Squat Exercise":
                frame_score.update(self._score_squat(joint_positions, exercise_config))
            elif exercise_config["name"] == "Shoulder Press Exercise":
                frame_score.update(self._score_shoulder_press(joint_positions, exercise_config))
            else:
                # Default to arm extension
                frame_score.update(self._score_arm_extension(joint_positions, exercise_config))
            
            return frame_score
            
        except Exception as e:
            logger.warning(f"Error scoring frame {frame_data.get('frame', 'unknown')}: {str(e)}")
            return None
    
    def _extract_joint_positions(self, landmarks: List[Dict[str, Any]]) -> Dict[str, Tuple[float, float]]:
        """
        Extract joint positions from landmarks.
        
        Args:
            landmarks: List of landmark data
            
        Returns:
            Dictionary of joint positions
        """
        joint_positions = {}
        
        # Map landmark indices to joint names
        if MEDIAPIPE_AVAILABLE:
            joint_mapping = {
                "left_shoulder": PoseLandmark.LEFT_SHOULDER.value,
                "right_shoulder": PoseLandmark.RIGHT_SHOULDER.value,
                "left_elbow": PoseLandmark.LEFT_ELBOW.value,
                "right_elbow": PoseLandmark.RIGHT_ELBOW.value,
                "left_wrist": PoseLandmark.LEFT_WRIST.value,
                "right_wrist": PoseLandmark.RIGHT_WRIST.value,
                "left_hip": PoseLandmark.LEFT_HIP.value,
                "right_hip": PoseLandmark.RIGHT_HIP.value,
                "left_knee": PoseLandmark.LEFT_KNEE.value,
                "right_knee": PoseLandmark.RIGHT_KNEE.value,
                "left_ankle": PoseLandmark.LEFT_ANKLE.value,
                "right_ankle": PoseLandmark.RIGHT_ANKLE.value
            }
        else:
            # Hardcoded MediaPipe landmark indices for testing
            joint_mapping = {
                "left_shoulder": 11,
                "right_shoulder": 12,
                "left_elbow": 13,
                "right_elbow": 14,
                "left_wrist": 15,
                "right_wrist": 16,
                "left_hip": 23,
                "right_hip": 24,
                "left_knee": 25,
                "right_knee": 26,
                "left_ankle": 27,
                "right_ankle": 28
            }
        
        for joint_name, landmark_idx in joint_mapping.items():
            if landmark_idx < len(landmarks):
                landmark = landmarks[landmark_idx]
                joint_positions[joint_name] = (landmark["x"], landmark["y"])
        
        return joint_positions
    
    def _score_arm_extension(self, joint_positions: Dict[str, Tuple[float, float]], 
                           exercise_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score arm extension exercise.
        
        Args:
            joint_positions: Joint positions dictionary
            exercise_config: Exercise configuration
            
        Returns:
            Arm extension scores
        """
        scores = {}
        
        # Score left arm
        if all(joint in joint_positions for joint in ["left_shoulder", "left_elbow", "left_wrist"]):
            left_angle = self._calculate_angle(
                joint_positions["left_shoulder"],
                joint_positions["left_elbow"],
                joint_positions["left_wrist"]
            )
            left_score = self._calculate_joint_score(left_angle, exercise_config)
            scores["left_arm"] = left_score
        
        # Score right arm
        if all(joint in joint_positions for joint in ["right_shoulder", "right_elbow", "right_wrist"]):
            right_angle = self._calculate_angle(
                joint_positions["right_shoulder"],
                joint_positions["right_elbow"],
                joint_positions["right_wrist"]
            )
            right_score = self._calculate_joint_score(right_angle, exercise_config)
            scores["right_arm"] = right_score
        
        return scores
    
    def _score_squat(self, joint_positions: Dict[str, Tuple[float, float]], 
                    exercise_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score squat exercise.
        
        Args:
            joint_positions: Joint positions dictionary
            exercise_config: Exercise configuration
            
        Returns:
            Squat scores
        """
        scores = {}
        
        # Score left knee
        if all(joint in joint_positions for joint in ["left_hip", "left_knee", "left_ankle"]):
            left_angle = self._calculate_angle(
                joint_positions["left_hip"],
                joint_positions["left_knee"],
                joint_positions["left_ankle"]
            )
            left_score = self._calculate_joint_score(left_angle, exercise_config)
            scores["left_knee"] = left_score
        
        # Score right knee
        if all(joint in joint_positions for joint in ["right_hip", "right_knee", "right_ankle"]):
            right_angle = self._calculate_angle(
                joint_positions["right_hip"],
                joint_positions["right_knee"],
                joint_positions["right_ankle"]
            )
            right_score = self._calculate_joint_score(right_angle, exercise_config)
            scores["right_knee"] = right_score
        
        return scores
    
    def _score_shoulder_press(self, joint_positions: Dict[str, Tuple[float, float]], 
                            exercise_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score shoulder press exercise.
        
        Args:
            joint_positions: Joint positions dictionary
            exercise_config: Exercise configuration
            
        Returns:
            Shoulder press scores
        """
        scores = {}
        
        # Score left shoulder (hip to shoulder to elbow)
        if all(joint in joint_positions for joint in ["left_hip", "left_shoulder", "left_elbow"]):
            left_angle = self._calculate_angle(
                joint_positions["left_hip"],
                joint_positions["left_shoulder"],
                joint_positions["left_elbow"]
            )
            left_score = self._calculate_joint_score(left_angle, exercise_config)
            scores["left_shoulder"] = left_score
        
        # Score right shoulder (hip to shoulder to elbow)
        if all(joint in joint_positions for joint in ["right_hip", "right_shoulder", "right_elbow"]):
            right_angle = self._calculate_angle(
                joint_positions["right_hip"],
                joint_positions["right_shoulder"],
                joint_positions["right_elbow"]
            )
            right_score = self._calculate_joint_score(right_angle, exercise_config)
            scores["right_shoulder"] = right_score
        
        return scores
    
    def _calculate_angle(self, a: Tuple[float, float], b: Tuple[float, float], 
                        c: Tuple[float, float]) -> float:
        """
        Calculate angle between three points.
        
        Args:
            a: First point (x, y)
            b: Middle point (x, y)
            c: Third point (x, y)
            
        Returns:
            Angle in degrees
        """
        try:
            # Convert to numpy arrays for easier calculation
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)
            
            # Calculate vectors
            ba = a - b
            bc = c - b
            
            # Calculate angle
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # Clamp to valid range
            angle = np.arccos(cosine_angle)
            
            # Convert to degrees
            angle_degrees = np.degrees(angle)
            
            return float(angle_degrees)
            
        except Exception as e:
            logger.warning(f"Error calculating angle: {str(e)}")
            return 0.0
    
    def _calculate_joint_score(self, angle: float, exercise_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate score for a joint based on angle.
        
        Args:
            angle: Joint angle in degrees
            exercise_config: Exercise configuration
            
        Returns:
            Joint score data
        """
        perfect_range = exercise_config["perfect_angle_range"]
        good_range = exercise_config["good_angle_range"]
        feedback_messages = exercise_config["feedback_messages"]
        
        # Determine score and feedback
        if perfect_range[0] <= angle <= perfect_range[1]:
            score = settings.PERFECT_SCORE
            feedback = feedback_messages["perfect"]
        elif good_range[0] <= angle <= good_range[1]:
            score = settings.GOOD_SCORE
            feedback = feedback_messages["good"]
        else:
            score = settings.NEEDS_IMPROVEMENT_SCORE
            feedback = feedback_messages["needs_improvement"]
        
        return {
            "angle": round(angle, 2),
            "score": score,
            "feedback": feedback,
            "confidence": 1.0  # Could be enhanced with visibility scores
        }
    
    def generate_analysis_summary(self, scores: List[Dict[str, Any]]) -> AnalysisSummary:
        """
        Generate analysis summary from scores.
        
        Args:
            scores: List of frame scores
            
        Returns:
            Analysis summary
        """
        if not scores:
            return AnalysisSummary(
                average_score=0.0,
                best_score=0,
                worst_score=0,
                total_frames=0,
                frames_with_pose=0,
                detection_rate=0.0,
                exercise_duration=0.0
            )
        
        # Calculate statistics
        all_scores = []
        for frame_score in scores:
            for joint_name, joint_data in frame_score.items():
                if isinstance(joint_data, dict) and "score" in joint_data:
                    all_scores.append(joint_data["score"])
        
        if not all_scores:
            return AnalysisSummary(
                average_score=0.0,
                best_score=0,
                worst_score=0,
                total_frames=len(scores),
                frames_with_pose=0,
                detection_rate=0.0,
                exercise_duration=scores[-1]["timestamp_sec"] - scores[0]["timestamp_sec"]
            )
        
        return AnalysisSummary(
            average_score=float(np.mean(all_scores)),
            best_score=int(np.max(all_scores)),
            worst_score=int(np.min(all_scores)),
            total_frames=len(scores),
            frames_with_pose=len(scores),
            detection_rate=1.0,
            exercise_duration=scores[-1]["timestamp_sec"] - scores[0]["timestamp_sec"]
        )


def score_from_landmarks(landmarks_json_path: str, output_json_path: str) -> str:
    """
    Legacy function for backward compatibility.
    
    Args:
        landmarks_json_path: Path to landmarks JSON file
        output_json_path: Path to output scores JSON file
        
    Returns:
        Path to saved scores file
    """
    scorer = PoseScorer()
    return scorer.score_from_landmarks(landmarks_json_path, output_json_path)


if __name__ == "__main__":
    # Test the pose scorer
    landmarks_path = "output_data/sample_landmarks.json"
    scores_path = "output_data/sample_scores.json"
    
    try:
        score_from_landmarks(landmarks_path, scores_path)
        print("Pose scoring test completed successfully")
    except Exception as e:
        print(f"❌ Pose scoring test failed: {str(e)}")
