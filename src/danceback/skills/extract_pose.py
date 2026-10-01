import cv2
import json
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import PoseLandmarker, PoseLandmarkerOptions, RunningMode
from mediapipe.tasks.python.core.base_options import BaseOptions
import numpy as np

# MediaPipe 33 个关键点的名称
LANDMARK_NAMES = [
    "nose", "left_eye_inner", "left_eye", "left_eye_outer",
    "right_eye_inner", "right_eye", "right_eye_outer",
    "left_ear", "right_ear", "mouth_left", "mouth_right",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_pinky", "right_pinky",
    "left_index", "right_index", "left_thumb", "right_thumb",
    "left_hip", "right_hip", "left_knee", "right_knee",
    "left_ankle", "right_ankle", "left_heel", "right_heel",
    "left_foot_index", "right_foot_index"
]

def extract_pose_3d(video_path: str, output_json: str = "pose_3d.json"):
    """从视频中提取每一帧的 3D 姿态，保存为 JSON。"""
    base_options = BaseOptions(model_asset_path="pose_landmarker_full.task")
    options = PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=RunningMode.VIDEO,  # 注意：这里是 VIDEO
        num_poses=1,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
    )

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法打开视频")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"视频 FPS: {fps}, 总帧数: {total_frames}")

    pose_data = {}

    with PoseLandmarker.create_from_options(options) as landmarker:
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # 视频模式下需要传入时间戳（毫秒）
            timestamp_ms = int(frame_idx * 1000 / fps) if fps > 0 else frame_idx
            detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)

            if detection_result.pose_world_landmarks:
                landmarks = detection_result.pose_world_landmarks[0]
                frame_data = {}
                for idx, lm in enumerate(landmarks):
                    name = LANDMARK_NAMES[idx] if idx < len(LANDMARK_NAMES) else f"point_{idx}"
                    frame_data[name] = [float(lm.x), float(lm.y), float(lm.z)]
                pose_data[f"frame_{frame_idx}"] = frame_data

            frame_idx += 1

    cap.release()

    # 保存 JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(pose_data, f, indent=2, ensure_ascii=False)

    print(f"已提取 {len(pose_data)} 帧的 3D 姿态，保存至: {output_json}")


if __name__ == "__main__":
    extract_pose_3d("dance.mp4")