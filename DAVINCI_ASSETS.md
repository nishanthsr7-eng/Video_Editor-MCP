# DaVinci Resolve — Installed Assets Reference

All assets are installed in the free edition of DaVinci Resolve. No Studio license required.

---

## How to access everything

| Asset type | Where to find it in Resolve |
|---|---|
| Titles / Overlays / Animated / 3D | Edit page → **Effects** (top-left panel) → **Toolbox** → **Titles** |
| Transitions | Edit page → **Effects** → **Toolbox** → **Video Transitions** → **Fusion Transitions** |
| Effects (Vignette, Glow, etc.) | Edit page → **Effects** → **Toolbox** → **Effects** → **Fusion Effects** |
| Scripts | Any page → **Workspace** menu → **Scripts** → Edit / Utility |
| Manage scripts | Run `manage-scripts.ps1` from the `DaVinci_Tools` folder |

> **After any Resolve restart** all assets refresh automatically. If something doesn't appear, fully quit and reopen Resolve.

---

## Titles

Drag from **Effects → Titles** onto an empty track above your video clip.  
To edit the text: double-click the clip on the timeline → the **Fusion** page opens → click the `TextPlus` node → change `StyledText` in the Inspector.

### Base Titles

| Name | Description |
|---|---|
| **Lower Third Simple** | Two-line lower third — name (white, bold) + role (blue, smaller). Left-aligned, lower-quarter position. |
| **Lower Third Bold Line** | Same as above but with a blue accent bar between the two lines. |
| **Center Title** | Large bold title centered on screen with a gray subtitle line below it. |
| **Bottom Subtitle** | Single white caption line centered near the bottom — use as a subtitle or translation. |
| **Breaking News Bar** | Full-width red bar at the bottom with "BREAKING" tag and scrolling headline text. |
| **Minimal Quote** | Italic quote text with large decorative quote mark and a source credit line. |
| **Top Left Title** | Episode title in the top-left corner with an episode number below it. |
| **Corner Watermark** | Semi-transparent handle (`@YourHandle`) in the top-right corner. Stays out of the way. |

---

### Animated Titles

These play their animation automatically when the clip starts. Trim the clip length to control how long the text stays on screen.

| Name | Animation | Duration |
|---|---|---|
| **Anim Fade In** | Text fades from invisible to full opacity | 30 frames |
| **Anim Fade Up** | Text rises slightly upward while fading in | 25 frames |
| **Anim Slide In Left** | Text slides in from off-screen left | 25 frames |
| **Anim Slide Up Lower Third** | Lower third (name + role) slides up from below frame | 28 frames |
| **Anim Scale Pop** | Text scales from zero with a small bounce at the end | 24 frames |
| **Anim Bounce In** | Text grows → overshoots → settles — elastic snap feel | 33 frames |
| **Anim Typewriter** | Text reveals left-to-right as if being typed (Courier font) | 60 frames |
| **Anim Zoom Fade Out** | Text slowly zooms outward while fading — use as an exit | 30 frames |

**How to change animation speed:**  
Open in Fusion → click the `BezierSpline` or `Path` node → drag the keyframe handles in the spline editor to make the animation faster or slower.

---

### 3D Style Titles

All 3D effects are built from stacked Fusion nodes — no 3D workspace needed.  
Edit text in the **front/core TextPlus node** (usually named `FrontText`, `CoreText`, `GoldText`, etc.).

| Name | Effect |
|---|---|
| **3D Extruded White** | Layered dark copies behind a bright white face create real depth and extrusion. |
| **3D Drop Shadow** | Blurred dark shadow offset from the text — clean professional look. |
| **3D Neon Glow** | Double glow (wide + tight) in blue-cyan around white text — neon sign effect. |
| **3D Gold Metallic** | Yellow-gold text with a specular highlight burst and cast shadow below. |
| **3D Chrome Silver** | Silver-gray text with dark reflections and a sharp specular flare. |
| **3D Fire Text** | Orange text with red outer glow and a bright hot-core inner glow. |
| **3D Outline Only** | Colored outline with hollow/transparent fill — editorial or logo-style look. |

