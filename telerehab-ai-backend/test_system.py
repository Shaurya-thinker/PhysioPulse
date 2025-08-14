#!/usr/bin/env python3
"""
Comprehensive system test for PhysioPulse.
This script tests all major components of the system.
"""
import os
import sys
import json
import tempfile
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import src.config
        import src.models
        import src.utils
        import src.pose_detector
        import src.pose_scorer
        import src.video_analyzer
        import src.api
        print("All imports successful")
        return True
    except ImportError as e:
        print(f"Import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("\n🔍 Testing configuration...")
    
    try:
        from src.config import settings, EXERCISE_CONFIGS, POSE_LANDMARKS
        
        # Test settings
        assert settings.API_TITLE == "PhysioPulse Telerehabilitation API"
        assert settings.PORT == 8000
        assert settings.MAX_VIDEO_SIZE_MB == 100
        
        # Test exercise configs
        assert "arm_extension" in EXERCISE_CONFIGS
        assert "squat" in EXERCISE_CONFIGS
        assert "shoulder_press" in EXERCISE_CONFIGS
        
        # Test landmarks
        assert len(POSE_LANDMARKS) == 33
        
        print("Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"Configuration test failed: {e}")
        return False

def test_utils():
    """Test utility functions."""
    print("\n🔍 Testing utility functions...")
    
    try:
        from src.utils import (
            generate_unique_filename, 
            ensure_directory_exists,
            calculate_processing_time,
            format_timestamp
        )
        from datetime import datetime
        
        # Test filename generation
        filename = generate_unique_filename("test.mp4")
        assert filename.endswith(".mp4")
        assert len(filename) > 10
        
        # Test directory creation
        test_dir = "test_temp_dir"
        ensure_directory_exists(test_dir)
        assert os.path.exists(test_dir)
        os.rmdir(test_dir)
        
        # Test time functions
        start_time = datetime.now()
        time.sleep(0.1)
        processing_time = calculate_processing_time(start_time)
        assert processing_time > 0
        
        formatted = format_timestamp(processing_time)
        assert "s" in formatted
        
        print("Utility functions work correctly")
        return True
    except Exception as e:
        print(f"Utility test failed: {e}")
        return False

def test_models():
    """Test data models."""
    print("\n🔍 Testing data models...")
    
    try:
        from src.models import (
            ExerciseType, 
            AnalysisStatus, 
            LandmarkPoint,
            FrameLandmarks,
            JointScore,
            FrameScore
        )
        
        # Test enums
        assert ExerciseType.ARM_EXTENSION == "arm_extension"
        assert AnalysisStatus.COMPLETED == "completed"
        
        # Test models
        landmark = LandmarkPoint(
            id=0,
            name="NOSE",
            x=0.5,
            y=0.5,
            z=0.0,
            visibility=0.9
        )
        assert landmark.id == 0
        assert landmark.name == "NOSE"
        
        joint_score = JointScore(
            angle=165.0,
            score=100,
            feedback="Perfect!",
            confidence=0.95
        )
        assert joint_score.score == 100
        assert joint_score.angle == 165.0
        
        print("Data models work correctly")
        return True
    except Exception as e:
        print(f"Models test failed: {e}")
        return False

def test_pose_detector():
    """Test pose detector initialization."""
    print("\n🔍 Testing pose detector...")
    
    try:
        from src.pose_detector import PoseDetector
        
        # Test initialization
        detector = PoseDetector(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        assert detector.min_detection_confidence == 0.5
        assert detector.min_tracking_confidence == 0.5
        
        print("Pose detector initialized successfully")
        return True
    except Exception as e:
        print(f"Pose detector test failed: {e}")
        return False

def test_pose_scorer():
    """Test pose scorer initialization."""
    print("\n🔍 Testing pose scorer...")
    
    try:
        from src.pose_scorer import PoseScorer
        
        # Test initialization
        scorer = PoseScorer()
        
        # Test angle calculation
        import numpy as np
        from src.pose_scorer import PoseScorer
        
        scorer = PoseScorer()
        
        # Test angle calculation with known values
        a = (0, 0)
        b = (1, 0)
        c = (1, 1)
        
        angle = scorer._calculate_angle(a, b, c)
        assert 0 <= angle <= 180
        
        print("Pose scorer initialized successfully")
        return True
    except Exception as e:
        print(f"Pose scorer test failed: {e}")
        return False

def test_video_analyzer():
    """Test video analyzer initialization."""
    print("\n🔍 Testing video analyzer...")
    
    try:
        from src.video_analyzer import VideoAnalyzer
        
        # Test initialization
        analyzer = VideoAnalyzer()
        
        # Test validation with non-existent file
        validation = analyzer.validate_video("nonexistent.mp4")
        assert not validation["valid"]
        assert "Video file not found" in validation["errors"]
        
        print("Video analyzer initialized successfully")
        return True
    except Exception as e:
        print(f"Video analyzer test failed: {e}")
        return False

def test_api_initialization():
    """Test API initialization."""
    print("\n🔍 Testing API initialization...")
    
    try:
        from src.api import app
        
        # Test that app is created
        assert app is not None
        assert hasattr(app, 'routes')
        
        print("API initialized successfully")
        return True
    except Exception as e:
        print(f"API test failed: {e}")
        return False

def test_file_operations():
    """Test file operations."""
    print("\n🔍 Testing file operations...")
    
    try:
        from src.utils import save_json_file, load_json_file, ensure_directory_exists
        
        # Test JSON operations
        test_data = {"test": "data", "number": 42}
        test_file = "test_output.json"
        
        # Save and load JSON
        save_json_file(test_data, test_file)
        loaded_data = load_json_file(test_file)
        
        assert loaded_data == test_data
        
        # Cleanup
        os.remove(test_file)
        
        print("File operations work correctly")
        return True
    except Exception as e:
        print(f"File operations test failed: {e}")
        return False

def test_end_to_end_pipeline():
    """Test the complete pipeline with mock data."""
    print("\n🔍 Testing end-to-end pipeline...")
    
    try:
        from src.video_analyzer import VideoAnalyzer
        from src.utils import save_json_file
        
        # Create mock landmarks data with all 33 MediaPipe landmarks
        landmarks = []
        for i in range(33):
            landmark = {
                "id": i,
                "name": f"LANDMARK_{i}",
                "x": 0.5,
                "y": 0.5,
                "z": 0.0,
                "visibility": 0.9
            }
            landmarks.append(landmark)
        
        # Set specific positions for arm extension joints
        landmarks[11] = {"id": 11, "name": "LEFT_SHOULDER", "x": 0.3, "y": 0.5, "z": 0.0, "visibility": 0.9}
        landmarks[13] = {"id": 13, "name": "LEFT_ELBOW", "x": 0.4, "y": 0.6, "z": 0.0, "visibility": 0.9}
        landmarks[15] = {"id": 15, "name": "LEFT_WRIST", "x": 0.5, "y": 0.7, "z": 0.0, "visibility": 0.9}
        landmarks[12] = {"id": 12, "name": "RIGHT_SHOULDER", "x": 0.7, "y": 0.5, "z": 0.0, "visibility": 0.9}
        landmarks[14] = {"id": 14, "name": "RIGHT_ELBOW", "x": 0.6, "y": 0.6, "z": 0.0, "visibility": 0.9}
        landmarks[16] = {"id": 16, "name": "RIGHT_WRIST", "x": 0.5, "y": 0.7, "z": 0.0, "visibility": 0.9}
        
        mock_landmarks = [
            {
                "frame": 1,
                "timestamp_sec": 0.0,
                "landmarks": landmarks
            }
        ]
        
        # Save mock landmarks
        landmarks_file = "test_landmarks.json"
        save_json_file(mock_landmarks, landmarks_file)
        
        # Test scoring
        from src.pose_scorer import PoseScorer
        scorer = PoseScorer()
        
        scores_file = "test_scores.json"
        scorer.score_from_landmarks(landmarks_file, scores_file, "arm_extension")
        
        # Verify scores were created
        assert os.path.exists(scores_file)
        
        # Load and verify scores
        with open(scores_file, 'r') as f:
            scores = json.load(f)
        
        assert len(scores) > 0
        assert "left_arm" in scores[0]
        
        # Cleanup
        os.remove(landmarks_file)
        os.remove(scores_file)
        
        print("End-to-end pipeline works correctly")
        return True
    except Exception as e:
        print(f"End-to-end pipeline test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting PhysioPulse System Tests\n")
    
    tests = [
        test_imports,
        test_configuration,
        test_utils,
        test_models,
        test_pose_detector,
        test_pose_scorer,
        test_video_analyzer,
        test_api_initialization,
        test_file_operations,
        test_end_to_end_pipeline
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test {test.__name__} crashed: {e}")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! System is ready to use.")
        return True
    else:
        print("Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
