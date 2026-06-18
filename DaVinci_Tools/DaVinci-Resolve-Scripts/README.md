# DaVinci Resolve Scripts

A collection of Lua scripts for automating common tasks in DaVinci Resolve via the Resolve Script API.

## What's Included

Scripts are organized by workflow area:

- **Clips Properties** — Batch-color clips on a named track from a CSV color list; color subtitle items by name patterns
- **Editing** — Add and rename tracks from a clipboard list; auto-arrange clips across tracks
- **Grading** — Apply grade operations across multiple clips programmatically
- **Markers** — Create, label, and manage timeline markers in bulk
- **MediaPool** — Organize and manipulate media pool bins and clips
- **Templates** — Fusion title/template utilities
- **Timeline** — Timeline-level operations: resolution, frame rate, and track management

## Installation

Copy scripts to the DaVinci Resolve Fusion Scripts folder for your OS:

**Windows**
```
C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts
```

**macOS**
```
/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility
```

**Linux**
```
/opt/resolve/Fusion/Scripts/Utility
```

After copying, scripts appear under **Workspace → Scripts** in DaVinci Resolve.

## Requirements

- DaVinci Resolve 17 or later (free or Studio)
- Scripting must be enabled: **Preferences → General → Enable scripting using local network**