**To change glow color** (Neon, Fire):  
In Fusion → click the `ColoredText` or `ColorCorrector` node → adjust the Midtones R/G/B sliders.

---

### Overlay Presets

Place on a track **above** your video. These composite over the footage.

| Name | Description | How to use |
|---|---|---|
| **Overlay Cinematic Bars** | Black bars top and bottom (2.35:1 letterbox look) | Place on V2 or higher for the full duration of your edit |
| **Overlay Cinematic Bars** | Black bars — 20% each side | Place on top track; trim to sequence length |
| **Overlay Social Follow** | Dark pill with "Follow for more!" + `@YourHandle` at bottom center | Change both TextPlus nodes to your handle |
| **Overlay Podcast Style** | Left blue accent bar + episode number + guest name + topic, dark card | Edit `EpLabel`, `NameLabel`, `TopicLabel` nodes |
| **Overlay Text Box** | Semi-transparent dark card with text — versatile info card | Edit `BoxText` node |
| **Overlay Score Bar** | Team A vs Team B scoreboard at the top — yellow scores, white names | Edit `Team1Name`, `Team1Score`, `Team2Name`, `Team2Score` |
| **FX Speed Lines** | White radial speed lines that flash in and out over 12 frames — anime energy burst | Place on V2 above your clip; the flash animates automatically at timeline start |
| **FX Lens Flare Hit** | Animated white-gold light burst that flares up then fades — impact flash overlay | Place on V2 at exact cut point; flare peaks at frame 5 and fades by frame 18 |
| **Neon Sign Flicker** | White-cyan neon text with double glow layer and realistic flicker animation | Edit `NeonText` → `StyledText`; adjust `FlickerSpline` keyframes to change flicker timing |
| **Countdown Timer** | 5→1 countdown with color shift (white→yellow→orange→red→alarm red) at 30fps | Each number visible for 30 frames; adjust A5/A4/A3/A2/A1 spline keyframe positions for different timing |
| **Progress Bar** | Animated fill bar sliding left-to-right with label text — 150-frame fill | `FillSpline` → keyframe [0] and [150] for start/end X positions; change `LabelText` content |
| **Meme Caption** | Bold Impact-style top and bottom captions — classic meme format | Edit `TopText` and `BottomText` → `StyledText`; change `Size` for smaller/larger |
| **Chat Bubble** | Blue rounded pill bubble with sender name + message text, fades in over 8 frames | Edit `SenderText` and `BubbleText` → `StyledText`; `BubbleAlpha` spline for timing |
| **Reaction Text Pop** | Bold yellow word that bounces in (0→1.2→1 scale), holds, then fades — reaction sticker feel | Edit `ReactionText` → `StyledText`; `PopSize` spline for bounce timing |
| **Audio Waveform Bar** | 8 animated equalizer bars with staggered up-down splines — music visualizer | Each `H1`–`H8` spline controls that bar's height animation; edit `BarBg` for bar color |
| **Split Text Reveal** | Large top word slides down from above, subtitle slides up from below, meet in center | Edit `TopHalf` and `BottomHalf` → `StyledText`; `TopPath`/`BotPath` for slide distance |
| **Vertical Story Frame** | Black bars top and bottom (22% each) for portrait/mobile framing with handle text | Edit `SafeLabel` → `StyledText` for your handle; adjust `TopMask`/`BotMask` Height for bar size |
| **Logo Reveal** | Dark background + bouncing scale reveal + glow halo — placeholder logo animation | Edit `LogoText` → `StyledText`; `LogoSize` spline for timing; `GlowBlur` → `XBlurSize` for halo |
| **News Ticker Scroll** | Red ticker bar with dark LIVE tag + scrolling white headline text — 240-frame scroll | Edit `ScrollText` → `StyledText`; `ScrollPath` [240] X value for scroll speed; `TagText` for tag label |
| **Matrix Rain** | Animated green falling column noise on black background — hacker aesthetic | `RainNoise` → `SeetheRate` (fall speed), `XScale` (column width); `GreenTint` → `GainGreen` for brightness |

