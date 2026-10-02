# DanceBack Agent

把正面舞蹈视频转成**背面跟练视角**，并通过 MCP / Function Calling 集成到 AI Agent。

## 项目目标
- 主线：正面视频 → 3D 姿态 → 绕 Y 轴旋转 180° → 背面数字人渲染
- 降级：左右镜像，快速跟练（fallback）

## 当前版本 v0.3

- [x] 项目骨架
- [x] 占位 Skill：镜像（fallback）
- [x] MCP Server 骨架（适配 mcp 2.x）
- [x] 2D 姿态提取（MediaPipe Tasks API）
- [x] 3D 姿态提取（MediaPipe World Landmarks）
- [x] 3D 骨架绕 Y 轴旋转 180°（背面视角）
- [x] 3D 骨架渲染成视频
- [x] 合并原视频音轨
- [ ] 高精度 3D 姿态提升（MotionBERT，v0.4）
- [ ] 保留原舞者外观的背面渲染（v0.5）

## 快速开始

### 1. 安装依赖
```bash
pip install -e .
```

### 2. 下载模型文件
运行姿态提取前，请先下载 MediaPipe 模型：

```powershell
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task" -OutFile "pose_landmarker_full.task"
```

### 3. 镜像视频（fallback 模式）
```bash
python src\danceback\skills\mirror.py dance.mp4 practice.mp4
```

### 4. 提取 2D 姿态
```bash
python src\danceback\skills\extract_pose.py
生成 pose_preview.jpg。
```

### 5. 启动 MCP Server
```bash
python src\danceback\agent\mcp_server.py
```

## 目录结构
```text
danceback-agent/
├── src/danceback/
│   ├── skills/
│   │   ├── mirror.py          # fallback：左右镜像
│   │   ├── back_view.py       # 主线：背面视角（占位）
│   │   └── extract_pose.py    # 2D 姿态提取
│   └── agent/
│       └── mcp_server.py      # MCP Server
├── pyproject.toml
└── README.md
```

## 路线图

| 版本 | 目标 | 状态 |
|---|---|---|
| v0.0.1 | 骨架 + 镜像占位 | ✅ |
| v0.1 | MCP Server + 2D 姿态提取 | ✅ |
| v0.2 | 3D 姿态提取 + 旋转 + 渲染 | ✅ |
| v0.3 | 音轨合并 + 视觉美化 | ✅ |
| v0.4 | MotionBERT 高精度 3D 姿态 | 📅 |
| v0.5 | 保留原舞者外观的背面渲染 | 📅 |

## 说明
- back_view 是主线，mirror 仅作 fallback。

- 单目正面视频无法真实恢复背面细节，背面为推断结果。

- pose_landmarker_full.task 和 pose_preview.jpg 已在 .gitignore 中忽略，不会上传。

- 请勿上传未授权舞蹈视频和音乐。

## 许可证
MIT
