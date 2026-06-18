"""
Batch background removal — rembg isnet-anime (DirectML GPU)
Processes all 45 selected clips from Audio-1-clip-selection.json
Output: Output/Onepiece/_nobg/Seg{N}_{Label}/{clip_NN}_{folder}_{name}_nobg.webm
Resumable: skips clips whose output already exists.
"""

import os
import re
import json
import subprocess
import time
from pathlib import Path
from PIL import Image

# ── GPU setup (DirectML — no CUDA toolkit required) ───────────────────────────
MODEL_DIR = r"D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing\Model"
os.environ["U2NET_HOME"] = MODEL_DIR
os.environ["ORT_DIRECTML"] = "1"

from rembg import remove, new_session
import onnxruntime as ort

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE          = Path(r"D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing")
CLIP_JSON     = BASE / "Output/Onepiece/_analysis/_clips/Audio-1-clip-selection.json"
OUT_ROOT      = BASE / "Output/Onepiece/_nobg"
TEMP_FRAMES_IN  = OUT_ROOT / "_temp/in"
TEMP_FRAMES_OUT = OUT_ROOT / "_temp/out"

# ── Helpers ───────────────────────────────────────────────────────────────────
def name_slug(filename: str) -> str:
    """[animeclipsraw.fr] 191fps (3).mp4 → 191fps-3,  luffy [animeclipsraw.fr]2.mp4 → luffy-2"""
    stem = Path(filename).stem
    stem = re.sub(r'\[.*?\]', '', stem)
    stem = re.sub(r'[().]', '-', stem)
    stem = re.sub(r'[^\w-]', '', stem)
    stem = re.sub(r'-+', '-', stem).strip('-')
    return stem.lower() if stem else "clip"

def label_slug(label: str) -> str:
    return re.sub(r'[^\w]+', '-', label).strip('-')

def folder_slug(folder: str) -> str:
    return re.sub(r'\s+', '-', folder).lower()

def get_fps(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "stream=r_frame_rate",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True
    )
    line = r.stdout.strip().split("\n")[0]
    n, d = map(int, line.split("/"))
    return round(n / d, 3)

def clear_dir(d: Path):
    if d.exists():
        for f in d.glob("*.png"):
            f.unlink()
    d.mkdir(parents=True, exist_ok=True)

# ── Build task list ───────────────────────────────────────────────────────────
data = json.loads(CLIP_JSON.read_text(encoding="utf-8"))
tasks = []

for seg in data["segments"]:
    seg_id    = seg["segment_id"]
    seg_lbl   = seg["label"]
    out_dir   = OUT_ROOT / f"Seg{seg_id}_{label_slug(seg_lbl)}"
    out_dir.mkdir(parents=True, exist_ok=True)

    for clip in seg["selected_clips"]:
        order    = clip["order"]
        folder   = clip["folder"]
        filename = clip["filename"]
        src      = BASE / clip["path"]
        out_name = f"clip_{order:02d}_{folder_slug(folder)}_{name_slug(filename)}_nobg.webm"
        tasks.append({
            "label":    f"Seg{seg_id} clip {order:02d} | {folder} | {filename}",
            "src":      src,
            "out_dir":  out_dir,
            "out_path": out_dir / out_name,
        })

# ── Init session ──────────────────────────────────────────────────────────────
print("=" * 65)
print(f"Batch rembg — isnet-anime via DirectML")
print(f"Providers : {ort.get_available_providers()}")
print(f"Total clips: {len(tasks)}")
print(f"Output root: {OUT_ROOT}")
print("=" * 65)
print("Initializing rembg session...")
session = new_session("isnet-anime", providers=["DmlExecutionProvider", "CPUExecutionProvider"])
print("Session ready.\n")

# ── Main loop ─────────────────────────────────────────────────────────────────
grand_start    = time.time()
total_frames   = 0
clips_done     = 0
clips_skipped  = 0
clips_failed   = 0

for i, task in enumerate(tasks):
    src      = task["src"]
    out_path = task["out_path"]
    label    = task["label"]

    print(f"[{i+1:>2}/{len(tasks)}] {label}")

    if out_path.exists():
        print(f"         SKIP — output already exists\n")
        clips_skipped += 1
        continue

    if not src.exists():
        print(f"         ERROR — source not found: {src}\n")
        clips_failed += 1
        continue

    # Get fps
    fps = get_fps(src)

    # Extract frames
    clear_dir(TEMP_FRAMES_IN)
    clear_dir(TEMP_FRAMES_OUT)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), str(TEMP_FRAMES_IN / "frame_%04d.png")],
        capture_output=True
    )
    frames = sorted(TEMP_FRAMES_IN.glob("frame_*.png"))

    if not frames:
        print(f"         ERROR — no frames extracted\n")
        clips_failed += 1
        continue

    print(f"         {len(frames)} frames @ {fps}fps | removing background...")

    # Remove background
    t0 = time.time()
    for j, fp in enumerate(frames):
        img    = Image.open(fp)
        result = remove(img, session=session)
        result.save(TEMP_FRAMES_OUT / fp.name)
        print(f"         frame {j+1:>4}/{len(frames)}", end="\r")

    elapsed       = time.time() - t0
    ms_per_frame  = elapsed / len(frames) * 1000
    total_frames += len(frames)
    print(f"         {len(frames)} frames done in {elapsed:.1f}s  ({ms_per_frame:.0f}ms/frame)")

    # Rebuild WebM VP9 + alpha
    subprocess.run(
        ["ffmpeg", "-y",
         "-framerate", str(fps),
         "-i", str(TEMP_FRAMES_OUT / "frame_%04d.png"),
         "-c:v", "libvpx-vp9",
         "-pix_fmt", "yuva420p",
         "-b:v", "0", "-crf", "18",
         str(out_path)],
        capture_output=True
    )

    if out_path.exists():
        size_kb = out_path.stat().st_size / 1024
        print(f"         [OK] {out_path.name}  ({size_kb:.0f} KB)\n")
        clips_done += 1
    else:
        print(f"         [FAIL] WebM not created\n")
        clips_failed += 1

# ── Summary ───────────────────────────────────────────────────────────────────
total_elapsed = time.time() - grand_start
print("=" * 65)
print(f"COMPLETE")
print(f"  Processed : {clips_done} clips  ({total_frames} frames)")
print(f"  Skipped   : {clips_skipped} (already existed)")
print(f"  Failed    : {clips_failed}")
print(f"  Total time: {total_elapsed:.0f}s  ({total_elapsed/60:.1f} min)")
print(f"  Output    : {OUT_ROOT}")
print("=" * 65)
