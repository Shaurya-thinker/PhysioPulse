"""
Tests for PhysioPulse API endpoints.
"""
import pytest
import json
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.api import app
from src.models import ExerciseType

client = TestClient(app)

# Test data
TEST_TOKEN = "test-token-123456789"
TEST_HEADERS = {"Authorization": f"Bearer {TEST_TOKEN}"}

@pytest.fixture
def mock_video_file():
    """Create a mock video file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        f.write(b"fake video content")
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def mock_analysis_results():
    """Mock analysis results."""
    return {
        "analysis_id": "test-analysis-123",
        "status": "completed",
        "processing_time": 5.2,
        "exercise_type": "arm_extension",
        "files": {
            "landmarks_file": "test_landmarks.json",
            "scores_file": "test_scores.json",
            "summary_file": "test_summary.json"
        },
        "summary": {
            "average_score": 85.5,
            "best_score": 100,
            "worst_score": 75,
            "total_frames": 100,
            "frames_with_pose": 95,
            "detection_rate": 0.95,
            "exercise_duration": 5.0
        }
    }

class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "uptime" in data

class TestAuthentication:
    """Test authentication requirements."""
    
    def test_analyze_without_auth(self):
        """Test that analysis endpoint requires authentication."""
        response = client.post("/analyze")
        assert response.status_code == 401
    
    def test_analysis_without_auth(self):
        """Test that getting analysis results requires authentication."""
        response = client.get("/analysis/test-id")
        assert response.status_code == 401
    
    def test_analyses_without_auth(self):
        """Test that listing analyses requires authentication."""
        response = client.get("/analyses")
        assert response.status_code == 401

class TestVideoAnalysis:
    """Test video analysis functionality."""
    
    @patch('src.api.video_analyzer.run_pipeline')
    @patch('src.api.save_uploaded_file')
    @patch('src.api.load_json_file')
    def test_analyze_video_success(self, mock_load_json, mock_save_file, mock_run_pipeline, mock_video_file, mock_analysis_results):
        """Test successful video analysis."""
        # Mock the pipeline
        mock_run_pipeline.return_value = mock_analysis_results
        
        # Mock file operations
        mock_save_file.return_value = mock_video_file
        mock_load_json.side_effect = [
            [{"frame": 1, "scores": {"left_arm": {"score": 100}}}],  # scores
            [{"frame": 1, "landmarks": []}],  # landmarks
            mock_analysis_results["summary"]  # summary
        ]
        
        with open(mock_video_file, 'rb') as f:
            response = client.post(
                "/analyze",
                headers=TEST_HEADERS,
                files={"video": ("test.mp4", f, "video/mp4")},
                data={"exercise_type": "arm_extension"}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert "analysis_id" in data
        assert data["exercise_type"] == "arm_extension"
    
    def test_analyze_invalid_file_type(self):
        """Test analysis with invalid file type."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"not a video file")
            f.flush()
            
            with open(f.name, 'rb') as file:
                response = client.post(
                    "/analyze",
                    headers=TEST_HEADERS,
                    files={"video": ("test.txt", file, "text/plain")}
                )
            
            os.unlink(f.name)
        
        assert response.status_code == 400
        assert "Unsupported file format" in response.json()["error"]
    
    def test_analyze_large_file(self):
        """Test analysis with file too large."""
        # Create a large file
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            # Write more than 100MB
            f.write(b"0" * (101 * 1024 * 1024))
            f.flush()
            
            with open(f.name, 'rb') as file:
                response = client.post(
                    "/analyze",
                    headers=TEST_HEADERS,
                    files={"video": ("large.mp4", file, "video/mp4")}
                )
            
            os.unlink(f.name)
        
        assert response.status_code == 400
        assert "File size exceeds" in response.json()["error"]

