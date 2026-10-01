from pathlib import Path

import pytest

from danceback.agent.mcp_server import convert_dance_video


def test_convert_dance_video_rejects_missing_input(tmp_path):
    missing = tmp_path / "missing.mp4"

    with pytest.raises(FileNotFoundError, match="Input video not found"):
        convert_dance_video(str(missing), str(tmp_path / "out.mp4"))


def test_convert_dance_video_rejects_unknown_mode(tmp_path):
    input_file = tmp_path / "input.mp4"
    input_file.write_bytes(b"fake video")

    with pytest.raises(ValueError, match="Unsupported mode"):
        convert_dance_video(str(input_file), str(tmp_path / "out.mp4"), mode="unknown")


def test_convert_dance_video_mirror_mode_calls_pipeline(monkeypatch, tmp_path):
    input_file = tmp_path / "input.mp4"
    input_file.write_bytes(b"fake video")
    captured = {}

    def fake_mirror_video(source_path: str, target_path: str):
        captured["source"] = source_path
        captured["target"] = target_path

    monkeypatch.setattr("danceback.agent.mcp_server.mirror_video", fake_mirror_video)

    result = convert_dance_video(str(input_file), str(tmp_path / "output.mp4"), mode=" mirror ")

    assert "镜像视频已生成" in result
    assert captured["source"] == str(input_file)
    assert captured["target"] == str(tmp_path / "output.mp4")
