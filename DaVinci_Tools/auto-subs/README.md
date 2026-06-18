# AutoSubs

Local-first AI subtitle generator. No cloud, no subscription, no data leaving your machine.

Works as a standalone app and integrates directly with **DaVinci Resolve**, **Adobe Premiere Pro**, and **After Effects**.

## Features

- **On-device transcription** via Whisper, Moonshine, and Parakeet models (whisper-rs + ONNX Runtime)
- **Speaker diarization** — identifies and labels individual speakers, enabling per-speaker subtitle styling
- **100+ languages** — transcription and translation across a wide range of languages
- **GPU acceleration** — Vulkan on Windows, DirectML on Windows, Metal on Apple Silicon
- **Cross-platform** — macOS (Apple Silicon and Intel), Windows, Linux
- **CLI mode** — scriptable for batch processing

## Requirements

- DaVinci Resolve, Adobe Premiere Pro, or After Effects (for NLE integration)
- Or use standalone with any video/audio file
- GPU optional but recommended for faster transcription

## Installation

Build from source using Rust + Cargo (Tauri project):

```bash
cd AutoSubs-App
cargo tauri build
```

Or install the Adobe extension separately from the `Adobe-Extension/` folder for Premiere Pro / After Effects integration.

## Usage

### Standalone
1. Launch AutoSubs and select an audio or video file
2. Choose your model size and language options
3. Click **Transcribe** — edit speakers and subtitles in the viewer
4. Export as SRT, plain text, or copy to clipboard

### DaVinci Resolve
1. Open DaVinci Resolve
2. Navigate to **Workspace → Scripts → AutoSubs**
3. Select your timeline clip and click **Transcribe**
4. Subtitles are added directly to the timeline with your chosen styling

### Adobe Premiere Pro / After Effects
Install the Adobe extension from `Adobe-Extension/` and access AutoSubs from the **Window → Extensions** menu.

## Tech Stack

Built with Rust, Tauri, and React. Transcription via whisper-rs (Rust bindings for Whisper) and ONNX Runtime for Moonshine/Parakeet models. Diarization via a bundled Rust diarization crate.
