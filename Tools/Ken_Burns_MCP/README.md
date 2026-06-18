# Ken Burns MCP

Turns a still image into a video clip with a slow zoom/pan ("Ken Burns")
effect, via ffmpeg's `zoompan` filter.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH.

## Tools

- `create_ken_burns` - generate a zoom/pan video from a still image, with
  configurable start/end zoom level, pan direction, resolution, fps and
  duration.
