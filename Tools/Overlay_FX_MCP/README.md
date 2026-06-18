# Overlay FX MCP

Cinematic look effects: film grain, vignette, chromatic aberration, and
animated light-leak/lens-flare overlays (procedurally generated, blended
with `screen` mode).

## Setup

```
uv sync
```

Requires `ffmpeg`/`ffprobe` on PATH. Bundled light-leak PNGs live in
`src/overlay_fx_mcp/assets/` (regenerate via `python generate_overlays.py`).

## Tools

- `add_film_grain` - overlay film-grain noise.
- `add_vignette` - darken frame edges.
- `add_chromatic_aberration` - offset red/blue channels for a glitch/CRT look.
- `add_light_leak` - animated colored light-leak/lens-flare panning across
  the frame (`warm`, `golden`, `cool`, `white` styles).
