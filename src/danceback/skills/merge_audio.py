import subprocess

def merge_audio(video_path: str, audio_source: str, output_path: str = "output_with_audio.mp4"):
    """将原视频的音轨合并到无声音的骨架视频里。"""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_source,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"已合并音频: {output_path}")

if __name__ == "__main__":
    merge_audio("skeleton_back.mp4", "dance.mp4")