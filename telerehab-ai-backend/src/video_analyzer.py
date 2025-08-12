import os
from src.pose_detector import extract_pose_landmarks
from src.pose_scorer import score_from_landmarks


def run_pipeline(video_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    landmarks_path = os.path.join(output_dir, "landmarks.json")
    scores_path = os.path.join(output_dir, "scores.json")

    # Step 1: Extract landmarks
    extract_pose_landmarks(video_path, landmarks_path)

    # Step 2: Score poses
    score_from_landmarks(landmarks_path, scores_path)

    return {
        "landmarks_file": landmarks_path,
        "scores_file": scores_path
    }

if __name__ == "__main__":
    run_pipeline("input_videos/sample.mp4", "output_data")
