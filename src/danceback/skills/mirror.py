import subprocess
import sys

def mirror_video(input_path: str, output_path: str):
    """fallback 模式：水平镜像，用于快速跟练验证 pipeline。"""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", "hflip",
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"[mirror] 已生成: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python mirror.py 输入视频 输出视频")
        sys.exit(1)
    mirror_video(sys.argv[1], sys.argv[2])
