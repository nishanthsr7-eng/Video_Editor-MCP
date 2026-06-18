# Speed Ramp MCP

Changes playback speed of a whole clip or specific segments ("speed
ramping"), with motion-compensated frame interpolation for smooth slow
motion and pitch-preserving audio tempo adjustment.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH.

## Tools

- `change_speed` - speed up or slow down an entire clip, with optional
  `minterpolate`-based smoothing for slow motion.
- `speed_ramp` - apply different speeds to different time segments of a
  clip and concatenate the result.
