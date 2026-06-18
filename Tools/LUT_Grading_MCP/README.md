# LUT Grading MCP

Applies cinematic 3D LUT color-grading presets (or any custom `.cube` file)
to a video via ffmpeg's `lut3d` filter, with adjustable intensity blending.

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH. Bundled `.cube` LUTs live in
`src/lut_grading_mcp/luts/` (regenerate via `python generate_luts.py`).

## Tools

- `list_luts` - list built-in LUT presets and descriptions.
- `apply_lut` - apply a built-in or custom `.cube` LUT to a video, with
  optional intensity blending against the original.

## Built-in presets

- `cinematic_teal_orange`
- `warm_vintage`
- `cool_blue`
- `high_contrast_bw`
- `faded_film`
- `moody_green`
- `bleach_bypass`