---

## Effects

Drag from **Effects → Fusion Effects** and drop directly **onto a clip**.  
Adjust intensity in the **Inspector** or by opening the clip in Fusion.

### Cinematic Effects

| Name | What it does | Key controls in Fusion |
|---|---|---|
| **Vignette** | Dark gradient edges draw focus toward the center of the frame | `EllipseMask` → `Width`/`Height` (size), `SoftEdge` (falloff); `BgDark` → `TopLeftAlpha` (darkness) |
| **Soft Glow** | Blurred copy of the image merged with Screen blending — cinematic glow | `Blur1` → `XBlurSize` (spread); `GlowMerge` → `Blend` (intensity) |
| **Film Grain** | `FastNoise` overlay in Overlay blend mode for analog texture | `Noise1` → `XScale`/`YScale` (grain size); `GrainMerge` → `Blend` (strength) |
| **Blur Edges** | Center stays sharp, edges blur — simulates shallow depth of field | `CenterMask` → `Width`/`Height` (sharp area size), `SoftEdge` (transition); `BlurredCopy` → `XBlurSize` (edge blur amount) |

### Anime / Viral Effects

Apply these to single clips for viral motion-edit impact. Stack multiple effects for stronger looks.

| Name | What it does | Key controls in Fusion | Anime usage |
|---|---|---|---|
| **Chromatic Aberration** | Splits red, green, and blue channels and shifts them in opposite directions — lens distortion look | `RedShifted` → `XOffset`/`YOffset` (shift red right); `BlueShifted` → `XOffset`/`YOffset` (shift blue left). Increase both for stronger effect | Power hits, intense moments, sakuga sequences |
| **Screen Shake** | Animated Transform that rapidly jiggles the frame in small random offsets over 18 frames | `ShakePath` → edit Point positions to change shake direction/distance; `ShakeTransform` → `Size` (slight overscale hides edges) | Impact frames, explosions, landing effects |
| **Zoom Punch** | Quick scale from 1.0 → 1.18 → settles at 1.15 — a punch-in zoom with snap | `ZoomSpline` → move keyframes to change speed; adjust peak value for subtler/stronger punch | Attack moments, emphasis on a single frame |
| **Afterimage Echo** | Three offset copies of the clip merged behind the original at decreasing opacity — motion trail | `Echo1/2/3` → `XOffset`/`YOffset` (trail direction); `MergeE1/2/3` → `Blend` (trail opacity) | Fast movement, speed smear, fighting edits |
| **VHS Retro** | Desaturation + scanline noise + film grain + slight chroma shift — analog tape look | `Desaturate` → `SaturationMaster` (less color); `GrainMerge` → `Blend` (grain strength); `ChromaBlend` → `Blend` (chroma shift) | Flashback scenes, 80s/90s nostalgia edits |
| **High Contrast Grade** | Punchy contrast with warm highlights and cool shadows — dramatic cinematic look | `HighContrast` → `ContrastMaster` (overall punch); `GainRed`/`GainBlue` (warm/cool balance) | Action sequences, fight edits, hype reels |
| **Teal Orange Grade** | Classic Hollywood blockbuster color grade — teal in shadows, orange in highlights | `TealOrange` → `LowRed`/`LowBlue` (shadow teal depth); `HighRed`/`HighBlue` (highlight warmth) | Cinematic AMVs, movie-style edits |
| **Vignette Pulse** | Animated vignette that rhythmically contracts and expands — heartbeat/tension pulse | `PulseSpline` → keyframe values (vignette size per frame); adjust period (frame spacing) for faster/slower pulse | Tense moments, boss fight intros, dramatic reveals |

