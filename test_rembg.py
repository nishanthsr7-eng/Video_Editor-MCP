"""
rembg background removal test — isnet-anime model
Processes a single clip: extracts frames → removes background → rebuilds video with alpha
Models loaded from: D:\...\Model  (u2net.onnx + isnet-anime.onnx)
GPU: onnxruntime-directml (DirectX 12, no CUDA toolkit required)
"""

import os
import subprocess
import shutil
from pathlib import Path
from PIL import Image
import time

# Point rembg to project Model folder before importing
MODEL_DIR = r"D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing\Model"
os.environ["U2NET_HOME"] = MODEL_DIR
# Force DirectML (DirectX 12) GPU provider — works without CUDA toolkit
os.environ["ORT_DIRECTML"] = "1"

from rembg import remove, new_session
import onnxruntime as ort

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE       = Path(r"D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing")
SAMPLE     = BASE / "Sources" / "Onepiece" / "Sad" / "[animeclipsraw.fr] 191fps (1).mp4"
OUT_DIR    = BASE / "Output" / "Onepiece" / "_test_rembg"
FRAMES_IN  = OUT_DIR / "frames_original"
FRAMES_OUT = OUT_DIR / "frames_nobg"
RESULT_VID = OUT_DIR / "sad_clip1_nobg.webm"

# ── Setup ──────────────────────────────────────────────────────────────────────
for d in [FRAMES_IN, FRAMES_OUT]:
    d.mkdir(parents=True, exist_ok=True)

# ── Step 1: Get clip info ──────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Reading clip info")
result = subprocess.run(
    ["ffprobe", "-v", "quiet", "-show_entries",
     "stream=width,height,r_frame_rate", "-of", "csv=p=0", str(SAMPLE)],
    capture_output=True, text=True
)
lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
width, height, fps_raw = lines[0].split(",")
width, height = int(width), int(height)
fps_num, fps_den = map(int, fps_raw.split("/"))
fps = round(fps_num / fps_den, 3)
print(f"  Resolution : {width}x{height}")
print(f"  FPS        : {fps}")

# ── Step 2: Extract frames ─────────────────────────────────────────────────────
print("\nSTEP 2: Extracting frames from clip")
subprocess.run([
    "ffmpeg", "-y", "-i", str(SAMPLE),
    str(FRAMES_IN / "frame_%04d.png")
], capture_output=True)
frames = sorted(FRAMES_IN.glob("frame_*.png"))
print(f"  Extracted  : {len(frames)} frames")

# ── Step 3: Run rembg with isnet-anime ────────────────────────────────────────
print("\nSTEP 3: Running rembg (isnet-anime model) — GPU via DirectML")
print(f"  ORT providers : {ort.get_available_providers()}")
providers = ["DmlExecutionProvider", "CPUExecutionProvider"]
session = new_session("isnet-anime", providers=providers)

t_start = time.time()
for i, frame_path in enumerate(frames):
    img = Image.open(frame_path)
    out = remove(img, session=session)
    out.save(FRAMES_OUT / frame_path.name)
    print(f"  Frame {i+1:>3}/{len(frames)} processed", end="\r")

elapsed = time.time() - t_start
print(f"\n  Done in    : {elapsed:.1f}s  ({elapsed/len(frames)*1000:.0f}ms/frame)")

# ── Step 4: Rebuild video with transparency (WebM VP9 + alpha) ────────────────
print("\nSTEP 4: Rebuilding video with transparent background (.webm)")
subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(fps),
    "-i", str(FRAMES_OUT / "frame_%04d.png"),
    "-c:v", "libvpx-vp9",
    "-pix_fmt", "yuva420p",
    "-b:v", "0", "-crf", "18",
    str(RESULT_VID)
], capture_output=True)

# ── Step 5: Report ─────────────────────────────────────────────────────────────
print("\nSTEP 5: Results")
if RESULT_VID.exists():
    size_kb = RESULT_VID.stat().st_size / 1024
    print(f"  Output     : {RESULT_VID}")
    print(f"  File size  : {size_kb:.1f} KB")
    print(f"  Frames     : {len(frames)}")
    print(f"  Format     : WebM VP9 with alpha (transparent background)")
    print("\n  SUCCESS — background removed!")
else:
    print("  ERROR: Output video not created. Check ffmpeg logs.")

print("=" * 60)
