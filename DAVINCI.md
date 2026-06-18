# DaVinci Resolve Integration

The `DaVinci_Tools/` folder contains a separate layer of tools for workflows centered on DaVinci Resolve. These work alongside the MCP servers but operate differently — they talk directly to a running Resolve instance via its Scripting API, or install assets into Resolve's file system.

---

## What's included

```
DaVinci_Tools/
├── DaVinci-Resolve-Scripts/    Lua scripts for batch timeline operations
├── resolve-scripts/            Additional Lua automation scripts
├── DaVinciResolve-DynamicText/ Python tool for driving Fusion title templates with live data
├── auto-subs/                  Local AI subtitle generator with Resolve/Premiere/AE integration
├── claude-resolve/             AI terminal plugin embedded inside Resolve Studio
├── awesome-davinci-resolve/    Curated reference: plugins, DCTLs, OFX effects, workflow tools
└── manage-scripts.ps1          Interactive script installer/remover
```

And separately, Fusion templates installed into Resolve:

```
DaVinci_Scripts/
├── Templates/
│   ├── Titles/      44 templates: animated, 3D, overlay, FX, captions, meme, chat
│   ├── Effects/     28 effects: cinematic grades, anime effects, overlay looks
│   ├── Transitions/ 16 transitions: classic + anime + kinetic
│   └── Generators/  5 animated backgrounds
└── Scripts/
    ├── Edit/        10 edit page scripts
    └── Utility/     10 utility scripts
```

---

## Python scripting bridge

`davinci_amv_builder.py` demonstrates how to build a full Resolve timeline programmatically. It connects to a running Resolve instance, reads a set of JSON descriptor files that describe clips, transitions, effects, and subtitles, then places everything on the timeline automatically.

**How it connects:**

```python
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
pm   = resolve.GetProjectManager()
proj = pm.GetCurrentProject()
mp   = proj.GetMediaPool()
```

This requires Resolve to be open with external scripting enabled:
> **Preferences → System → General → External scripting using = Local**

**Run from DaVinci's internal console** (Workspace → Console → Py3):
```python
exec(open(r"path\to\davinci_amv_builder.py", encoding="utf-8").read(), globals())
```

**Or run from a terminal:**
```bash
python davinci_amv_builder.py
```

### What the script does

Given a set of JSON analysis files (clip selections, transition definitions, subtitle data, audio analysis), the script:

1. Creates a new timeline at the target resolution and frame rate
2. Imports source clips into the media pool
3. Places clips on the timeline in order, setting in/out points
4. Applies clip colors per segment (for visual organization in the timeline)
5. Adds markers with grade instructions so the colorist knows what to apply per section
6. Inserts the audio track

The JSON files that drive it are produced by the MCP server pipeline (audio analysis, beat detection, manual clip selection). This is the bridge between the automated processing side and the final manual polish in Resolve.

---

## Fusion templates

All templates are `.setting` files that install into Resolve's Fusion templates directory:

```
%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Templates\Edit\
```

They work in the **free edition** of DaVinci Resolve. No Studio license required.

### Accessing templates in Resolve

| Asset type | Location in Resolve |
|---|---|
| Titles / Overlays / Animated / 3D | Edit page → Effects → Toolbox → Titles |
| Transitions | Edit page → Effects → Toolbox → Video Transitions → Fusion Transitions |
| Effects (grades, shakes, glows) | Edit page → Effects → Toolbox → Effects → Fusion Effects |
| Generators | Edit page → Effects → Toolbox → Generators |
| Scripts | Any page → Workspace → Scripts → Edit / Utility |

---

### Titles (44 templates)

**Base titles** — static text, lower thirds, subtitles, news bars, watermarks

**Animated titles** — auto-play on clip start: fade in, slide in, scale pop, bounce, typewriter, zoom fade out

**3D style titles** — built from stacked Fusion nodes (no 3D workspace needed): extruded, drop shadow, neon glow, gold metallic, chrome silver, fire text, outline only

**Overlay presets** — composited over footage: cinematic letterbox bars, social follow prompts, podcast layout, score bar, meme captions, chat bubbles, reaction pops, audio waveform visualizer, news ticker, countdown timer

**FX overlays** — animated: speed lines flash, lens flare hit, neon sign flicker, matrix rain, logo reveal, split text reveal, progress bar

---

### Effects (28 presets)

Drop directly onto a clip in the timeline.

**Cinematic:** Vignette, Soft Glow, Film Grain, Blur Edges

**Anime / viral impact:**
| Effect | Use case |
|---|---|
| Chromatic Aberration | Power hits, intense moments, sakuga sequences |
| Screen Shake | Impact frames, explosions, landings |
| Zoom Punch | Attack moments, single-frame emphasis |
| Afterimage Echo | Fast movement, speed smear, fighting edits |
| VHS Retro | Flashback scenes, nostalgia edits |
| High Contrast Grade | Action sequences, fight edits, hype reels |
| Teal Orange Grade | Cinematic AMVs, movie-style edits |
| Vignette Pulse | Tense moments, boss fight intros, dramatic reveals |

**Additional looks:** Duotone, Bleach Bypass, Film Halation, Neon Cyberpunk, Lo-Fi Dreamy, Anamorphic Flare Streaks, Old Film, BW Color Pop, Mirror Effect, Edge Glow, Light Rays, Rain Overlay, Bokeh Particles, Pixelate, Posterize

**Stacking tip:** Apply **Chromatic Aberration** + **Screen Shake** together on an impact clip. Cut to a clip with **High Contrast Grade**. This is the standard anime edit impact formula.

