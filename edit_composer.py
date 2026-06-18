"""
edit_composer.py — Onepiece AMV full edit composer

Layer order (bottom → top):
  Layer 1 — Base clips   : source video, color graded, speed adjusted
  Layer 2 — Text/Captions: ASS karaoke subtitles burned onto Layer 1
  Layer 3 — Characters   : nobg WebM overlaid on top with alpha

Audio: Audio-1.mp3.mpeg (all source clip audio muted)

Output: Output/Onepiece/Audio-1-edit.mp4
"""

import sys, json, subprocess, shutil, re
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE      = Path(r"D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing")
ANA       = BASE / "Output/Onepiece/_analysis"
NOBG_ROOT = BASE / "Output/Onepiece/_nobg"
SRC_ROOT  = BASE / "Sources/Onepiece"
AUDIO_SRC = SRC_ROOT / "Audio-1.mp3.mpeg"
WORK_DIR  = BASE / "Output/Onepiece/_edit_work"
OUT_VIDEO = BASE / "Output/Onepiece/Audio-1-edit.mp4"

OUT_W, OUT_H = 1920, 1080
OUT_FPS      = 60
LB_H         = int(OUT_W / 2.39)        # 803px active height (2.39:1 letterbox)
LB_PAD       = (OUT_H - LB_H) // 2     # 138px black bars top + bottom

WORK_DIR.mkdir(parents=True, exist_ok=True)

# ── Load JSON ──────────────────────────────────────────────────────────────────
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

clips_data = load(ANA / "_clips/Audio-1-clip-selection.json")
trans_data = load(ANA / "_clips/Audio-1-transitions-effects.json")
capts_data = load(ANA / "_clips/Audio-1-captions-layer.json")

# ── Utilities ──────────────────────────────────────────────────────────────────
def ffrun(cmd, desc):
    print(f"  ▶ {desc}")
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        err = r.stderr.decode(errors="replace")
        print(f"  ✗ FAILED:\n{err[-800:]}")
    return r.returncode == 0

