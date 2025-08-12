import json
import math
import os
from mediapipe.python.solutions.pose import PoseLandmark

def calculate_angle(a, b, c):
    ang = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) -
        math.atan2(a[1] - b[1], a[0] - b[0])
    )
    return abs(ang) if abs(ang) <= 180 else 360 - abs(ang)

def score_from_landmarks(landmarks_json_path: str, output_json_path: str):
    with open(landmarks_json_path, 'r') as f:
        frames_data = json.load(f)

    scores = []
    for frame_data in frames_data:
        lm = frame_data["landmarks"]

        # Extract key points for left and right arm
        left_shoulder = (lm[PoseLandmark.LEFT_SHOULDER.value]["x"], lm[PoseLandmark.LEFT_SHOULDER.value]["y"])
        left_elbow = (lm[PoseLandmark.LEFT_ELBOW.value]["x"], lm[PoseLandmark.LEFT_ELBOW.value]["y"])
        left_wrist = (lm[PoseLandmark.LEFT_WRIST.value]["x"], lm[PoseLandmark.LEFT_WRIST.value]["y"])

        right_shoulder = (lm[PoseLandmark.RIGHT_SHOULDER.value]["x"], lm[PoseLandmark.RIGHT_SHOULDER.value]["y"])
        right_elbow = (lm[PoseLandmark.RIGHT_ELBOW.value]["x"], lm[PoseLandmark.RIGHT_ELBOW.value]["y"])
        right_wrist = (lm[PoseLandmark.RIGHT_WRIST.value]["x"], lm[PoseLandmark.RIGHT_WRIST.value]["y"])

        # Calculate angles
        left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Scoring logic
        def get_score(angle):
            if 150 <= angle <= 180:
                return 100, "Perfect extension"
            elif 120 <= angle < 150:
                return 75, "Almost there"
            else:
                return 50, "Needs improvement"

        left_score, left_feedback = get_score(left_elbow_angle)
        right_score, right_feedback = get_score(right_elbow_angle)

        scores.append({
            "frame": frame_data["frame"],
            "timestamp_sec": frame_data.get("timestamp_sec", None),
            "left_arm": {
                "angle": left_elbow_angle,
                "score": left_score,
                "feedback": left_feedback
            },
            "right_arm": {
                "angle": right_elbow_angle,
                "score": right_score,
                "feedback": right_feedback
            }
        })

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w') as f:
        json.dump(scores, f, indent=2)

    print(f"✅ Scoring complete. Results saved to {output_json_path}")
    return output_json_path

if __name__ == "__main__":
    score_from_landmarks("output_data/sample_landmarks.json", "output_data/sample_scores.json")
