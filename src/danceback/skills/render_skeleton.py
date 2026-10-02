import json
import os
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

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
    with open(json_path, "r", encoding="utf-8") as f:
        pose_data = json.load(f)

    frames = sorted(pose_data.keys(), key=lambda k: int(k.split("_")[1]))
    frames = frames[:max_frames]
    print(f"共 {len(frames)} 帧待渲染")

    tmp_dir = "tmp_frames"
    os.makedirs(tmp_dir, exist_ok=True)

    for i, fk in enumerate(frames):
        landmarks = pose_data[fk]

        # 关键：先创建 fig 和 ax
        fig = plt.figure(figsize=(5, 5))
        fig.patch.set_facecolor('black')          # fig 存在了，可以设背景
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('black')                 # ax 创建之后才能设背景
        ax.grid(False)                            # 关掉网格

        # 取坐标
        xs = [c[0] for c in landmarks.values()]
        ys = [c[2] for c in landmarks.values()]
        zs = [-c[1] for c in landmarks.values()]
        ax.scatter(xs, ys, zs, c='cyan', s=20)

        # 画连线
        for a, b in POSE_CONNECTIONS:
            if a in landmarks and b in landmarks:
                x1, z1, y1 = landmarks[a]
                x2, z2, y2 = landmarks[b]
                ax.plot([x1, x2], [y1, y2], [-z1, -z2], c='lime', linewidth=2)

        # 固定坐标轴范围
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.8, 0.8)
        ax.set_zlim(-0.8, 0.8)
        ax.set_box_aspect([1, 1, 1])

        # 隐藏坐标轴数字和刻度，让画面更干净
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_zlabel('')
        ax.set_title(f"Back View - Frame {i}", color='white')
        ax.view_init(elev=15, azim=-70)

        img_path = os.path.join(tmp_dir, f"frame_{i:05d}.png")
        plt.savefig(img_path, dpi=70, facecolor='black')
        plt.close(fig)

        if i % 10 == 0:
            print(f"已渲染 {i}/{len(frames)}")

    # 合成视频
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