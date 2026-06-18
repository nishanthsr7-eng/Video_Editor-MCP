# Highlight Reel MCP

Automatically picks the most "exciting" segments of a video based on audio loudness
(RMS) and transient/impact strength (onset detection via librosa), then concatenates
them in chronological order into a highlight reel / trailer.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH.

## Tools

- `generate_highlights` - select and concatenate the highest-scoring segments of a
  video into a short highlight reel.
