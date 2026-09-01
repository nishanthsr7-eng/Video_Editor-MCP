# Frame Extractor MCP

Frame extraction and general clip utilities via ffmpeg command-line tools -
frame extraction, trimming, concatenation, overlay compositing, scaling, and
video info lookup.

Used in this pipeline mainly for `extract_frames_from_video`, feeding source
frames into the Real-ESRGAN upscaling and character extraction steps.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH.

## Tools

- `find_video_path` - recursive filename search under a directory (exact or
  suffix-less match), returns the full path.
- `get_video_info` - duration, fps, codec, width, height.
- `clip_video` - trim by start time plus an end time or duration.
- `concat_videos` - join a list of clips; uses fast-path concat automatically
  when width/height/fps already match across inputs.
- `overlay_video` - composite one video over another at a given position and
  pixel offset.
- `scale_video` - resize, with `-2` on either dimension to preserve aspect
  ratio.
- `extract_frames_from_video` - pull frames as PNG/JPG/WEBP, either every N
  seconds or all frames, with an optional total-frame cap.
- `play_video` - preview a clip via ffplay (rate/loop control).

---

Vendored from [video-creator/ffmpeg-mcp](https://github.com/video-creator/ffmpeg-mcp)
(MIT license, see [LICENSE](LICENSE)) and used as-is.