**Stacking tip:** For peak anime edit impact, apply **Chromatic Aberration** + **Screen Shake** together on a single impact clip. Then cut to a clean clip with **High Contrast Grade** applied.

### Additional Effects

| Name | What it does | Key controls in Fusion |
|---|---|---|
| **Duotone** | Full desaturation then recolors shadows purple-blue and highlights gold-orange | `DuoTone` → `LowRed/G/B` (shadow color), `HighRed/G/B` (highlight color) |
| **Bleach Bypass** | Screen blends a grayscale copy over itself — low saturation, lifted blacks, high contrast | `FinalGrade` → `ContrastMaster`, `SaturationMaster`, `BrightnessLow` |
| **Film Halation** | Extracts highlights, blurs them heavily, tints orange-red, screen blends back — real film lens artifact | `HaloBlur` → `XBlurSize`/`YBlurSize` (glow spread); `HaloTint` → `GainRed`/`GainBlue` (color) |
| **Neon Cyberpunk Grade** | Blue-cyan shadows, pink-magenta highlights, high saturation, soft glow layer | `CyberpunkGrade` → all channel Gain/Low/High sliders; `GlowMerge` → `Blend` |
| **Lo-Fi Dreamy** | Lifted blacks, pastel saturation, soft screen glow — Tumblr/aesthetic vibe | `PastelGrade` → `BrightnessLow` (lift), `SaturationMaster`; `DreamMerge` → `Blend` |
| **Anamorphic Flare Streaks** | Extracts highlights, extreme horizontal blur only, tints blue — anamorphic lens streak | `HorizStreak` → `XBlurSize` (streak length); `BlueTint` → channel Gain (streak color) |
| **Old Film** | Sepia grade + flicker brightness oscillation + vertical scratch noise + grain + vignette | `FlickerSpline` keyframe values; `ScratchMerge`/`GrainMerge` → `Blend` |
| **BW Color Pop** | Near-grayscale with a slight color overlay — hint-of-color effect | `Grayscale` → `SaturationMaster`; `ColorPop` → `Blend` (0 = full B&W, higher = more color) |
| **Mirror Effect** | Flips and double-exposes the clip over itself — symmetrical abstract look | `MirrorBlend` → `Blend` (0.5 = equal mix, 1 = full flip) |
| **Edge Glow** | Difference-extracts edges, tints green, blurs them, screen blends back — anime cel look | `EdgeBright` → `MasterRGBGain` (glow intensity), `GainGreen` (color); `GlowMerge` → `Blend` |
| **Light Rays** | Crushes shadows, double-blurs highlights into warm god rays | `RayBlurX`/`RayBlurX2` → `XBlurSize`/`YBlurSize` (ray spread); `RayMerge` → `Blend` |
| **Rain Overlay** | Animated vertical streak noise screen-blended over clip — blue-tinted rain | `RainNoise` → `SeetheRate` (rain speed), `XScale` (streak density); `RainMerge` → `Blend` |
| **Bokeh Particles** | Blurred noise particles in blue-purple tones screen-blended — soft light bokeh | `BokehBlur` → `XBlurSize` (circle size); `BokehTint` → channel Gain (particle color) |
| **Pixelate** | Double Transform (scale way down then way up) creates blocky low-res look | `PixSmall` → `Size` (lower = more pixels); default is 6% scale |
| **Posterize** | Three stacked high-contrast ColorCorrectors crush tones into flat graphic bands | `Pass1/2/3` → `ContrastMaster` (more = harder posterize) |

---

## Transitions

Drag from **Effects → Video Transitions → Fusion Transitions** and drop **between two clips**.  
Resize the transition handle to control duration.

### Classic Transitions

| Name | Effect |
|---|---|
| **Dip to Black** | Both clips fade through black — the classic cinematic cut |
| **Dip to White** | Both clips fade through white — dreamlike or flashback feel |
| **Cross Blur** | Outgoing clip blurs out while incoming clip blurs in and dissolves |

