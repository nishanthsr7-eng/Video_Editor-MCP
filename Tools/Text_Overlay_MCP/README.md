# Text Overlay MCP

Adds "edit"-style bold text overlays (e.g. "IT WAS YOU") to videos using PIL-rendered
fonts with gradients, outlines, shadows and word-by-word reveal animations.

## Setup

```
uv sync
```

Bundled fonts live in `fonts/` - 24 free/OFL-licensed fonts from Google Fonts,
covering bold display ("edit" titles: Anton, Bebas Neue, Montserrat ExtraBold,
Poppins ExtraBold, Oswald Bold, Archivo Black, Russo One, Black Ops One,
Bungee, Teko, Roboto Condensed, Inter Black, Fredoka, Open Sans Bold),
playful/comic (Bangers, Lobster), script/handwritten (Pacifico, Permanent
Marker, Dancing Script, Caveat), and serif/narration captions (Playfair
Display, Lora, Merriweather, PT Serif). Use `list_fonts` for the exact names.

## Tools

- `list_fonts` - list available bundled fonts.
- `add_text_overlay` - render a text animation over a video, producing both a
  transparent overlay video (`overlay.webm`) and a fully composited output
  video (`output_burned.<ext>`).