class TestAnalysisResults:
    """Test analysis results endpoints."""
    
    @patch('src.api.load_json_file')
    def test_get_analysis_results(self, mock_load_json):
        """Test getting analysis results."""
        # Mock the analysis results in memory
        from src.api import analysis_results
        analysis_results["test-analysis-123"] = {
            "results": {
                "analysis_id": "test-analysis-123",
                "files": {
                    "landmarks_file": "test_landmarks.json",
                    "scores_file": "test_scores.json",
                    "summary_file": "test_summary.json"
                }
            },
            "user_id": "demo_user",
            "created_at": "2023-01-01T00:00:00"
        }
        
        # Mock file loading
        mock_load_json.side_effect = [
            [{"frame": 1, "scores": {"left_arm": {"score": 100}}}],  # scores
            [{"frame": 1, "landmarks": []}],  # landmarks
            {"average_score": 85.5}  # summary
        ]
        
        response = client.get(
            "/analysis/test-analysis-123",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["analysis_id"] == "test-analysis-123"
        assert "scores" in data
        assert "landmarks" in data
    
    def test_get_nonexistent_analysis(self):
        """Test getting non-existent analysis."""
        response = client.get(
            "/analysis/nonexistent-id",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 404
        assert "Analysis not found" in response.json()["error"]
    
    def test_list_analyses(self):
        """Test listing analyses."""
        # Add some test analyses
        from src.api import analysis_results
        analysis_results["test-1"] = {
            "results": {"exercise_type": "arm_extension", "processing_time": 5.0, "status": "completed"},
            "user_id": "demo_user",
            "created_at": "2023-01-01T00:00:00"
        }
        analysis_results["test-2"] = {
            "results": {"exercise_type": "squat", "processing_time": 3.0, "status": "completed"},
            "user_id": "demo_user",
            "created_at": "2023-01-02T00:00:00"
        }
        
        response = client.get("/analyses", headers=TEST_HEADERS)
        
        assert response.status_code == 200
        data = response.json()
        assert "analyses" in data
        assert data["total"] >= 2
        assert len(data["analyses"]) >= 2

class TestPatientManagement:
    """Test patient management endpoints."""
    
    def test_create_patient(self):
        """Test creating a new patient."""
        patient_data = {
            "patient_id": "test-patient-123",
            "name": "John Doe",
            "age": 30,
            "condition": "Knee injury"
        }
        
        response = client.post(
            "/patients",
            headers=TEST_HEADERS,
            json=patient_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["patient_id"] == "test-patient-123"
        assert data["name"] == "John Doe"
    
    def test_get_patient(self):
        """Test getting patient information."""
        # First create a patient
        patient_data = {
            "patient_id": "test-patient-456",
            "name": "Jane Smith",
            "age": 25
        }
        
        client.post("/patients", headers=TEST_HEADERS, json=patient_data)
        
        # Then get the patient
        response = client.get(
            "/patients/test-patient-456",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["patient_id"] == "test-patient-456"
        assert data["name"] == "Jane Smith"
    
    def test_list_patients(self):
        """Test listing patients."""
        response = client.get("/patients", headers=TEST_HEADERS)
        
        assert response.status_code == 200
        data = response.json()
        assert "patients" in data
        assert "total" in data

class TestSessionManagement:
    """Test session management endpoints."""
    
    def test_create_session(self):
        """Test creating a new session."""
        session_data = {
            "session_id": "test-session-123",
            "patient_id": "test-patient-123",
            "exercise_type": "arm_extension",
            "start_time": "2023-01-01T10:00:00",
            "status": "active"
        }
        
        response = client.post(
            "/sessions",
            headers=TEST_HEADERS,
            json=session_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test-session-123"
        assert data["exercise_type"] == "arm_extension"
    
    def test_get_session(self):
        """Test getting session information."""
        # First create a session
        session_data = {
            "session_id": "test-session-456",
            "patient_id": "test-patient-123",
            "exercise_type": "squat",
            "start_time": "2023-01-01T11:00:00",
            "status": "completed"
        }
        
        client.post("/sessions", headers=TEST_HEADERS, json=session_data)
        
        # Then get the session
        response = client.get(
            "/sessions/test-session-456",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test-session-456"
        assert data["exercise_type"] == "squat"

class TestProgressReporting:
    """Test progress reporting endpoints."""
    
    def test_get_patient_progress(self):
        """Test getting patient progress report."""
        response = client.get(
            "/patients/test-patient-123/progress",
            headers=TEST_HEADERS
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["patient_id"] == "test-patient-123"
        assert "total_sessions" in data
        assert "average_score" in data
        assert "recommendations" in data

class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_token(self):
        """Test with invalid token."""
        response = client.get("/health", headers={"Authorization": "Bearer invalid"})
        assert response.status_code == 401
    
    def test_malformed_token(self):
        """Test with malformed token."""
        response = client.get("/health", headers={"Authorization": "Bearer 123"})
        assert response.status_code == 401
    
    def test_missing_token(self):
        """Test with missing token."""
        response = client.get("/analyses")
        assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__])
