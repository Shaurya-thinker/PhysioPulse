import cv2
import json
import os
from mediapipe.python.solutions.pose import Pose, PoseLandmark

# CONFIG
FRAME_SKIP = 5  # Process every 5th frame

def extract_pose_landmarks(video_path, output_json_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # For timestamp calculation
    frame_id = 0
    results_data = []

    with Pose(static_image_mode=False) as pose:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame_id += 1
            if frame_id % FRAME_SKIP != 0:
                continue

            timestamp_sec = round(frame_id / fps, 2)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            pose_landmarks = getattr(results, "pose_landmarks", None)
            if pose_landmarks:
                lm = getattr(pose_landmarks, "landmark", None)
                if not lm:
                    continue

                frame_landmarks = {
                    "frame": frame_id,
                    "timestamp_sec": timestamp_sec,
                    "landmarks": [
                        {
                            "id": idx,
                            "name": PoseLandmark(idx).name,
                            "x": lm[idx].x,
                            "y": lm[idx].y,
                            "z": lm[idx].z,
                            "visibility": lm[idx].visibility
                        }
                        for idx in range(len(lm))
                    ]
                }

                results_data.append(frame_landmarks)

    cap.release()

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w") as f:
        json.dump(results_data, f, indent=2)

    print(f"✅ Landmarks saved to {output_json_path}")
    return output_json_path


if __name__ == "__main__":
    video_path = "input_videos/sample.mp4"
    output_path = "output_data/sample_landmarks.json"
    extract_pose_landmarks(video_path, output_path)
