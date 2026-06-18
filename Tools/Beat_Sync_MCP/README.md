# Beat Sync MCP

Detects the beat grid of a music track (via librosa) and automatically cuts
together footage from multiple clips so the edits land on the beat -
a "kinetic" music-video style cut.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH plus librosa/numpy/soundfile (installed
via uv sync).

## Tools

- `detect_beats` - analyze a music file's tempo (BPM) and beat timestamps.
- `generate_beat_synced_video` - cut and concatenate footage from a list of
  clips, switching on beat boundaries, with the music track as final audio.
