# Chroma Key MCP

Green/blue-screen keying and background replacement via ffmpeg's `chromakey`
filter.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH with `libvpx-vp9` encoder support
(for alpha-channel webm output).

## Tools

- `remove_background` - key out a solid-color background, output a
  transparent-alpha webm (usable as a compositor/timeline overlay).
- `replace_background` - key out a solid-color background and composite the
  subject onto a new image or video background in one step.
