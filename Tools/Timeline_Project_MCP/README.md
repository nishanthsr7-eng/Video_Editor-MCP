# Timeline Project MCP

Maintains a JSON "project" describing a sequence of clips (with optional
transitions between them) plus a set of overlay layers (images, stickers,
transparent video, text renders, etc.) positioned in time and space, then
renders the whole project to a single output video in one pass via ffmpeg.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH.

## Tools

- `create_project` - create a new project JSON file with canvas size/fps.
- `add_clip` - append a clip (video or image) to the main timeline, optionally
  with a transition from the previous clip.
- `remove_clip` - remove a clip by index.
- `add_overlay` - add an overlay layer (image/sticker/transparent video) with
  position, size, opacity and a time window.
- `remove_overlay` - remove an overlay by index.
- `get_project` - inspect the project contents and estimated total duration.
- `render_project` - render the full project (normalize clips, apply
  transitions, composite overlays) to a final mp4.
