# Compositor MCP

Composites multiple layers (images, transparent video/webm overlays, picture-in-picture
clips) onto a base video using a single ffmpeg `filter_complex` graph - position, scale,
opacity, time window and stacking order are all configurable per layer.

## Setup

```
uv sync
```

Requires `ffmpeg` and `ffprobe` on PATH.

## Tools

- `compose_layers` - stack N layers (images or videos, in back-to-front order) onto a
  base video, each with its own position, size, opacity, visible time range, and
  (for video layers) optional audio mixing.
