# Color Match MCP

Analyzes the color profile (RGB mean/std from sampled frames) of a video and matches
one video's overall brightness/contrast/tint to another via an ffmpeg `lutrgb`
linear transform.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH.

## Tools

- `get_color_profile` - returns RGB mean/std from sampled frames.
- `match_color` - matches a target video's color statistics to a reference video.
