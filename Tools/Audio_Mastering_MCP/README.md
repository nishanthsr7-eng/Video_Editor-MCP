# Audio Mastering MCP

Post-processing for audio tracks: loudness normalization (EBU R128 loudnorm), noise
reduction (afftdn), and background music mixing with optional sidechain ducking.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH.

## Tools

- `normalize_loudness` - normalize a track to a target LUFS.
- `reduce_noise` - reduce steady background noise (afftdn).
- `add_background_music` - mix in a music track, optionally ducking it under dialogue.
