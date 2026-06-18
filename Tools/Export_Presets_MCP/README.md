# Export Presets MCP

One-call export to social-platform-ready specs (resolution, bitrate, fps, aspect
ratio) for YouTube, YouTube Shorts, TikTok, Instagram (Reels/Post/Story), Twitter/X,
and Facebook.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH.

## Tools

- `list_platform_presets` - list available platform presets and their specs.
- `export_for_platform` - re-encode a video to a platform preset, with `crop` or
  `pad` handling for aspect-ratio mismatches.
