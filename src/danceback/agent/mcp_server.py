from mcp.server.mcpserver import MCPServer   
from danceback.skills.mirror import mirror_video

mcp = MCPServer("DanceBack")  

@mcp.tool()
def convert_dance_video(
    input_path: str,
    output_path: str = "output.mp4",
    mode: str = "mirror"
) -> str:
    """
    将正面舞蹈视频转换为跟练版本。
    mode:
      - mirror: 左右镜像（fallback，v0.0.1 可用）
      - back_view: 背面视角（主线，v0.3 实现）
    """
    if mode == "mirror":
        mirror_video(input_path, output_path)
        return f"镜像视频已生成: {output_path}"
    elif mode == "back_view":
        return "背面视角功能尚未实现，将在 v0.3 上线。"
    else:
        return f"未知模式: {mode}"

@mcp.tool()
def analyze_dance_pose(video_path: str) -> str:
    """提取舞蹈视频第一帧的人体骨骼，生成 pose_preview.jpg。"""
    from danceback.skills.extract_pose import extract_first_frame_pose
    extract_first_frame_pose(video_path)
    return "已生成骨骼预览图: pose_preview.jpg"

if __name__ == "__main__":
    mcp.run(transport="stdio")