### Anime / Viral Transitions

| Name | Effect | Anime usage |
|---|---|---|
| **Flash White** | Clip 1 fades to pure white, then clip 2 fades in from white — 20-frame burst | Power-up moments, impact hits, scene reveals |
| **Flash Black** | Same as Flash White but through black — more aggressive, 5-frame blackout then recovery | Fight cuts, dramatic chapter breaks |
| **Whip Pan Right** | Extreme horizontal motion blur on outgoing clip, reverse blur on incoming clip | Camera whip transitions between scenes |
| **Zoom Blur Cut** | Outgoing clip zooms out with blur, incoming clip zooms in from large — kinetic impact | Speed ramps, action sequence cuts |
| **Glitch Cut** | RGB channels split and shift horizontally with rapid oscillation — chromatic glitch on cut | Tech/cyber edits, hype montages, AMV cuts |

**Tip — Flash transitions:** Set the transition to exactly 20 frames (less than 1 second) for the snappiest anime look. Place on the edit point between an impact frame and the reaction shot.

### Additional Transitions

| Name | Effect |
|---|---|
| **Spin Rotate** | Both clips rotate and scale — clip 1 spins out, clip 2 spins in from opposite angle |
| **Slide Push Left** | Clip 1 pushes off-screen left as clip 2 enters from right — clean kinetic cut |
| **Circle Iris** | Circular mask grows from center revealing clip 2 — classic cinema iris |
| **Strobe Cut** | Rapidly alternates between both clips 5 times before settling on clip 2 |
| **Color Wipe** | Orange color bar sweeps left-to-right, revealing clip 2 behind it |
| **Pixel Scatter** | Clip 2 assembles from scattered noise pixels — digital reveal |
| **Flip Horizontal** | Clip 1 squishes and slides off, clip 2 snaps in — card-flip feel |
| **Light Leak** | Warm orange light streak sweeps across a standard dissolve — film photography look |

---

## Scripts

Run from **Workspace → Scripts** in any page. Output appears in the **Console** (Workspace → Console).

### Edit Page Scripts

| Script | What it does | How to use |
|---|---|---|
| **colorize_tracks** | Colors all video clips by track number — Track 1 = Orange, Track 2 = Yellow, etc. | Open a timeline → Workspace → Scripts → Edit → colorize_tracks |
| **add_interval_markers** | Adds blue chapter markers every 5 seconds across the whole timeline | Open a timeline → run script. Edit `INTERVAL_SECONDS` at the top of the file to change spacing |
| **insert_flash_frames** | Adds a white marker at the current playhead clip's start frame with instructions for inserting a flash | Place playhead on a clip → run script → follow console instructions to manually place a white Color generator at the marked cut |
| **beat_sync_prep** | Prints all timeline markers (beat reference points) and all V1 clip edit points with timecodes and frame numbers | Run before editing to a song. Copy the frame numbers into a spreadsheet or note to line up cuts with music beats |
| **auto_scene_markers** | Adds a Yellow marker at the start of every clip on V1 — creates an instant scene map | Open a timeline → run script. Rename the markers in the timeline to label scenes |
| **remove_all_markers** | Clears every marker from the timeline | Run after batch_add_effect or any marker workflow is done to clean up |
| **flag_short_clips** | Marks clips shorter than 6 frames Red — finds micro-clips before export | Edit `MIN_FRAMES` at top of file to change the threshold |
| **set_all_duration** | Checks every V1 clip against a target frame length — Green = matches, Orange = differs | Edit `TARGET_FRAMES` at top. Use for beat edits where every clip must be the same length |
| **batch_add_effect** | Adds Cyan markers at every V1 clip as reminders to manually apply a specific effect | Edit `EFFECT_NAME` at top; run remove_all_markers when done applying effects |
| **copy_grade_to_track** | Marks the first clip Green and prints all V1 clip names with grade copy keyboard shortcuts | Run on Color page; use Ctrl+C / Ctrl+V or Gallery stills to copy grades between clips |

