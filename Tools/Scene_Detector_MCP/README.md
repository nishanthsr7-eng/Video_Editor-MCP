# Scene Detector MCP

Detects shot/scene-change points in a video (PySceneDetect's content-aware detector) and
can split a video into per-scene clips via ffmpeg.

## Setup

```
uv sync
```

Requires `ffmpeg` on PATH (used by `split_scenes`).

## Tools

- `detect_scenes` - list detected scene boundaries (start/end/duration per shot).
- `split_scenes` - split the video into one file per detected shot.
