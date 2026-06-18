# Claude Resolve

**AI Motion Graphics Generator for DaVinci Resolve Studio**

A Workflow Integration Plugin that embeds an AI coding terminal directly inside DaVinci Resolve Studio. Describe an animation in plain text — the plugin generates the code, renders it frame-by-frame to ProRes 4444 with full alpha transparency, and imports it straight into your timeline.

## What It Does

Type a prompt like *"white text revealing letter by letter with a glitch effect"* or *"smooth logo spin with motion blur"* — Claude generates and renders a pixel-perfect animation as a `.mov` file with alpha channel, ready to drop onto any track in Resolve.

**Good for:** title cards, text reveals, glitch transitions, lower thirds, animated logos, stylised overlays — any specific one-off animation for the current project.

**Rendering pipeline:** HTML/CSS/JS animation → Playwright (frame-perfect, no `requestAnimationFrame`) → ffmpeg → ProRes 4444 `.mov` → auto-imported to timeline at playhead.

## Requirements

- **DaVinci Resolve Studio** — Studio edition required (free edition does not support Workflow Integration Plugins). Built against Studio 21.
- **Claude Code CLI** — signed in with a Pro or Max plan. The plugin runs Claude Code as a subprocess; no API key is stored.
- **Node.js 18+** — used by the Claude Code CLI.
- **ffmpeg** — not bundled; the installer auto-installs it via winget (Windows) or Homebrew (macOS).
- **Windows or macOS**

## Installation

### Windows
1. Double-click `install.bat`
2. Restart DaVinci Resolve

### macOS
1. Double-click `install.command`
   - If blocked by Gatekeeper: right-click → **Open**, then confirm
   - If the double-click does nothing: run `bash install.command` in Terminal
   - If Gatekeeper still blocks: `xattr -dr com.apple.quarantine .` in the plugin folder
2. Restart DaVinci Resolve

The installer handles Node.js, the Claude Code CLI, Playwright Chromium, and ffmpeg — and prints a clear summary of anything it couldn't install automatically.

## Usage

1. In Resolve: **Workspace → Workflow Integrations → Claude Resolve**
2. Type a prompt describing the animation
3. Preview the result in the built-in player
4. Click **Render .mov** — the animation is rendered and imported to your timeline

## Settings

- **Model** — Sonnet (faster) or Opus (more detailed)
- **FPS** — 24, 25, 30, or 60
- **Resolution** — 1920×1080, 3840×2160, 1080×1920, 1080×1350, or 1080×1080
- **Assets** — manage rendered `.mov` files; sync to Media Pool or delete

## Bundled Fonts

Ships with three fonts so animations look consistent across machines:

- Bricolage Grotesque
- Fraunces
- JetBrains Mono

## Tech Stack

- **Plugin shell:** Electron (bundled with Resolve 21), HTML/CSS/JS
- **Resolve API:** WorkflowIntegration.node (sandboxed IPC via preload.js)
- **AI engine:** Claude Code CLI spawned via `child_process`
- **Renderer:** Playwright → ffmpeg → ProRes 4444 `.mov`

## Troubleshooting

**Installer hangs at "Downloading Playwright Chromium" (Windows):**
Antivirus (commonly Windows Defender) can block Chromium during extraction. Add the browser cache folder to exclusions and re-run the installer.

**Plugin doesn't appear in Resolve after install:**
Ensure Resolve was fully restarted, not just the project. Check that the plugin folder was copied to `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Workflow Integration Plugins\`.

**First response is slow:**
The Claude Code CLI process cold-starts on the first prompt. Subsequent responses in the same session are faster.