### Utility Scripts

| Script | What it does | Output |
|---|---|---|
| **timeline_stats** | Prints duration, frame rate, track count, total clips, and marker count | Console |
| **find_gaps** | Scans all video tracks and lists every gap with its timecode and length | Console |
| **export_clip_list** | Exports every clip's name, in-point, and duration to a `.txt` file | `Desktop\clip_list.txt` |
| **youtube_chapters** | Converts all timeline markers into YouTube timestamp format (e.g. `0:45 Chapter 2`) | Console — copy-paste into YouTube description |
| **organize_media_pool** | Moves all clips in the root bin into **Video / Audio / Images / Other** sub-bins automatically | Media Pool |
| **duplicate_timeline** | Creates a copy of the current timeline named `<original> COPY` | Timeline panel |
| **rename_sequential** | Renames every video clip `Clip_001`, `Clip_002`, etc. left-to-right, top track first | Timeline |
| **clear_clip_colors** | Removes all clip color flags from every video clip in the timeline | Timeline |
| **export_markers_csv** | Exports all markers to a CSV file — Frame, Timecode, Color, Name, Note, Duration | `Desktop\markers_export.csv` |
| **count_clip_usage** | Counts how many times each clip name appears across all video tracks — finds overused/unused media | Console |

---

---

## Generators

Drag from **Effects → Generators** onto an empty track. These are animated backgrounds — place them on V1 (as a standalone background clip) or V2 (composited behind titles).

| Name | What it generates | Key controls in Fusion |
|---|---|---|
| **Animated Gradient** | Two-color linear gradient that slowly cycles through hue combinations over 180 frames | `R1/G1/B1` splines = top-left color over time; `R2/G2/B2` = bottom-right color |
| **Aurora Northern Lights** | Green + blue animated light ribbons on a dark navy sky — sweeping organic movement | `AuroraNoise` → `SeetheRate` (speed), `XScale`/`YScale` (ribbon size); `GreenShift` → channel Gain (colors) |
| **Electric Sparks** | Two layers of bright animated particle arcs on dark background — lightning/plasma feel | `SparkNoise1/2` → `SeetheRate` (spark speed), `Contrast` (density); channel Gain (colors) |
| **Glitch Bars** | Cyan + magenta horizontal noise bars that jump and drift — digital interference pattern | `GlitchNoise1/2` → `SeetheRate` (jump speed), `YScale` (bar height); `GlitchX` spline (horizontal shift) |
| **Starfield** | Three layers of static + slow-drifting star points on deep space background | `Stars1/2/3` → `Contrast`/`Brightness` (star density/size); `PanSpline` end value (pan speed) |

**Usage tip:** Drop any generator on V1, set its duration to match your sequence, then place titles from the Titles panel on V2 above it.

---

## Script Manager

The [manage-scripts.ps1](DaVinci_Tools/manage-scripts.ps1) tool lets you install or delete scripts interactively without touching Resolve's folders manually.

**Run it:**
```
powershell -ExecutionPolicy Bypass -File "DaVinci_Tools\manage-scripts.ps1"
```

**Menu options:**

| Option | What it does |
|---|---|
| `[1] List` | Shows all scripts currently installed in Resolve, numbered and grouped by folder |
| `[2] Install` | Shows all available scripts from the DaVinci_Tools source folders. Enter numbers like `1 3 5-8` or `all` |
| `[3] Delete` | Same numbered list as Install, but removes the selected scripts from Resolve. Cleans empty subfolders automatically |

---

## File Locations

All assets live inside DaVinci Resolve's user data folder:

```
%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\
├── Templates\Edit\
│   ├── Titles\          ← 44 templates: Base, Animated, 3D, Overlay, FX, Meme, Chat, etc.
│   ├── Transitions\     ← 16 transitions: classic + anime + spin/push/iris/wipe/scatter
│   ├── Effects\         ← 28 effects: cinematic + anime + color grades + overlays
│   └── Generators\      ← 5 generators: Gradient, Aurora, Sparks, Glitch, Starfield
└── Scripts\
    ├── Edit\            ← 10 edit scripts
    └── Utility\         ← 10 utility scripts
```

