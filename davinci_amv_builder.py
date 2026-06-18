"""
Onepiece AMV - DaVinci Resolve Timeline Builder
================================================
FROM DAVINCI CONSOLE (Workspace > Console > Py3):
  exec(open(r"D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing\davinci_amv_builder.py", encoding="utf-8").read(), globals())

FROM TERMINAL:
  cd "D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing"
  python davinci_amv_builder.py
"""

import os, sys, json
from pathlib import Path

# ── connection ────────────────────────────────────────────────────────────────
# Inline the same setup as _resolve_env.py so this works from both
# DaVinci's internal console (exec'd) and an external terminal.

BASE = Path(r"D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing")

os.environ.setdefault("RESOLVE_SCRIPT_API",
    r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting")
os.environ.setdefault("RESOLVE_SCRIPT_LIB",
    r"D:\DaVinci\fusionscript.dll")

_mod = os.path.join(os.environ["RESOLVE_SCRIPT_API"], "Modules")
if _mod not in sys.path:
    sys.path.insert(0, _mod)

import DaVinciResolveScript as _dvr
resolve = _dvr.scriptapp("Resolve")

if resolve is None:
    raise RuntimeError(
        "Cannot connect to DaVinci Resolve.\n"
        "Check: Preferences > System > General > External scripting using = Local\n"
        "Then restart DaVinci and try again."
    )

print("Connected:", resolve.GetProductName(), resolve.GetVersionString())

pm   = resolve.GetProjectManager()
proj = pm.GetCurrentProject()
if proj is None:
    raise RuntimeError("No project open in DaVinci. Open a project first.")
mp = proj.GetMediaPool()
print("Project:", proj.GetName())

# ── paths & data ──────────────────────────────────────────────────────────────

SRC   = BASE / "Sources"  / "Onepiece"
ANA   = BASE / "Output"   / "Onepiece" / "_analysis"
WORK  = BASE / "Output"   / "Onepiece" / "_edit_work"
AUDIO = BASE / "Sources"  / "Onepiece" / "Audio-1.mp3.mpeg"
WORK.mkdir(parents=True, exist_ok=True)

clips_data = json.loads((ANA / "_clips" / "Audio-1-clip-selection.json").read_text(encoding="utf-8"))
trans_data = json.loads((ANA / "_clips" / "Audio-1-transitions-effects.json").read_text(encoding="utf-8"))
subs_data  = json.loads((ANA / "_audio"  / "Audio-1-subtitles.json").read_text(encoding="utf-8"))
audio_data = json.loads((ANA / "_audio"  / "Audio-1-clip-analysis.json").read_text(encoding="utf-8"))
print("JSON loaded")

# ── constants ─────────────────────────────────────────────────────────────────

TIMELINE_NAME = "Onepiece AMV - Audio-1"
FPS           = 60
W, H          = 1920, 1080
AUDIO_DUR     = audio_data["total_duration_seconds"]

def s2f(sec): return int(round(sec * FPS))

SEG_COLOR = {1:"Orange", 2:"Orange", 3:"Cyan",
             4:"Yellow", 5:"Pink",   6:"Blue", 7:"Green"}

SEG_GRADE = {
    1: "Warm: Temp+10, Sat+8%, Vignette 20%, Fade-in 0.6s from Black",
    2: "Warm continued: Temp+10, Sat+8%, Vignette 20%",
    3: "Cool neutral: Temp-5, Motion-blur cuts, Zoom +3% per clip",
    4: "Sepia: Temp+15, Desat 25%, Bloom 20%, 80% speed",
    5: "Golden: Temp+18, Sat+15%, +0.3EV, Bloom 25%",
    6: "Sad1-5: Desat55% Temp-20 Vig45% 60%spd FilmGrain25% | Pre-TS6-19: Desat25% Temp-20 HardCuts",
    7: "Bright warm: Temp+15, Sat+12%, +0.4EV, Bloom 30%, Vignette 15->0%, 80%spd clips3-5",
}

TRANSITION_NOTES = {
    1: "Cross Dissolve 0.5s | Seg1->Seg2 | @6.74s",
    2: "Fade-to-Black 0.5s OUT -> Hold 0.3s -> Fade-from-Black 0.5s | Seg2->Seg3 | @13.44s",
    3: "Motion Blur Wipe Horizontal 0.4s | Seg3->Seg4 | @20.14s",
    4: "MAJOR BREAK: Fade-to-Black 0.8s OUT -> Hold 1.8s -> Fade-from-Black 0.8s | Seg4->Seg5 | @26.12s",
    5: "Fade-to-Black 0.6s OUT -> Hold 0.4s -> Fade-from-Black 0.6s | Seg5->Seg6 | @33.88s",
    6: "Dip-to-White FLASH: 0.25s OUT -> 0.1s hold -> 0.3s IN | Seg6->Seg7 | @45.88s",
    7: "Fade-to-White 3.0s | End | @51.06s",
}

def get_speed(seg_id, order, folder):
    if seg_id == 4: return 0.80
    if seg_id == 6 and folder == "Sad": return 0.60
    if seg_id == 7 and order >= 3: return 0.80
    return 1.0

# ── project settings ──────────────────────────────────────────────────────────

proj.SetSetting("timelineResolutionWidth",  str(W))
proj.SetSetting("timelineResolutionHeight", str(H))
proj.SetSetting("timelineFrameRate",        str(float(FPS)))
print(f"Project: {W}x{H} @ {FPS}fps")

# ── bins ──────────────────────────────────────────────────────────────────────

def _bin(parent, name):
    for sub in (parent.GetSubFolderList() or []):
        if sub.GetName() == name:
            return sub
    return mp.AddSubFolder(parent, name)

root_folder = mp.GetRootFolder()
amv_bin  = _bin(root_folder, "Onepiece AMV")
vid_bin  = _bin(amv_bin, "Video")
aud_bin  = _bin(amv_bin, "Audio")
sub_bin  = _bin(amv_bin, "Subtitles")
seg_bins = {seg["segment_id"]: _bin(vid_bin, f"Seg{seg['segment_id']} - {seg['label']}")
            for seg in clips_data["segments"]}
print(f"Bins: Seg1-Seg{len(seg_bins)} ready")

# ── find clip anywhere in pool ────────────────────────────────────────────────

def find_clip(name):
    stack = [mp.GetRootFolder()]
    while stack:
        fol = stack.pop()
        for c in (fol.GetClipList() or []):
            if c.GetName() == name:
                return c
        stack.extend(fol.GetSubFolderList() or [])
    return None

# ── import audio ──────────────────────────────────────────────────────────────

mp.SetCurrentFolder(aud_bin)
audio_media = find_clip(AUDIO.name)
if audio_media is None:
    imported = mp.ImportMedia([str(AUDIO)]) or []
    audio_media = imported[0] if imported else None
print("Audio:", audio_media.GetName() if audio_media else "FAILED")

# ── import video clips per segment ────────────────────────────────────────────

path_to_media = {}

for seg in clips_data["segments"]:
    seg_id = seg["segment_id"]
    mp.SetCurrentFolder(seg_bins[seg_id])
    to_import = []
    for clip in seg["selected_clips"]:
        fp = str(BASE / clip["path"])
        existing = find_clip(Path(fp).name)
        if existing:
            path_to_media[fp] = existing
        elif Path(fp).exists():
            to_import.append(fp)
        else:
            print(f"  MISSING: {clip['filename']}")
    if to_import:
        for item in (mp.ImportMedia(to_import) or []):
            try:
                path_to_media[item.GetClipProperty("File Path")] = item
            except Exception:
                pass
    print(f"  Seg{seg_id}: done")

# ── ordered clip list ─────────────────────────────────────────────────────────

clips = []
for seg in clips_data["segments"]:
    for c in seg["selected_clips"]:
        fp = str(BASE / c["path"])
        mi = path_to_media.get(fp) or find_clip(Path(fp).name)
        clips.append({
            "seg_id":   seg["segment_id"],
            "order":    c["order"],
            "folder":   c["folder"],
            "filename": c["filename"],
            "duration": c["duration_seconds"],
            "speed":    get_speed(seg["segment_id"], c["order"], c["folder"]),
            "mi":       mi,
        })

missing = sum(1 for c in clips if c["mi"] is None)
print(f"Clips: {len(clips)} total, {missing} missing")

# ── create / replace timeline ─────────────────────────────────────────────────

for i in range(1, proj.GetTimelineCount() + 1):
    t = proj.GetTimelineByIndex(i)
    if t and t.GetName() == TIMELINE_NAME:
        print(f"Removing old: {TIMELINE_NAME}")
        mp.DeleteTimelines([t])
        break

mp.SetCurrentFolder(vid_bin)
tl = mp.CreateEmptyTimeline(TIMELINE_NAME)
if tl is None:
    raise RuntimeError("Could not create timeline.")
proj.SetCurrentTimeline(tl)

while tl.GetTrackCount("video") < 2:
    tl.AddTrack("video")
print(f"Timeline created: {W}x{H}@{FPS}fps  V={tl.GetTrackCount('video')}")

# ── place clips on V1 ─────────────────────────────────────────────────────────

payload = []
for c in clips:
    if c["mi"] is None:
        print(f"  SKIP: Seg{c['seg_id']} order {c['order']}")
        continue
    try:
        src_fps = float(c["mi"].GetClipProperty("FPS") or 0)
    except Exception:
        src_fps = 0.0
    if src_fps <= 0:
        src_fps = 191.0
    end_frame = max(0, int(round(c["duration"] * src_fps)) - 1)
    payload.append({
        "mediaPoolItem": c["mi"],
        "startFrame":    0,
        "endFrame":      end_frame,
        "trackIndex":    1,
        "mediaType":     1,
    })

placed = mp.AppendToTimeline(payload) or []
print(f"V1: {len(placed)}/{len(payload)} clips placed")

# ── speed changes ─────────────────────────────────────────────────────────────

tl_items = tl.GetItemListInTrack("video", 1) or []
speed_n   = 0
if len(tl_items) == len(clips):
    for c, item in zip(clips, tl_items):
        if c["speed"] != 1.0:
            try:
                item.SetProperty("Speed", c["speed"] * 100.0)
                speed_n += 1
            except Exception:
                pass
    print(f"Speed: {speed_n} clips adjusted")
else:
    print(f"Speed: item count mismatch ({len(tl_items)} vs {len(clips)}) - set manually")
    print("  Seg4 all -> 80%  |  Seg6 Sad clips -> 60%  |  Seg7 clips3-5 -> 80%")

# ── clip colours ──────────────────────────────────────────────────────────────

tl_items = tl.GetItemListInTrack("video", 1) or []
for c, item in zip(clips, tl_items):
    try:
        item.SetClipColor(SEG_COLOR.get(c["seg_id"], "Beige"))
    except Exception:
        pass
print("Clip colours applied")

# ── audio on A1 ───────────────────────────────────────────────────────────────

if audio_media:
    r = mp.AppendToTimeline([{
        "mediaPoolItem": audio_media,
        "startFrame":    0,
        "endFrame":      s2f(AUDIO_DUR) - 1,
        "trackIndex":    1,
        "mediaType":     2,
    }])
    print("Audio A1:", "OK" if r else "FAILED - add manually")

# ── SRT file ──────────────────────────────────────────────────────────────────

def _t(sec):
    h=int(sec//3600); m=int((sec%3600)//60); s=int(sec%60)
    ms=int(round((sec-int(sec))*1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

srt = WORK / "onepiece_amv_captions.srt"
lines = []
for i, sg in enumerate(subs_data["segments"], 1):
    lines += [str(i), f"{_t(sg['start'])} --> {_t(sg['end'])}", sg["text"], ""]
srt.write_text("\n".join(lines), encoding="utf-8")
print(f"SRT: {srt.name}")

# ── markers ───────────────────────────────────────────────────────────────────

# Red = transitions
for tr in trans_data["between_segment_transitions"]:
    tl.AddMarker(s2f(tr["position_seconds"]), "Red",
                 f"T{tr['transition_id']}: {tr['transition_type']}",
                 TRANSITION_NOTES.get(tr["transition_id"], ""), 1)

# Blue = colour grades
for se in trans_data["segment_effects"]:
    sid = se["segment_id"]
    tl.AddMarker(s2f(se["time_range"]["start"]), "Blue",
                 f"S{sid}: {se['label']}",
                 f"GRADE: {SEG_GRADE.get(sid,'')}",
                 max(1, s2f(se["time_range"]["end"] - se["time_range"]["start"])))

# Purple = Fusion / effects
for t0, t1, note in [
    (0.0,   1.0,   "Fade-in 0.6s from Black - keyframe Opacity on clip 1"),
    (17.28, 20.14, "Seg3 ZOOM: Transform > Zoom 100->103% per Luffy clip"),
    (22.60, 26.12, "Seg4 BLOOM: Fusion Glow 20% wide on Kid clips"),
    (31.46, 33.88, "Seg5 BLOOM: Fusion Glow 25% highlights on Smile clips"),
    (37.76, 45.88, "Seg6 FILM GRAIN 25% on Sad clips 1-5 in Color page"),
    (48.26, 54.60, "Seg7 BLOOM 30% + Vignette 15->0% + Dissolve-to-White 2.5s on last clip"),
]:
    tl.AddMarker(s2f(t0), "Purple", f"FX@{t0:.1f}s", note, max(1, s2f(t1 - t0)))

# Yellow = global setup at frame 0
tl.AddMarker(0, "Yellow", "GLOBAL SETUP",
    "Letterbox -> Project Settings > Output Blanking > 2.40:1 | "
    "Film Grain -> Color > Texture > Film Grain 12% | "
    "SRT -> File > Import > Subtitle (onepiece_amv_captions.srt)", 1)

print("Markers: 7 Red + 7 Blue + 6 Purple + 1 Yellow")

pm.SaveProject()
print("Project saved.")

# ── summary ───────────────────────────────────────────────────────────────────

print(f"""
=================================================================
  ONEPIECE AMV - DAVINCI TIMELINE BUILT
=================================================================
  Clips on V1 : {len(placed)}
  Audio on A1 : {AUDIO_DUR:.2f}s
  Markers     : 7 Red  7 Blue  6 Purple  1 Yellow
  SRT         : Output/Onepiece/_edit_work/onepiece_amv_captions.srt
-----------------------------------------------------------------
  TRANSITIONS (Red markers - Edit page)
  T1  6.74s  Cross Dissolve 0.5s
  T2 13.44s  Fade Black 0.5+0.3+0.5s
  T3 20.14s  Motion Blur Wipe H 0.4s
  T4 26.12s  Fade Black 0.8+1.8+0.8s  *** MAJOR BREAK ***
  T5 33.88s  Fade Black 0.6+0.4+0.6s
  T6 45.88s  Dip-to-White flash
  T7 51.06s  Fade to White 3.0s
-----------------------------------------------------------------
  COLOUR GRADES (Blue markers - Color page)
  Orange Seg1-2  Warm  Temp+10  Sat+8%  Vignette20%
  Cyan   Seg3    Cool  Temp-5
  Yellow Seg4    Sepia Temp+15  Desat25%  Bloom20%
  Pink   Seg5    Gold  Temp+18  Sat+15%  +0.3EV  Bloom25%
  Blue   Seg6    Sad: Desat55% Temp-20 Vig45% | Supp: Desat25%
  Green  Seg7    Warm  Temp+15  Sat+12%  +0.4EV  Bloom30%
-----------------------------------------------------------------
  WITHIN-SEGMENT (Edit page)
  Seg1: Dissolve 0.1s clips1->2 only
  Seg2: Hard Cut all
  Seg3: Hard Cut all (rapid luffy cuts)
  Seg4: Dissolve 0.2s Kid clips
  Seg5: Dissolve 0.25s Smile clips
  Seg6: Dissolve 0.15s Sad1-5 | Hard Cut Pre-TS 6-19
  Seg7: Hard Cut clips1-4 | Last clip -> Dissolve-to-White 2.5s
-----------------------------------------------------------------
  GLOBAL (Yellow marker frame 0)
  Letterbox  Project Settings > Output Blanking > 2.40:1
  FilmGrain  Color > Texture > Film Grain 12%
  Subtitles  File > Import > Subtitle
=================================================================
""")
