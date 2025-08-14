"""
Enhanced pose detection module using MediaPipe for PhysioPulse.
"""
import cv2
import json
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import numpy as np

# Try to import mediapipe, fallback to mock if not available
try:
    from mediapipe.python.solutions.pose import Pose, PoseLandmark
    from mediapipe.python.solutions.drawing_utils import draw_landmarks
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logging.warning("MediaPipe not available. Using mock implementation for testing.")

from src.config import settings, POSE_LANDMARKS
from src.models import FrameLandmarks, LandmarkPoint
from src.utils import logger, save_json_file, ensure_directory_exists

class PoseDetector:
    """Enhanced pose detection class with error handling and configuration."""
    
    def __init__(self, 
                 static_image_mode: bool = False,
                 model_complexity: int = 1,
                 smooth_landmarks: bool = True,
                 enable_segmentation: bool = False,
                 smooth_segmentation: bool = True,
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize pose detector with MediaPipe.
        
        Args:
            static_image_mode: Whether to process static images
            model_complexity: Model complexity (0, 1, or 2)
            smooth_landmarks: Whether to smooth landmarks
            enable_segmentation: Whether to enable segmentation
            smooth_segmentation: Whether to smooth segmentation
            min_detection_confidence: Minimum detection confidence
            min_tracking_confidence: Minimum tracking confidence
        """
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        # Initialize MediaPipe Pose if available
        if MEDIAPIPE_AVAILABLE:
            self.pose = Pose(
                static_image_mode=static_image_mode,
                model_complexity=model_complexity,
                smooth_landmarks=smooth_landmarks,
                enable_segmentation=enable_segmentation,
                smooth_segmentation=smooth_segmentation,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence
            )
            logger.info("Pose detector initialized successfully with MediaPipe")
        else:
            self.pose = None
            logger.warning("Pose detector initialized with mock implementation (MediaPipe not available)")
    
    def extract_pose_landmarks(self, video_path: str, output_json_path: str) -> str:
        """
        Extract pose landmarks from video file.
        
        Args:
            video_path: Path to input video file
            output_json_path: Path to output JSON file
            
        Returns:
            Path to saved landmarks file
            
        Raises:
            FileNotFoundError: If video file doesn't exist
            ValueError: If video file is invalid
            RuntimeError: If pose detection fails
        """
        # Validate input file
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Open video capture
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {video_path}")
        
        try:
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            logger.info(f"Processing video: {video_path}")
            logger.info(f"Video properties: {width}x{height}, {fps}fps, {total_frames} frames")
            
            frame_id = 0
            processed_frames = 0
            results_data: List[Dict[str, Any]] = []
            
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break
                
                frame_id += 1
                
                # Skip frames based on configuration
                if frame_id % settings.FRAME_SKIP != 0:
                    continue
                
                timestamp_sec = round(frame_id / fps, 2)
                
                try:
                    if MEDIAPIPE_AVAILABLE and self.pose:
                        # Convert BGR to RGB
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        # Process frame with MediaPipe
                        results = self.pose.process(rgb_frame)
                        
                        pose_landmarks = getattr(results, "pose_landmarks", None)
                        if pose_landmarks:
                            lm = getattr(pose_landmarks, "landmark", None)
                            if lm and len(lm) > 0:
                                frame_landmarks = self._extract_frame_landmarks(
                                    frame_id, timestamp_sec, lm
                                )
                                results_data.append(frame_landmarks)
                                processed_frames += 1
                    else:
                        # Mock implementation for testing
                        frame_landmarks = self._generate_mock_landmarks(frame_id, timestamp_sec)
                        results_data.append(frame_landmarks)
                        processed_frames += 1
                    
                    # Log progress every 100 frames
                    if frame_id % 100 == 0:
                        logger.info(f"Processed {frame_id}/{total_frames} frames")
                        
                except Exception as e:
                    logger.warning(f"Error processing frame {frame_id}: {str(e)}")
                    continue
            
            # Save results
            if results_data:
                self._save_landmarks(results_data, output_json_path)
                logger.info(f"Landmarks extracted successfully: {processed_frames} frames processed")
                logger.info(f"Detection rate: {processed_frames / (total_frames // settings.FRAME_SKIP) * 100:.1f}%")
            else:
                raise RuntimeError("No pose landmarks detected in video")
            
            return output_json_path
            
        except Exception as e:
            logger.error(f"Error during pose detection: {str(e)}")
            raise RuntimeError(f"Pose detection failed: {str(e)}")
        
        finally:
            cap.release()
            if self.pose:
                self.pose.close()
    
    def _extract_frame_landmarks(self, frame_id: int, timestamp_sec: float, landmarks) -> Dict[str, Any]:
        """
        Extract landmarks for a single frame.
        
        Args:
            frame_id: Frame number
            timestamp_sec: Timestamp in seconds
            landmarks: MediaPipe landmarks object
            
        Returns:
            Frame landmarks dictionary
        """
        frame_landmarks = {
            "frame": frame_id,
            "timestamp_sec": timestamp_sec,
            "landmarks": []
        }
        
        for idx in range(len(landmarks)):
            landmark = landmarks[idx]
            
            # Get landmark name
            try:
                if MEDIAPIPE_AVAILABLE:
                    landmark_name = PoseLandmark(idx).name
                else:
                    landmark_name = f"LANDMARK_{idx}"
            except ValueError:
                landmark_name = f"LANDMARK_{idx}"
            
            landmark_data = {
                "id": idx,
                "name": landmark_name,
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility
            }
            
            frame_landmarks["landmarks"].append(landmark_data)
        
        return frame_landmarks
    
    def _save_landmarks(self, results_data: List[Dict[str, Any]], output_json_path: str) -> None:
        """
        Save landmarks data to JSON file.
        
        Args:
            results_data: List of frame landmarks
            output_json_path: Output file path
        """
        try:
            ensure_directory_exists(os.path.dirname(output_json_path))
            save_json_file(results_data, output_json_path)
            logger.info(f"Landmarks saved to: {output_json_path}")
        except Exception as e:
            logger.error(f"Failed to save landmarks: {str(e)}")
            raise RuntimeError(f"Failed to save landmarks: {str(e)}")
    
    def validate_landmarks(self, landmarks_data: List[Dict[str, Any]]) -> bool:
        """
        Validate extracted landmarks data.
        
        Args:
            landmarks_data: List of frame landmarks
            
        Returns:
            True if valid, False otherwise
        """
        if not landmarks_data:
            return False
        
        for frame_data in landmarks_data:
            if "frame" not in frame_data or "landmarks" not in frame_data:
                return False
            
            landmarks = frame_data["landmarks"]
            if not landmarks or len(landmarks) != 33:  # MediaPipe has 33 landmarks
                return False
            
            for landmark in landmarks:
                required_fields = ["id", "name", "x", "y", "z", "visibility"]
                if not all(field in landmark for field in required_fields):
                    return False
                
                # Validate coordinate ranges
                if not (0 <= landmark["x"] <= 1 and 0 <= landmark["y"] <= 1):
                    return False
                
                if not (0 <= landmark["visibility"] <= 1):
                    return False
        
        return True

    def _generate_mock_landmarks(self, frame_id: int, timestamp_sec: float) -> Dict[str, Any]:
        """
        Generate mock landmarks for testing when MediaPipe is not available.
        
        Args:
            frame_id: Frame number
            timestamp_sec: Timestamp in seconds
            
        Returns:
            Mock frame landmarks dictionary
        """
        frame_landmarks = {
            "frame": frame_id,
            "timestamp_sec": timestamp_sec,
            "landmarks": []
        }
        
        # Generate 33 mock landmarks (MediaPipe standard)
        for idx in range(33):
            # Create realistic mock data
            landmark_data = {
                "id": idx,
                "name": f"LANDMARK_{idx}",
                "x": 0.5 + 0.1 * np.sin(frame_id * 0.1 + idx * 0.2),  # Varying x position
                "y": 0.5 + 0.1 * np.cos(frame_id * 0.1 + idx * 0.2),  # Varying y position
                "z": 0.0,  # Fixed z position
                "visibility": 0.8 + 0.2 * np.sin(frame_id * 0.05 + idx * 0.1)  # Varying visibility
            }
            
            # Clamp values to valid ranges
            landmark_data["x"] = max(0.0, min(1.0, landmark_data["x"]))
            landmark_data["y"] = max(0.0, min(1.0, landmark_data["y"]))
            landmark_data["visibility"] = max(0.0, min(1.0, landmark_data["visibility"]))
            
            frame_landmarks["landmarks"].append(landmark_data)
        
        return frame_landmarks


def extract_pose_landmarks(video_path: str, output_json_path: str) -> str:
    """
    Legacy function for backward compatibility.
    
    Args:
        video_path: Path to input video file
        output_json_path: Path to output JSON file
        
    Returns:
        Path to saved landmarks file
    """
    detector = PoseDetector(
        min_detection_confidence=settings.POSE_CONFIDENCE_THRESHOLD,
        min_tracking_confidence=settings.POSE_TRACKING_CONFIDENCE
    )
    return detector.extract_pose_landmarks(video_path, output_json_path)


if __name__ == "__main__":
    # Test the pose detector
    video_path = "input_videos/sample.mp4"
    output_path = "output_data/sample_landmarks.json"
    
    try:
        extract_pose_landmarks(video_path, output_path)
        print("Pose detection test completed successfully")
    except Exception as e:
        print(f"❌ Pose detection test failed: {str(e)}")
