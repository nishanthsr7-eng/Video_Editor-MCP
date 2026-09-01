# Setup

## Prerequisites

### ffmpeg

All video processing relies on ffmpeg. Install via winget on Windows:

```powershell
winget install Gyan.FFmpeg
```

This installs the full build (includes libvidstab for stabilization, libvpx for alpha-channel webm output). Verify it's on your PATH:

```bash
ffmpeg -version
ffprobe -version
```

### uv

`uv` is a fast Python package manager used to manage the virtual environment for each MCP server.

```powershell
winget install astral-sh.uv
```

---

## Installing MCP server dependencies

Each MCP server is a standalone Python project. Run `uv sync` inside each one:

```bash
cd "Tools/Audio_Analyzer_MCP" && uv sync
cd "Tools/Beat_Sync_MCP"      && uv sync
cd "Tools/Character_Extractor_MCP" && uv sync
cd "Tools/Color_Match_MCP"    && uv sync
cd "Tools/Compositor_MCP"     && uv sync
cd "Tools/Effects_MCP"        && uv sync
cd "Tools/Export_Presets_MCP" && uv sync
cd "Tools/Frame_Extractor_MCP" && uv sync
cd "Tools/Highlight_Reel_MCP" && uv sync
cd "Tools/Ken_Burns_MCP"      && uv sync
cd "Tools/LUT_Grading_MCP"    && uv sync
cd "Tools/Overlay_FX_MCP"     && uv sync
cd "Tools/Scene_Detector_MCP" && uv sync
cd "Tools/Speed_Ramp_MCP"     && uv sync
cd "Tools/Stabilization_MCP"  && uv sync
cd "Tools/Text_Overlay_MCP"   && uv sync
cd "Tools/Timeline_Project_MCP" && uv sync
cd "Tools/Audio_Mastering_MCP" && uv sync
cd "Tools/Chroma_Key_MCP"     && uv sync
```

Servers that have no extra Python dependencies (only ffmpeg on PATH) skip the `uv sync` step entirely — their `pyproject.toml` will have an empty dependencies list.

The `video-edit-mcp` server (third-party) needs no local install — it runs via:

```bash
uvx video-edit-mcp
```

---

## Registering with Claude Code

The `.mcp.json` at the project root registers all MCP servers. Open Claude Code from this directory:

```bash
claude
```

All servers are available immediately. No manual connection step.

> **After any code change** inside a Tools/ folder, restart Claude Code (or use `/mcp reconnect` if available) so the updated code is reloaded.

---

## Model file downloads

Some servers download model weights on first use:

| Server | Model | Download size | Notes |
|---|---|---|---|
| `character-extractor-mcp` | ISNet ONNX (`isnetis.onnx`) | ~170 MB | Bundled in `Tools/Character_Extractor_MCP/models/` — no download needed |
| `audio-analyzer-mcp` | faster-whisper (speech-to-text) | 74 MB (base) – 3 GB (large-v3) | Downloaded from HuggingFace on first `transcribe_audio` call, then cached |

---

## DaVinci Resolve setup (optional)

Required only if you intend to use the DaVinci Resolve integration.

**Enable external scripting in Resolve:**
> Preferences → System → General → External scripting using = **Local**

Restart Resolve after changing this setting.

**Install Lua scripts and Fusion templates:**

```powershell
powershell -ExecutionPolicy Bypass -File "DaVinci_Tools\manage-scripts.ps1"
```

Select option `[2] Install` and enter `all` to install everything, or pick specific items by number.

After installation, fully quit and reopen Resolve to refresh the Effects panel.

---

## Directory structure

```
project root/
├── .mcp.json                  MCP server registration for Claude Code
├── Tools/                     19 custom MCP servers
│   ├── Audio_Analyzer_MCP/
│   ├── Beat_Sync_MCP/
│   ├── Character_Extractor_MCP/
│   ├── ... (one folder per server)
│   └── RealESRGAN/            Bundled upscaling binary + anime models
├── DaVinci_Tools/             DaVinci Resolve utilities
│   ├── DaVinci-Resolve-Scripts/
│   ├── resolve-scripts/
│   ├── claude-resolve/
│   ├── DaVinciResolve-DynamicText/
│   ├── auto-subs/
│   └── manage-scripts.ps1
├── DaVinci_Scripts/           Fusion templates and Lua scripts (source)
│   ├── Templates/
│   └── Scripts/
├── demo/                      Showcase clip embedded in README.md
├── Sources/                   Input media (not tracked in git)
└── Output/                    Generated outputs (not tracked in git)
```

---

## GPU acceleration

Real-ESRGAN (frame upscaling) uses **Vulkan** via the bundled `realesrgan-ncnn-vulkan.exe` binary. This works on any GPU with Vulkan support — NVIDIA, AMD, and Intel. No CUDA or ROCm required.

The Character Extractor (background removal) runs on **CPU via ONNX Runtime**. On a mid-range CPU this is ~1–2 seconds per frame. For large batches, run the extraction overnight or process only the shots you need after splitting scenes first.

All other processing (ffmpeg filters, audio analysis, text rendering) runs on CPU.