def probe_dur(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:    return float(r.stdout.strip())
    except: return 0.0

def lslug(s):   return re.sub(r"[^\w]+", "-", s).strip("-")
def fslug(s):   return s.lower().replace(" ", "-")
def nslug(fn):
    s = Path(fn).stem
    s = re.sub(r"\[.*?\]", "", s)
    s = re.sub(r"[().]", "-", s)
    s = re.sub(r"[^\w-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s.lower() or "clip"

def nobg_path(sid, slbl, order, folder, fn):
    d = NOBG_ROOT / f"Seg{sid}_{lslug(slbl)}"
    return d / f"clip_{order:02d}_{fslug(folder)}_{nslug(fn)}_nobg.webm"

# ── Grade filters ──────────────────────────────────────────────────────────────
# base_grade: applied to source clip (Layer 1) — includes scale, grade, vignette
# char_grade: applied to nobg clip (Layer 3) — includes scale, grade (no vignette, preserves alpha)

# Use decrease+pad for both layers — avoids odd-dimension issues from increase+crop
SCALE_BASE = (f"scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=decrease,"
              f"pad={OUT_W}:{OUT_H}:(ow-iw)/2:(oh-ih)/2")
SCALE_CHAR = (f"scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=decrease,"
              f"pad={OUT_W}:{OUT_H}:(ow-iw)/2:(oh-ih)/2")

def grade(seg_id, folder):
    """Color grade using eq + colorbalance (no curves — avoids Windows quoting issues)."""
    if seg_id in (1, 2):
        # Warm: boost red/green, cut blue, +8% sat
        return "eq=brightness=0.02:saturation=1.08,colorbalance=rs=0.04:rm=0.04:rh=0.03:bs=-0.04:bm=-0.04:bh=-0.03"
    if seg_id == 3:
        # Cool neutral: slight red cut, blue boost, -5% sat
        return "eq=saturation=0.95,colorbalance=rs=-0.02:rm=-0.02:bs=0.02:bm=0.02"
    if seg_id == 4:
        # Sepia/warm amber: strong red boost, blue cut, -25% sat
        return "eq=saturation=0.75:brightness=0.01,colorbalance=rs=0.06:rm=0.05:rh=0.04:bs=-0.07:bm=-0.06:bh=-0.05"
    if seg_id == 5:
        # Golden warm: strong red/green boost, blue cut, +15% sat
        return "eq=brightness=0.05:saturation=1.15,colorbalance=rs=0.07:rm=0.06:rh=0.05:gs=0.02:gm=0.02:bs=-0.08:bm=-0.07:bh=-0.06"
    if seg_id == 6:
        if folder == "Sad":
            # Heavy desaturate + cool blue
            return "eq=saturation=0.45,colorbalance=rs=-0.08:rm=-0.07:rh=-0.06:bs=0.09:bm=0.08:bh=0.07"
        # Moderate desaturate + cool blue
        return "eq=saturation=0.75,colorbalance=rs=-0.05:rm=-0.04:rh=-0.03:bs=0.06:bm=0.05:bh=0.04"
    if seg_id == 7:
        # Bright warm: boost red/green, cut blue, +12% sat
        return "eq=brightness=0.06:saturation=1.12,colorbalance=rs=0.06:rm=0.05:rh=0.04:gs=0.01:gm=0.01:bs=-0.07:bm=-0.06:bh=-0.05"
    return ""

def vignette(seg_id, folder):
    """Vignette filter (Layer 1 only)."""
    if seg_id in (1, 2):    return "vignette=angle=PI/5"
    if seg_id == 6:         return "vignette=angle=PI/3"
    if seg_id == 7:         return "vignette=angle=PI/6"
    return ""

def speed(seg_id, order, folder):
    if seg_id == 4:                     return 0.80
    if seg_id == 6 and folder == "Sad": return 0.60
    if seg_id == 7 and order >= 3:     return 0.80
    return 1.0

def base_vf(seg_id, order, folder):
    """Full vf string for Layer 1 (source clip)."""
    spd   = speed(seg_id, order, folder)
    pts   = f"setpts={1/spd:.4f}*PTS"
    parts = [pts, SCALE_BASE, grade(seg_id, folder)]
    vig   = vignette(seg_id, folder)
    if vig: parts.append(vig)
    parts.append(f"fps={OUT_FPS}")
    return ",".join(p for p in parts if p)

def char_vf(seg_id, order, folder):
    """Full vf string for Layer 3 (nobg WebM, alpha preserved).
    No color grade here — eq/curves don't support yuva420p.
    Grade lives on Layer 1 (base). Character stays natural on top.
    """
    spd   = speed(seg_id, order, folder)
    pts   = f"setpts={1/spd:.4f}*PTS"
    parts = [pts, SCALE_CHAR, f"fps={OUT_FPS}"]
    return ",".join(p for p in parts if p)

# ── Phase 1 — Pre-process every clip into two intermediates ────────────────────
print("=" * 65)
print("PHASE 1 — Pre-processing clips")
print("  base_*.mp4  -> Layer 1 (source, graded, no alpha)")
print("  char_*.webm -> Layer 3 (nobg, graded, alpha preserved)")
print("=" * 65)

base_clips = []   # [{path, duration, seg_id, order, folder}, ...]
char_clips = []   # same shape, webm with alpha

for seg in clips_data["segments"]:
    sid  = seg["segment_id"]
    slbl = seg["label"]

    for clip in seg["selected_clips"]:
        order  = clip["order"]
        folder = clip["folder"]
        fn     = clip["filename"]
        src    = BASE / clip["path"]
        nobg   = nobg_path(sid, slbl, order, folder, fn)

        slug = f"s{sid:02d}_c{order:02d}_{fslug(folder)}_{nslug(fn)}"
        base_out = WORK_DIR / f"base_{slug}.mp4"
        char_out = WORK_DIR / f"char_{slug}.webm"

        # ── Layer 1: base clip ────────────────────────────────────────────────
        if base_out.exists():
            print(f"  SKIP base [{sid}/{order}]")
        else:
            print(f"\n  [{sid}/{order}] {folder} | {fn}")
            ok = ffrun([
                "ffmpeg", "-y", "-i", str(src),
                "-vf", base_vf(sid, order, folder),
                "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-an",
                str(base_out)
            ], f"Layer1 base_{slug}.mp4")
            if not ok:
                print("  ✗ base clip failed — skipping pair")
                continue

        base_clips.append({
            "path": base_out, "duration": probe_dur(base_out),
            "seg_id": sid, "order": order, "folder": folder
        })

        # ── Layer 3: character (nobg, alpha preserved) ────────────────────────
        if char_out.exists():
            print(f"  SKIP char [{sid}/{order}]")
        elif not nobg.exists():
            # Fallback: fully transparent black clip matching base duration
            print(f"  WARN nobg missing — transparent gap for [{sid}/{order}]")
            dur = probe_dur(base_out)
            ok  = ffrun([
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"color=c=black@0:size={OUT_W}x{OUT_H}:rate={OUT_FPS}",
                "-t", str(dur),
                "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "30",
                str(char_out)
            ], f"Layer3 transparent gap [{sid}/{order}]")
        else:
            spd   = speed(sid, order, folder)
            ok = ffrun([
                "ffmpeg", "-y", "-i", str(nobg),
                "-vf", char_vf(sid, order, folder),
                "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p",
                "-b:v", "0", "-crf", "18", "-an",
                str(char_out)
            ], f"Layer3 char_{slug}.webm")
            if not ok:
                print("  ✗ char clip failed")
                continue

        char_clips.append({
            "path": char_out, "duration": probe_dur(char_out),
            "seg_id": sid, "order": order, "folder": folder
        })

print(f"\nPhase 1: {len(base_clips)} base clips, {len(char_clips)} char clips")

# ── Phase 2 — Build shared timeline structure ──────────────────────────────────
print("\n" + "=" * 65)
print("PHASE 2 — Building timeline")
print("=" * 65)

seg_base = defaultdict(list)
seg_char = defaultdict(list)
for c in base_clips: seg_base[c["seg_id"]].append(c)
for c in char_clips: seg_char[c["seg_id"]].append(c)
for d in (seg_base, seg_char):
    for sid in d: d[sid].sort(key=lambda x: x["order"])

trans_by_seg = {t["from_segment"]: t
                for t in trans_data["between_segment_transitions"]
                if isinstance(t.get("from_segment"), int)}

def make_gap_clip(dur, name, color="black", alpha=False):
    out = WORK_DIR / name
    if out.exists(): return out
    if alpha:
        # Transparent (alpha=0) WebM gap for Layer 3
        ffrun([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"color=c=black@0:size={OUT_W}x{OUT_H}:rate={OUT_FPS}",
            "-t", str(dur),
            "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "30",
            str(out)
        ], f"Transparent gap {name}")
    else:
        ffrun([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"color=c={color}:size={OUT_W}x{OUT_H}:rate={OUT_FPS}",
            "-t", str(dur),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            str(out)
        ], f"Solid gap {name}")
    return out

def build_timeline(clips_by_seg, is_char=False):
    """Build an ordered clip list with xfade metadata and gap clips inserted."""
    tl = []
    for seg_num in range(1, 8):
        clips = clips_by_seg.get(seg_num, [])
        if not clips:
            print(f"  WARNING: no {'char' if is_char else 'base'} clips for seg {seg_num}")
            continue

        within = next((w for w in trans_data["within_segment_transitions"]
                       if w["segment_id"] == seg_num), None)
        within_dur = 0.0
        if within:
            within_dur = within.get("duration_seconds", 0) or within.get("duration_seconds_sad", 0)

        for i, c in enumerate(clips):
            is_last    = (i == len(clips) - 1)
            xfade_type = None
            xfade_dur  = 0.0

            # Between-segment cross dissolve on last clip
            if is_last and seg_num in trans_by_seg:
                t  = trans_by_seg[seg_num]
                tt = t["transition_type"]
                if "Cross Dissolve" in tt:
                    xfade_type = "dissolve"
                    xfade_dur  = t.get("duration_seconds", 0.5)

            # Within-segment dissolve on non-last clips
            if not is_last and within_dur > 0:
                xfade_type = "dissolve"
                xfade_dur  = within_dur

            tl.append({
                "file":       c["path"],
                "duration":   c["duration"],
                "xfade_next": xfade_type,
                "xfade_dur":  xfade_dur,
            })

        # Between-segment gap
        if seg_num < 7 and seg_num in trans_by_seg:
            t  = trans_by_seg[seg_num]
            tt = t["transition_type"]

            if "Cross Dissolve" in tt:
                gap = t["silence_gap_seconds"] - t.get("duration_seconds", 0.5)
                if gap > 0.05:
                    name = f"gap_s{seg_num}_{'char' if is_char else 'base'}.{'webm' if is_char else 'mp4'}"
                    gc   = make_gap_clip(gap, name, alpha=is_char)
                    tl.append({"file": gc, "duration": gap, "xfade_next": "dissolve", "xfade_dur": 0.3})

            elif "Fade to Black" in tt or "Fade to Black (Hold)" in tt:
                fade_out = t.get("fade_out_duration_seconds", 0.5)
                fade_in  = t.get("fade_in_duration_seconds", 0.5)
                black_dur = t["silence_gap_seconds"] - fade_out - fade_in
                if black_dur > 0.05:
                    name = f"gap_s{seg_num}_hold_{'char' if is_char else 'base'}.{'webm' if is_char else 'mp4'}"
                    gc   = make_gap_clip(black_dur, name, alpha=is_char)
                    tl.append({"file": gc, "duration": black_dur, "xfade_next": None, "xfade_dur": 0})

            elif "Dip to White" in tt or "Flash" in tt:
                hold_w   = t.get("hold_white_seconds", 0.1)
                fade_in  = t.get("fade_in_duration_seconds", 0.3)
                w_dur    = hold_w + 0.05
                name     = f"gap_s{seg_num}_white_{'char' if is_char else 'base'}.{'webm' if is_char else 'mp4'}"
                color    = "white" if not is_char else "black"
                gc       = make_gap_clip(w_dur, name, color=color, alpha=is_char)
                tl.append({"file": gc, "duration": w_dur, "xfade_next": "dissolve", "xfade_dur": fade_in})

    return tl

base_tl = build_timeline(seg_base, is_char=False)
char_tl = build_timeline(seg_char, is_char=True)
print(f"  Base timeline: {len(base_tl)} entries")
print(f"  Char timeline: {len(char_tl)} entries")

# ── Phase 3 — Assemble each layer independently ────────────────────────────────
print("\n" + "=" * 65)
print("PHASE 3 — Assembling Layer 1 (base) and Layer 3 (characters)")
print("=" * 65)

def assemble(timeline, out_path, label, is_char=False):
    """Chain all clips with xfade transitions → single assembled video."""
    if out_path.exists():
        print(f"  SKIP {label} (exists)")
        return True

    n = len(timeline)
    if n == 0:
        print(f"  ERROR: empty timeline for {label}")
        return False
    if n == 1:
        shutil.copy(str(timeline[0]["file"]), str(out_path))
        return True

    input_flags  = []
    filter_parts = []
    for entry in timeline:
        input_flags += ["-i", str(entry["file"])]

    prev_label  = "0:v"
    running_dur = timeline[0]["duration"]

    for i in range(1, n):
        cur  = f"{i}:v"
        out  = f"v{i}"
        xt   = timeline[i-1]["xfade_next"]
        xd   = timeline[i-1]["xfade_dur"]

        if xt and xd > 0 and running_dur > xd:
            offset = max(0.0, running_dur - xd)
            filter_parts.append(
                f"[{prev_label}][{cur}]xfade=transition={xt}:"
                f"duration={xd:.3f}:offset={offset:.3f}[{out}]"
            )
            running_dur += timeline[i]["duration"] - xd
        else:
            offset = max(0.0, running_dur - 0.001)
            filter_parts.append(
                f"[{prev_label}][{cur}]xfade=transition=fade:"
                f"duration=0.001:offset={offset:.3f}[{out}]"
            )
            running_dur += timeline[i]["duration"]

        prev_label = out

    # Fade in from black at start
    filter_parts.append(f"[{prev_label}]fade=t=in:st=0:d=0.6[fi]")
    # Fade to white at end
    fade_out_start = running_dur - 3.0
    filter_parts.append(f"[fi]fade=t=out:st={fade_out_start:.3f}:d=3.0:color=white[fo]")

    if not is_char:
        # Letterbox bars only on base layer
        filter_parts.append(
            f"[fo]drawbox=x=0:y=0:w={OUT_W}:h={LB_PAD}:color=black@1:t=fill,"
            f"drawbox=x=0:y={OUT_H-LB_PAD}:w={OUT_W}:h={LB_PAD}:color=black@1:t=fill[out]"
        )
        map_label = "[out]"
        enc = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", str(OUT_FPS), "-an"]
    else:
        map_label = "[fo]"
        enc = ["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p",
               "-b:v", "0", "-crf", "16", "-r", str(OUT_FPS), "-an"]

    filter_str = ";".join(filter_parts)
    cmd = (["ffmpeg", "-y"] + input_flags +
           ["-filter_complex", filter_str,
            "-map", map_label] + enc + [str(out_path)])

    return ffrun(cmd, f"Assemble {label}")

base_assembled = WORK_DIR / "base_assembled.mp4"
char_assembled = WORK_DIR / "chars_assembled.webm"

assemble(base_tl, base_assembled, "Layer1 base", is_char=False)
assemble(char_tl, char_assembled, "Layer3 chars", is_char=True)

# ── Phase 4 — Generate ASS karaoke subtitles (Layer 2) ───────────────────────
print("\n" + "=" * 65)
print("PHASE 4 — Generating ASS karaoke subtitles (Layer 2)")
print("=" * 65)

ass_file = WORK_DIR / "captions.ass"

def hex_to_ass(hx, alpha=0):
    h = hx.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"&H{alpha:02X}{b:02X}{g:02X}{r:02X}"

def ts(sec):
    h  = int(sec // 3600)
    m  = int((sec % 3600) // 60)
    s  = int(sec % 60)
    cs = int((sec - int(sec)) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

lines = [
    "[Script Info]", "ScriptType: v4.00+",
    f"PlayResX: {OUT_W}", f"PlayResY: {OUT_H}",
    "WrapStyle: 2", "",
    "[V4+ Styles]",
    "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,"
    "OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,"
    "ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,"
    "Alignment,MarginL,MarginR,MarginV,Encoding"
]

margin_v = LB_PAD + 40

for cap in capts_data["captions"]:
    cid    = cap["caption_id"]
    st     = cap["style"]
    italic = 1 if st.get("font_style") == "italic" else 0
    lines.append(
        f"Style: Cap{cid},Montserrat,{st['font_size_px']},"
        f"{hex_to_ass(st['base_color'])},{hex_to_ass(st['highlight_color'])},"
        f"&H80000000,&H00000000,-1,{italic},0,0,"
        f"100,100,1,0,1,2,2,2,80,80,{margin_v},1"
    )

lines += ["", "[Events]",
          "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"]

for cap in capts_data["captions"]:
    cid    = cap["caption_id"]
    st     = cap["style"]
    words  = cap["word_highlights"]
    base_c = hex_to_ass(st["base_color"])
    hi_c   = hex_to_ass(st["highlight_color"])

    special = set()
    if "special_word_highlight" in cap:
        sw = cap["special_word_highlight"]
        if isinstance(sw.get("word"), str):   special.add(sw["word"])
        if isinstance(sw.get("words"), list): special.update(sw["words"])

    by_line = defaultdict(list)
    for w in words: by_line[w["line"]].append(w)

    fin_ms  = int(cap.get("animation_in",  {}).get("duration_seconds", 0.3) * 1000)
    fout_ms = int(cap.get("animation_out", {}).get("duration_seconds", 0.3) * 1000)
    fade    = f"{{\\fad({fin_ms},{fout_ms})}}"

    for ln in sorted(by_line):
        ln_words = by_line[ln]
        txt = ""
        for w in ln_words:
            dur_cs = int((w["active_end"] - w["active_start"]) * 100)
            color  = hi_c if w["word"] in special else base_c
            txt   += f"{{\\1c{color}\\kf{dur_cs}}}{w['word']} "
        txt = txt.rstrip()
        lines.append(
            f"Dialogue: 0,{ts(cap['display_start'])},{ts(cap['display_end'])},"
            f"Cap{cid},,0,0,0,,{fade}{txt}"
        )

ass_file.write_text("\n".join(lines), encoding="utf-8-sig")
print(f"  Written: {ass_file.name}  ({len(capts_data['captions'])} caption blocks)")

# ── Phase 5 — Final composite: L1 + L2 (captions) + L3 (chars) + audio ────────
print("\n" + "=" * 65)
print("PHASE 5 — Final composite")
print("  [Layer 1] base_assembled.mp4")
print("  [Layer 2] captions.ass  ← burned onto Layer 1")
print("  [Layer 3] chars_assembled.webm  ← overlaid on top")
print("  [Audio  ] Audio-1.mp3.mpeg")
print("=" * 65)

if not base_assembled.exists():
    print("  ERROR: base_assembled.mp4 missing — Phase 3 failed.")
elif not char_assembled.exists():
    print("  ERROR: chars_assembled.webm missing — Phase 3 failed.")
else:
    # Use relative path for captions.ass — avoids Windows drive colon issue in
    # FFmpeg filter_complex where ':' is the option separator
    fc = (
        f"[0:v]ass=captions.ass[l12];"
        f"[l12][1:v]overlay=format=auto[out];"
        f"[2:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(base_assembled),   # input 0 — Layer 1
        "-i", str(char_assembled),   # input 1 — Layer 3
        "-i", str(AUDIO_SRC),        # input 2 — audio
        "-filter_complex", fc,
        "-map", "[out]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "15",
        "-c:a", "aac", "-b:a", "320k",
        "-r", str(OUT_FPS),
        "-movflags", "+faststart",
        str(OUT_VIDEO)
    ]

    print("  ▶ Final render (L1 + L2 + L3 + audio)")
    r = subprocess.run(cmd, capture_output=True, cwd=str(WORK_DIR))
    if r.returncode != 0:
        err = r.stderr.decode(errors="replace")
        print(f"  ✗ FAILED:\n{err[-800:]}")
    ok = (r.returncode == 0)
    if ok:
        size_mb = OUT_VIDEO.stat().st_size / (1024 * 1024)
        dur     = probe_dur(OUT_VIDEO)
        print(f"\n{'=' * 65}")
        print(f"  DONE  →  {OUT_VIDEO}")
        print(f"  Size  :  {size_mb:.1f} MB")
        print(f"  Length:  {dur:.2f}s")
        print(f"{'=' * 65}")
    else:
        print("  Final render FAILED.")
