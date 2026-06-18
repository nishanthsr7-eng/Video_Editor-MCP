# Architecture

## Overview

The framework is a collection of MCP (Model Context Protocol) servers, each wrapping a specific video processing capability. Claude connects to all of them simultaneously via `.mcp.json` and acts as the orchestrator — choosing which tools to call, in what order, with what parameters.

No single server knows about the others. The AI holds the context of the edit and decides how to compose the pipeline.

```
Claude (AI orchestrator)
    │
    ├── ffmpeg-mcp              Frame extraction, clipping, scaling, concat, playback
    ├── scene-detector-mcp      Shot detection and splitting
    ├── character-extractor-mcp Subject segmentation (ISNet ONNX)
    ├── audio-analyzer-mcp      Beat/BPM, sections, impacts, speech-to-text
    ├── beat-sync-mcp           Beat-grid-driven multi-clip assembly
    ├── effects-mcp             Visual effects and transitions (ffmpeg filters)
    ├── compositor-mcp          Multi-layer compositing (ffmpeg filter_complex)
    ├── chroma-key-mcp          Green/blue screen keying and background replace
    ├── overlay-fx-mcp          Film grain, vignette, chromatic aberration, light leaks
    ├── ken-burns-mcp           Still image → zoom/pan video
    ├── stabilization-mcp       Two-pass video stabilization (vidstab)
    ├── speed-ramp-mcp          Speed control and per-segment speed ramping
    ├── text-overlay-mcp        Animated text overlays and karaoke captions
    ├── color-match-mcp         Per-channel color matching between clips
    ├── lut-grading-mcp         3D LUT color grading (.cube presets)
    ├── export-presets-mcp      Platform-spec export (YouTube, TikTok, Instagram, etc.)
    ├── timeline-project-mcp    JSON-described multi-clip project renderer
    ├── highlight-reel-mcp      Audio-energy-based highlight extraction
    ├── audio-mastering-mcp     Loudness normalization, noise reduction, music mixing
    └── video-edit-mcp          Third-party: MoviePy-based general editing (PyPI)
```

---

## MCP Servers

### `ffmpeg-mcp` — Frame Extractor

**Location:** `Tools/Frame_Extractor_MCP`

Core ffmpeg wrapper. All other processing starts here.

| Tool | What it does |
|---|---|
| `get_video_info` | Returns metadata: duration, resolution, fps, codec, bitrate |
| `find_video_path` | Recursive search for a video file by name |
| `extract_frames_from_video` | Dumps frames to disk as PNG/JPG/WebP at any interval |
| `enhance_frames` | 4× upscale via Real-ESRGAN (GPU, Vulkan) — anime model bundled |
| `clip_video` | Cut a segment by start/end time |
| `scale_video` | Resize to a target resolution |
| `overlay_video` | Picture-in-picture with audio mix |
| `concat_videos` | Concatenate clips (fast mode or re-encode) |
| `play_video` | Playback via ffplay |

Real-ESRGAN binary (`Tools/RealESRGAN/realesrgan-ncnn-vulkan.exe`) is bundled with anime models. Uses Vulkan so it runs on any GPU without CUDA.

---

### `scene-detector-mcp` — Scene Detector

**Location:** `Tools/Scene_Detector_MCP`

Wraps PySceneDetect's content-aware shot detector.

| Tool | What it does |
|---|---|
| `detect_scenes` | Returns shot boundaries as timestamps |
| `split_scenes` | Detects cuts and splits the video into one file per shot |

Useful before per-shot processing: only the relevant shots need to be extracted and processed rather than the whole source file.

---

### `character-extractor-mcp` — Character Extractor

**Location:** `Tools/Character_Extractor_MCP`

Segments the foreground subject from every frame using an ISNet ONNX model (anime-optimized, from `skytnt/anime-seg` on HuggingFace). Runs on CPU via ONNX Runtime.

| Tool | What it does |
|---|---|
| `extract_character` | Outputs transparent-background RGBA PNGs from a frame folder |

Options: inference resolution (default 1024px), soft/hard mask threshold, optional background-only layer output. Throughput: ~1–2s per frame on CPU.

---

### `audio-analyzer-mcp` — Audio Analyzer

**Location:** `Tools/Audio_Analyzer_MCP`

Extracts the audio track from any video and analyzes it. All tools return data — nothing is written to disk.

| Tool | What it does |
|---|---|
| `get_audio_info` | Duration, sample rate, RMS loudness |
| `detect_beats` | BPM + per-beat timestamps (librosa) |
| `detect_downbeats` | First beat of each bar |
| `detect_sections` | Structural segmentation: intro / verse / build / drop / chorus / outro |
| `detect_impacts` | Transient hits with relative strength scores (0–1) |
| `analyze_audio_features` | Per-window RMS, spectral centroid, zero-crossing rate |
| `transcribe_audio` | Local speech-to-text with word-level timestamps (faster-whisper) |

