# DanceBack Agent

把正面舞蹈视频转成**背面跟练视角**，并通过 MCP / Function Calling 集成到 AI Agent。

## 项目目标
- 主线：正面视频 → 3D 姿态 → 绕 Y 轴旋转 180° → 背面数字人渲染
- 降级：左右镜像，快速跟练（fallback）

## 当前版本 v0.0.1
- [x] 项目骨架
- [x] 占位 Skill：镜像（仅用于验证 pipeline）
- [ ] MCP Server（v0.1）
- [ ] 2D 姿态提取（v0.1）
- [ ] 3D 姿态提升（v0.2）
- [ ] 背面数字人渲染（v0.3）

## 快速开始
python src\danceback\skills\mirror.py dance.mp4 practice.mp4

## 路线图
| 版本 | 目标 |
|---|---|
| v0.0.1 | 骨架 + 镜像占位 |
| v0.1 | MCP Server + 2D 姿态提取 |
| v0.2 | 3D 姿态提升 |
| v0.3 | 背面数字人渲染 |

## 说明
- `back_view` 是主线，`mirror` 仅作 fallback。
- 单目正面视频无法真实恢复背面细节，背面为推断结果。
- 请勿上传未授权舞蹈视频和音乐。

## 许可证
MIT