Source files (for editing and reinstalling) live in:
```
DaVinci_Tools\
├── DaVinci-Resolve-Scripts\   ← X-Raym Lua scripts
├── resolve-scripts\           ← General resolve Lua scripts
├── claude-resolve\            ← Claude AI workflow integration plugin
├── DaVinciResolve-DynamicText\ ← Python dynamic text tool
└── manage-scripts.ps1         ← Script manager
```

---

## Quick Start Workflow

1. **Color-code your tracks** → `colorize_tracks` so you can see what's what at a glance
2. **Find any holes** → `find_gaps` before you start finishing
3. **Add titles** → drag from Effects → Titles; double-click to edit text in Fusion
4. **Add atmosphere** → drop **Vignette** and **Soft Glow** on hero clips
5. **Smooth cuts** → drag **Cross Blur** or **Dip to Black** between clips
6. **Chapter markers** → `add_interval_markers` then edit names in the timeline
7. **Export for YouTube** → `youtube_chapters` → paste timestamps into description
8. **Organize media** → `organize_media_pool` to sort clips into bins before finishing

---

## Anime Edit Workflow

A step-by-step guide for creating viral anime-style edits using the installed presets.

### 1. Beat Prep
- Import your audio track to A1
- Run `add_interval_markers` to mark every 5 seconds as a rough guide
- Then manually add markers exactly on the music beats you want to cut to
- Run `beat_sync_prep` — copy the marker frame numbers and plan your cuts

### 2. Cut Rhythm
- Edit all your anime clips on V1 to the beat markers
- Keep impact frames (the hit/explosion peak frame) as short as 2–4 frames
- Run `colorize_tracks` after rough cut so tracks are color-coded

### 3. Add Impact Effects (on the key clip)
Stack these in this order on impact clips:
1. Drag **Screen Shake** onto the impact clip
2. Drag **Chromatic Aberration** onto the same clip (effects stack)
3. Place **FX Lens Flare Hit** on V2 directly above the cut point
4. (Optional) Place **FX Speed Lines** on V2 a few frames before the hit

### 4. Flash Transitions
- Between the impact clip and the next clip: drag **Flash White** or **Flash Black**
- Set transition duration to 12–20 frames
- For tech/cyberpunk AMVs: use **Glitch Cut** instead

### 5. Motion Transitions
- Between normal scene cuts: use **Whip Pan Right** (12–18 frames)
- For speed ramp moments: use **Zoom Blur Cut** (20 frames)

### 6. Color Grade
- Apply **Teal Orange Grade** on your hero clips for cinematic look
- Or use **High Contrast Grade** for raw punch
- Add **VHS Retro** on flashback/memory clips

### 7. Vignette Pulse
- On the climax or boss fight moment: drop **Vignette Pulse** on the clip
- It pulses the vignette rhythmically — feels like a heartbeat

### 8. Lower Thirds / Titles
- Character intros: **Anim Bounce In** (bold name) + **Lower Third Bold Line**
- Scene title cards: **Anim Zoom Fade Out** (fades out dramatically)
- Episode count: **Top Left Title**

### Recommended Effect Combinations

| Scene type | Effects to stack |
|---|---|
| Punch/kick landing | Screen Shake + Chromatic Aberration + Flash White transition |
| Speed burst | Zoom Punch + FX Speed Lines overlay + Zoom Blur Cut transition |
| Explosion | Screen Shake + FX Lens Flare Hit + High Contrast Grade |
| Flashback | VHS Retro + Soft Glow + Dip to White transition |
| Boss reveal | Vignette Pulse + High Contrast Grade + Flash Black transition |
| Power-up | Chromatic Aberration + Teal Orange Grade + FX Lens Flare Hit |