The `transcribe_audio` output feeds directly into `add_karaoke_captions` in `text-overlay-mcp`.

---

### `beat-sync-mcp` — Beat Sync

**Location:** `Tools/Beat_Sync_MCP`

Detects the music's beat grid (librosa) and assembles footage from multiple clips into a beat-synced edit automatically. Cuts land on beat boundaries.

| Tool | What it does |
|---|---|
| `detect_beats` | Analyze tempo and beat timestamps from a music file |
| `generate_beat_synced_video` | Round-robins through the given clips, cutting on every N beats; audio replaced with the music track |

---

### `effects-mcp` — Effects

**Location:** `Tools/Effects_MCP`

Applies ffmpeg-filter-based effects and xfade transitions.

| Tool | What it does |
|---|---|
| `list_effects` | Lists available effect names |
| `apply_effect` | Applies one effect, optionally scoped to a time window |
| `list_transitions` | Lists ~50 xfade transition names |
| `apply_transition` | Joins two clips with a crossfade transition |

Available effects: `zoom_punch`, `shake`, `rgb_split`, `flash`, `vignette`, `glow`, `film_grain`, `light_leak`, `speed_ramp`, `grade_warm`, `grade_cool`, `grade_high_contrast`, `grade_faded`, `grade_punchy`.

---

### `compositor-mcp` — Compositor

**Location:** `Tools/Compositor_MCP`

Composites multiple layers onto a base video in a single ffmpeg `filter_complex` pass. Designed to assemble the outputs of `character-extractor-mcp`, `text-overlay-mcp`, and `chroma-key-mcp` in one shot.

| Tool | What it does |
|---|---|
| `compose_layers` | Stacks N layers (images or videos with alpha) onto a base video |

Per-layer parameters: position (pixel or ffmpeg expressions), scale, opacity, time window, audio mix-in. Layers are drawn back-to-front.

---

### `chroma-key-mcp` — Chroma Key

**Location:** `Tools/Chroma_Key_MCP`

Green/blue screen keying via ffmpeg's chromakey filter.

| Tool | What it does |
|---|---|
| `remove_background` | Keys out a solid color → outputs transparent-alpha webm |
| `replace_background` | Keys out + composites onto a new background in one step |

---

### `overlay-fx-mcp` — Overlay FX

**Location:** `Tools/Overlay_FX_MCP`

Cinematic look effects generated procedurally and blended with screen mode.

| Tool | What it does |
|---|---|
| `add_film_grain` | FastNoise overlay for analog texture |
| `add_vignette` | Dark gradient edges toward center |
| `add_chromatic_aberration` | R/B channel horizontal offset (glitch/CRT look) |
| `add_light_leak` | Animated colored light sweep (warm / golden / cool / white) |

---

### `ken-burns-mcp` — Ken Burns

**Location:** `Tools/Ken_Burns_MCP`

Turns a still image into a video clip with a slow zoom/pan via ffmpeg's `zoompan` filter.

| Tool | What it does |
|---|---|
| `create_ken_burns` | Configurable start/end zoom, pan direction, duration, resolution, fps |

---

### `stabilization-mcp` — Stabilization

**Location:** `Tools/Stabilization_MCP`

Two-pass video stabilization via ffmpeg's `vidstabdetect`/`vidstabtransform`.

| Tool | What it does |
|---|---|
| `stabilize_video` | Configurable smoothing window, shakiness estimate, edge-crop zoom |

---

### `speed-ramp-mcp` — Speed Ramp

**Location:** `Tools/Speed_Ramp_MCP`

Whole-clip or per-segment speed control. For slow motion, uses `minterpolate` for motion-compensated frame interpolation. Audio tempo adjusts automatically (pitch-preserving `atempo`).

| Tool | What it does |
|---|---|
| `change_speed` | Speed multiplier for the whole clip |
| `speed_ramp` | Different speeds for different time segments |

---

### `text-overlay-mcp` — Text Overlay

**Location:** `Tools/Text_Overlay_MCP`

Renders animated text overlays using PIL with 24 bundled fonts. Outputs a transparent VP9 webm overlay plus a burned-in version.

| Tool | What it does |
|---|---|
| `list_fonts` | Lists the 24 bundled fonts |
| `add_text_overlay` | Bold text with word-by-word, typewriter, or fade animation |
| `add_karaoke_captions` | Word-by-word highlighted captions synced to speech timestamps |

Animation modes: `word_by_word` (classic reveal), `typewriter`, `fade`, `none`. Karaoke captions consume the `segments` output from `transcribe_audio` directly.

---

### `color-match-mcp` — Color Match

**Location:** `Tools/Color_Match_MCP`

Matches color grade between two clips by sampling frames and applying a per-channel linear gain/offset via ffmpeg's `lutrgb` filter.

| Tool | What it does |
|---|---|
| `get_color_profile` | Per-channel (R/G/B) mean and standard deviation from sampled frames |
| `match_color` | Maps target clip color statistics toward reference; blendable strength |