---

### Transitions (16 presets)

Drag between two clips on the timeline.

**Classic:** Dip to Black, Dip to White, Cross Blur

**Anime / kinetic:**
| Transition | Use case |
|---|---|
| Flash White | Power-up moments, impact hits, scene reveals |
| Flash Black | Fight cuts, chapter breaks |
| Whip Pan Right | Scene whip transitions |
| Zoom Blur Cut | Speed ramps, action sequence cuts |
| Glitch Cut | Tech/cyber edits, hype montages |

**Additional:** Spin Rotate, Slide Push Left, Circle Iris, Strobe Cut, Color Wipe, Pixel Scatter, Flip Horizontal, Light Leak

**Flash transition tip:** Set Flash White or Flash Black to exactly 20 frames. Place it at the cut between an impact frame and the reaction shot.

---

### Generators (5 animated backgrounds)

Drag onto an empty track. Use as standalone backgrounds on V1, or as composited layers behind titles.

| Generator | What it produces |
|---|---|
| Animated Gradient | Two-color gradient cycling through hue combinations |
| Aurora Northern Lights | Green + blue animated light ribbons on dark sky |
| Electric Sparks | Animated particle arcs — lightning/plasma look |
| Glitch Bars | Cyan + magenta horizontal noise bars — digital interference |
| Starfield | Three layers of drifting star points on deep space |

---

## Lua scripts

Run from **Workspace → Scripts** in any page. Output appears in the Console.

### Edit page scripts

| Script | What it does |
|---|---|
| `colorize_tracks` | Colors all video clips by track: Track 1 = Orange, Track 2 = Yellow, etc. |
| `add_interval_markers` | Adds chapter markers every N seconds across the whole timeline |
| `auto_scene_markers` | Adds a Yellow marker at the start of every clip on V1 |
| `beat_sync_prep` | Prints all markers and V1 edit points with frame numbers for beat planning |
| `insert_flash_frames` | Marks the playhead clip's start frame for manual flash frame placement |
| `remove_all_markers` | Clears every marker from the timeline |
| `flag_short_clips` | Marks clips shorter than N frames Red |
| `set_all_duration` | Checks V1 clips against a target frame count (Green = match, Orange = differs) |
| `batch_add_effect` | Adds Cyan markers on every V1 clip as reminders to apply a specific effect |
| `copy_grade_to_track` | Marks the first clip and prints all V1 clip names with grade-copy shortcuts |

### Utility scripts

| Script | What it does |
|---|---|
| `timeline_stats` | Prints duration, fps, track count, total clips, marker count |
| `find_gaps` | Lists every gap in all video tracks with timecode and length |
| `export_clip_list` | Exports every clip's name, in-point, and duration to a text file |
| `youtube_chapters` | Converts timeline markers to YouTube timestamp format for the description |
| `organize_media_pool` | Moves all clips into Video / Audio / Images / Other sub-bins |
| `duplicate_timeline` | Creates a copy of the current timeline |
| `rename_sequential` | Renames video clips Clip_001, Clip_002, etc. left-to-right, top track first |
| `clear_clip_colors` | Removes all clip color flags |
| `export_markers_csv` | Exports all markers to CSV: Frame, Timecode, Color, Name, Note, Duration |
| `count_clip_usage` | Counts how many times each clip appears across all video tracks |

---

## Script manager

`manage-scripts.ps1` installs and removes scripts without touching Resolve's folders manually.

```powershell
powershell -ExecutionPolicy Bypass -File "DaVinci_Tools\manage-scripts.ps1"
```

Options: List installed scripts, Install selected scripts (by number or `all`), Delete selected scripts.

---

## Anime edit workflow in Resolve

A step-by-step sequence for creating beat-synced anime edits using the installed presets.

**1. Beat prep**
- Import audio to A1
- Run `add_interval_markers` as rough 5-second guides
- Manually place markers on the exact music beats you want to cut to
- Run `beat_sync_prep` → copy frame numbers → plan cuts in a spreadsheet

**2. Cut to beat**
- Edit anime clips on V1 to land on beat markers
- Keep impact frames 2–4 frames long
- Run `colorize_tracks` after rough cut

**3. Impact effects** (on the key clip, stacked)
1. Drag **Screen Shake** onto the clip
2. Drag **Chromatic Aberration** onto the same clip
3. Place **FX Lens Flare Hit** on V2 above the cut point
4. (Optional) Place **FX Speed Lines** on V2 a few frames before the hit

**4. Transitions**
- Impact cut: **Flash White** or **Flash Black** (12–20 frames)
- For tech/cyberpunk: **Glitch Cut**
- Scene whip: **Whip Pan Right** (12–18 frames)
- Speed ramp moment: **Zoom Blur Cut** (20 frames)

**5. Color grade**
- Hero clips: **Teal Orange Grade** or **High Contrast Grade**
- Flashback/memory clips: **VHS Retro**
- Climax: add **Vignette Pulse** on top

**Recommended combinations by scene type:**

| Scene | Effect stack |
|---|---|
| Punch/kick landing | Screen Shake + Chromatic Aberration + Flash White |
| Speed burst | Zoom Punch + FX Speed Lines + Zoom Blur Cut |
| Explosion | Screen Shake + FX Lens Flare Hit + High Contrast Grade |
| Flashback | VHS Retro + Soft Glow + Dip to White |
| Boss reveal | Vignette Pulse + High Contrast Grade + Flash Black |
| Power-up | Chromatic Aberration + Teal Orange Grade + FX Lens Flare Hit |
