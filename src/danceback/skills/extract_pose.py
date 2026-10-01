import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import PoseLandmarker, PoseLandmarkerOptions, RunningMode
from mediapipe.tasks.python.core.base_options import BaseOptions
import numpy as np

def extract_first_frame_pose(video_path: str):
    # 1. 配置模型
    base_options = BaseOptions(model_asset_path="pose_landmarker_full.task")
    options = PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=RunningMode.IMAGE,  # 处理单张图片
        num_poses=1,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
    )

    # 2. 创建 PoseLandmarker 实例
    with PoseLandmarker.create_from_options(options) as landmarker:
        # 3. 读取视频第一帧
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("无法读取视频")
            return

        # 4. 转换为 MediaPipe Image 格式
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # 5. 执行姿态检测
        detection_result = landmarker.detect(mp_image)

        # 6. 在图像上绘制骨骼点
        if detection_result.pose_landmarks:
            for landmarks in detection_result.pose_landmarks:
                for lm in landmarks:
                    x = int(lm.x * frame.shape[1])
                    y = int(lm.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            cv2.imwrite("pose_preview.jpg", frame)
            print("已生成骨骼预览图: pose_preview.jpg")
        else:
            print("未检测到人体")

if __name__ == "__main__":
    extract_first_frame_pose("dance.mp4")