---

### `lut-grading-mcp` — LUT Grading

**Location:** `Tools/LUT_Grading_MCP`

Applies 3D LUT color grades via ffmpeg's `lut3d` filter. Intensity is blendable between the original and the fully graded result.

| Tool | What it does |
|---|---|
| `list_luts` | Lists the 7 bundled .cube presets |
| `apply_lut` | Applies a preset or custom .cube file at configurable intensity |

Bundled presets: `cinematic_teal_orange`, `warm_vintage`, `cool_blue`, `high_contrast_bw`, `faded_film`, `moody_green`, `bleach_bypass`.

---

### `export-presets-mcp` — Export Presets

**Location:** `Tools/Export_Presets_MCP`

One-step re-encode to platform-ready specs. Handles aspect ratio mismatches via crop-to-fill or pad-to-fit.

| Tool | What it does |
|---|---|
| `list_platform_presets` | Returns the full table of platform specs |
| `export_for_platform` | Re-encodes to a platform preset |

Platforms: `youtube`, `youtube_shorts`, `tiktok`, `instagram_reels`, `instagram_post`, `instagram_story`, `twitter`, `facebook`.

---

### `timeline-project-mcp` — Timeline Project

**Location:** `Tools/Timeline_Project_MCP`

Maintains a JSON project file describing a multi-clip sequence with transitions and overlay layers. Renders the whole project to a single MP4 in one pass.

| Tool | What it does |
|---|---|
| `create_project` | New project JSON with canvas size and fps |
| `add_clip` | Append a clip to the main timeline |
| `remove_clip` | Remove a clip by index |
| `add_overlay` | Add an overlay layer (image or alpha video) with position and time window |
| `remove_overlay` | Remove an overlay by index |
| `get_project` | Inspect the full project contents and estimated duration |
| `render_project` | Render the full project to MP4 |

---

### `highlight-reel-mcp` — Highlight Reel

**Location:** `Tools/Highlight_Reel_MCP`

Analyzes a video's audio track (RMS loudness + onset strength via librosa), scores sliding windows, greedily picks the highest-scoring non-overlapping segments until a target duration is reached, then concatenates them chronologically.

| Tool | What it does |
|---|---|
| `generate_highlights` | Configurable target duration, clip length, minimum gap between picks |

---

### `audio-mastering-mcp` — Audio Mastering

**Location:** `Tools/Audio_Mastering_MCP`

| Tool | What it does |
|---|---|
| `normalize_loudness` | EBU R128 loudness normalization (ffmpeg `loudnorm`) |
| `reduce_noise` | FFT denoiser for background hiss/hum (ffmpeg `afftdn`) |
| `add_background_music` | Mixes a music track with sidechain ducking; loops to fill video length |

---

### `video-edit-mcp` — General Video Editing (third-party)

**Source:** PyPI — `uvx video-edit-mcp` (no local folder)

A third-party MCP server (MoviePy + yt-dlp) that handles general editing tasks not covered by the custom tools:

- Trim, merge, resize, crop, rotate
- Speed control, fade in/out, grayscale, mirror
- Image/video overlays with transparency
- Frame operations: extract frames, build video from image sequence
- Audio: extract, loop, concat, volume/fade, multiple track mixing, soundtrack replace
- YouTube and platform download via yt-dlp
- In-memory object store for chaining operations without re-specifying paths

---

## Data flow example

A full pipeline converting a raw anime clip into a beat-synced export:

```
1. detect_scenes(source.mp4)
        → [{start, end, file}, ...]

2. extract_frames_from_video(scene_03.mp4)
        → Output/scene_03/frame_0001.png ...

3. enhance_frames(Output/scene_03/)
        → Output/scene_03_enhanced/frame_0001.png ...  (4× upscale)

4. extract_character(Output/scene_03_enhanced/)
        → Output/scene_03_enhanced_character/frame_0001.png  (transparent)

5. detect_beats(music.mp3)
        → {tempo_bpm: 128, beat_times: [0.47, 0.94, 1.41, ...]}

6. transcribe_audio(vocals.mp4, word_timestamps=True)
        → {segments: [{text, words: [{word, start, end}, ...]}]}

7. add_text_overlay(base_clip.mp4, "FINALLY FREE", animation="word_by_word")
        → Output/clip_text_overlay/overlay.webm   (transparent)
        → Output/clip_text_overlay/output_burned.mp4

8. compose_layers(
       base_video=bg.mp4,
       layers=[
           {file: frame_0001.png, x: "W-w-40", y: "H-h-40", width: 600},
           {file: overlay.webm,   x: "(W-w)/2", y: "H-h-200"}
       ]
   )
        → Output/bg_composite.mp4

9. apply_lut(bg_composite.mp4, lut="cinematic_teal_orange")
        → Output/bg_composite_graded.mp4

10. export_for_platform(bg_composite_graded.mp4, platform="tiktok")
        → Output/bg_composite_graded_tiktok.mp4
```
