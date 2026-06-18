# Audio Analyzer MCP

Analyzes the audio track of a video (or a standalone audio file) for tempo/beat,
transcription, impact/transient moments, and spectral features - useful for
beat-synced editing, caption timing, and finding "impactful" moments to cut on.

## Setup

```
uv sync
```

Requires `ffmpeg` on PATH (used to extract audio from video files).
`faster-whisper` downloads its model weights from huggingface on first use
(cached afterwards).

## Tools

- `get_audio_info` - duration, sample rate, overall loudness (RMS).
- `detect_beats` - tempo (BPM) and beat timestamps for rhythm-synced cuts.
- `detect_impacts` - transient/"impact" moments (drum hits, sudden loudness
  changes) with relative strength, for transitions/effect triggers.
- `analyze_audio_features` - per-window RMS, spectral centroid, zero-crossing
  rate, plus overall summary stats.
- `transcribe_audio` - local speech-to-text (faster-whisper) with word-level
  timestamps ("audio text").
