# Multi-Agent Orchestration Framework for Generative Video Editing

An AI-native video editing system built on the **Model Context Protocol (MCP)**. An AI assistant (Claude) connects to a suite of specialized tools — each one a standalone MCP server — and composes multi-step editing workflows through natural language.

You describe what you want. The AI calls the right tools in the right order, processes the media, and delivers the result.

---

## Demo

An edit produced with this project — *Cyberpunk: Edgerunners*.

<video src="demo/cyberpunk_edgerunners.mp4" controls muted width="100%"></video>

---

## What this is

Traditional video editing requires manual work in a timeline editor. This framework replaces that loop with a conversation:

> *"Take the intro clip, upscale it, remove the background from the character, put them on a dark gradient, add a word-by-word text reveal synced to the beat drop, grade it cinematic teal-orange, and export for TikTok."*

The AI decomposes that into tool calls — scene detection, frame extraction, upscaling, background removal, compositing, audio analysis, text overlay, color grading, export — and executes the full pipeline end to end.

Each tool is an independent MCP server. The AI connects to all of them simultaneously and can mix and match freely. No single tool knows about the others; the AI is the orchestrator.

---

## What it can do

### Video Analysis
- Detect scene cuts and split footage by shot
- Extract frames (every frame, or sampled at intervals)
- Upscale frames 2–4× via Real-ESRGAN (GPU-accelerated, anime-optimized model included)

### Subject Extraction
- Segment the foreground subject from background using an ONNX ISNet model (anime-optimized)
- Output transparent-background PNGs ready for compositing
- Optionally output the background-only layer

### Audio Analysis
- Detect BPM and per-beat timestamps
- Detect downbeats (first beat of each bar)
- Segment songs into structural sections (intro / verse / build / drop / chorus / outro)
- Detect transient impacts with strength scores
- Transcribe speech locally (faster-whisper) with word-level timestamps

### Beat-Synced Editing
- Automatically cut multiple clips to land on beat boundaries
- Control pacing with beats-per-cut

### Visual Effects
- Zoom punch, camera shake, RGB split, flash, vignette, glow, film grain, light leak, speed ramp
- Cinematic color grades: warm, cool, high contrast, faded, punchy
- 50+ crossfade transition types (xfade presets)
- Chromatic aberration, anamorphic flares, light leaks (animated, procedural)
- Slow-motion with motion-compensated frame interpolation
- Image-to-video Ken Burns (zoom/pan) effect

### Compositing
- Stack multiple layers — characters, text overlays, PIP clips, background images — in a single ffmpeg pass
- Per-layer: position, scale, opacity, time window, audio mix-in
- Green/blue screen keying to transparent webm or direct background replacement

### Text & Subtitles
- Bold animated text overlays: word-by-word reveal, typewriter, fade
- 24 bundled fonts (bold display, script, serif, playful)
- Karaoke-style captions synced to word-level speech timestamps
- Outputs both a transparent overlay webm and a burned-in version

### Color
- 3D LUT grading with 7 cinematic presets (bundled .cube files) at adjustable intensity
- Per-channel color matching between two clips via linear gain/offset

### Audio Post
- EBU R128 loudness normalization
- FFT noise reduction
- Background music mixing with automatic sidechain ducking

### Export
- One-step export to platform specs: YouTube, YouTube Shorts, TikTok, Instagram Reels, Instagram Post, Instagram Story, Twitter, Facebook
- Crop-to-fill or pad-to-fit for aspect ratio mismatches

### Highlight Reel
- Automatically finds and assembles the most energetic moments from any footage based on audio loudness and onset strength

### Timeline Projects
- JSON-described multi-clip sequences with transitions and overlay layers
- Renders the full project to a single MP4 in one ffmpeg pass

---

## DaVinci Resolve Integration

For workflows that use DaVinci Resolve as the editing environment, the project includes a separate layer of tools:

- **Lua scripts** for batch operations inside Resolve: clip coloring, marker creation, timeline stats, media pool organization, beat-sync prep, and more
- **Fusion templates**: 44 title templates, 16 transitions, 28 effects, 5 animated generators — all installable into the free edition of Resolve
- **AI terminal plugin** (`claude-resolve`): embeds an AI assistant directly inside Resolve Studio for natural-language motion graphics

See [DAVINCI.md](DAVINCI.md) for the full reference, including attribution
for the handful of vendored third-party tools it bundles.

---

## How it works

```
.mcp.json              registers all MCP servers with Claude
Tools/                 19 custom MCP servers (Python, uv-managed)
DaVinci_Tools/         DaVinci Resolve utilities and integrations
Sources/               input media
Output/                generated outputs
```

Claude connects to the servers listed in `.mcp.json`. Each server exposes a set of tools. Claude calls them like functions, passing file paths and parameters, reading back results, and chaining outputs into the next call.

A full pipeline — extract → upscale → key out background → analyze audio → composite → grade → export — runs as a single conversation with no manual steps.

See [ARCHITECTURE.md](ARCHITECTURE.md) for a detailed breakdown of every server and tool.

---

## Quick start

See [SETUP.md](SETUP.md) for full installation instructions.

**Short version:**
1. Install `ffmpeg` and `uv`
2. Run `uv sync` in each `Tools/<server>` folder
3. Open Claude Code from this directory — the `.mcp.json` auto-registers all servers
4. Describe your edit

---

## Typical pipeline

```
detect_scenes()              → find shot boundaries in source footage
extract_frames_from_video()  → pull frames from a specific shot
enhance_frames()             → 4× upscale via Real-ESRGAN
extract_character()          → transparent-background character cutouts
detect_beats()               → get beat timestamps from the music
add_text_overlay()           → render a word-by-word reveal overlay
compose_layers()             → composite character + text onto a background
apply_lut()                  → apply a cinematic color grade
export_for_platform()        → encode for TikTok / YouTube Shorts
```

---

## License

MIT — see [LICENSE](LICENSE). A small number of bundled tools are vendored
from other open-source authors and keep their own license: `Tools/Frame_Extractor_MCP/`
and three tools under `DaVinci_Tools/` (see [DAVINCI.md](DAVINCI.md#third-party-tools)).
