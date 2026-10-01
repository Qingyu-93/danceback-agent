import json
import os
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 无界面模式，防止弹窗
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# MediaPipe 33 个关键点的骨架连接关系
POSE_CONNECTIONS = [
    ("left_shoulder", "right_shoulder"),
    ("left_shoulder", "left_elbow"),
    ("right_shoulder", "right_elbow"),
    ("left_elbow", "left_wrist"),
    ("right_elbow", "right_wrist"),
    ("left_shoulder", "left_hip"),
    ("right_shoulder", "right_hip"),
    ("left_hip", "right_hip"),
    ("left_hip", "left_knee"),
    ("right_hip", "right_knee"),
    ("left_knee", "left_ankle"),
    ("right_knee", "right_ankle"),
    ("left_ankle", "left_heel"),
    ("right_ankle", "right_heel"),
    ("left_heel", "left_foot_index"),
    ("right_heel", "right_foot_index"),
]


def render_skeleton_video(
    json_path: str = "pose_3d_back.json",
    output_video: str = "skeleton_back.mp4",
    fps: int = 30,
    max_frames: int = 150,
):
    """把 3D 骨架 JSON 渲染成视频（骨架点连线）。"""
    with open(json_path, "r", encoding="utf-8") as f:
        pose_data = json.load(f)

    # 按帧号排序
    frames = sorted(pose_data.keys(), key=lambda k: int(k.split("_")[1]))
    frames = frames[:max_frames]  # 控制时长，先渲染前 150 帧
    print(f"共 {len(frames)} 帧待渲染")

    tmp_dir = "tmp_frames"
    os.makedirs(tmp_dir, exist_ok=True)

    # 固定坐标轴范围（MediaPipe 世界坐标约 ±1 米）
    axis_range = 1.2
    all_x, all_y, all_z = [], [], []
    for fk in frames:
        for coords in pose_data[fk].values():
            all_x.append(coords[0])
            all_y.append(coords[1])
            all_z.append(coords[2])

    x_range = (min(all_x) - 0.2, max(all_x) + 0.2)
    y_range = (min(all_y) - 0.2, max(all_y) + 0.2)
    z_range = (min(all_z) - 0.2, max(all_z) + 0.2)

    # 逐帧渲染
    for i, fk in enumerate(frames):
        landmarks = pose_data[fk]

        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection='3d')

        # 画关节点
        xs = [c[0] for c in landmarks.values()]
        ys = [c[2] for c in landmarks.values()]   # 用 MediaPipe 的 Z 当作前后深度
        zs = [-c[1] for c in landmarks.values()]  # 用 MediaPipe 的 Y 取反当作上下高度
        ax.scatter(xs, ys, zs, c='red', s=15)

        # 画连线
        for a, b in POSE_CONNECTIONS:
            if a in landmarks and b in landmarks:
                x1, z1, y1 = landmarks[a]
                x2, z2, y2 = landmarks[b]
                ax.plot([x1, x2], [y1, y2], [-z1, -z2], c='blue', linewidth=2)

        # 固定坐标轴范围，避免画面乱晃
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.8, 0.8)
        ax.set_zlim(-0.8, 0.8)
        ax.set_box_aspect([1, 1, 1])     # 防止比例失调导致人体拉长

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f"Back View - Frame {i}")
        ax.view_init(elev=15, azim=-70)  # 稍微抬高视角，换个角度，增强立体感  # 水平视线

        img_path = os.path.join(tmp_dir, f"frame_{i:05d}.png")
        plt.savefig(img_path, dpi=70)
        plt.close(fig)

        if i % 10 == 0:
            print(f"已渲染 {i}/{len(frames)}")

    # 用 OpenCV 合成视频
    first_img = cv2.imread(os.path.join(tmp_dir, "frame_00000.png"))
    height, width, _ = first_img.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for i in range(len(frames)):
        img_path = os.path.join(tmp_dir, f"frame_{i:05d}.png")
        img = cv2.imread(img_path)
        if img is not None:
            out.write(img)

    out.release()
    print(f"骨架视频已生成: {output_video}")


if __name__ == "__main__":
    render_skeleton_video()