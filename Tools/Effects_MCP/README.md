# Effects MCP

Applies "edit-style" effects (zoom punch, shake, RGB split, flash, vignette, glow, film
grain, light leak, speed ramp, color grading presets) and transitions (ffmpeg `xfade`,
~50 built-in transition types) to video clips via ffmpeg.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH.

## Tools

- `list_effects` - list available effect names and descriptions.
- `apply_effect` - apply one effect to a clip (optionally limited to a time range).
- `list_transitions` - list available xfade transition names.
- `apply_transition` - crossfade/transition between two clips.
