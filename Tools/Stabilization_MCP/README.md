# Stabilization MCP

Removes handheld camera shake using ffmpeg's two-pass `vidstabdetect`/
`vidstabtransform` filters, with a light unsharp pass to compensate for the
slight blur stabilization introduces.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH built with `libvidstab` support
(the standard Gyan.FFmpeg Windows builds include it).

## Tools

- `stabilize_video` - two-pass stabilization with configurable smoothing,
  shakiness estimate, and optional zoom-in to crop residual edge wobble.
