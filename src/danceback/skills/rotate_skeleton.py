import json

def rotate_3d_to_back(input_json: str = "pose_3d.json", output_json: str = "pose_3d_back.json"):
    """将 3D 姿态绕 Y 轴旋转 180 度，变成背面视角。"""
    with open(input_json, "r", encoding="utf-8") as f:
        pose_data = json.load(f)

    rotated_data = {}
    for frame_key, landmarks in pose_data.items():
        rotated_frame = {}
        for name, coords in landmarks.items():
            x, y, z = coords
            # 绕 Y 轴旋转 180 度：x 和 z 取反
            rotated_frame[name] = [-x, y, -z]
        rotated_data[frame_key] = rotated_frame

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(rotated_data, f, indent=2, ensure_ascii=False)

    print(f"已生成背面视角骨架数据: {output_json}")

if __name__ == "__main__":
    rotate_3d_to_back()