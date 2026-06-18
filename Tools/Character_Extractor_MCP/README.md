# Character Extractor MCP

Splits anime characters from their backgrounds using the [anime-segmentation](https://github.com/SkyTNT/anime-segmentation)
ISNet model (ONNX), exposed as an MCP tool for use with Claude Code.

## Setup

```
uv sync
```

The ONNX model (`models/isnetis.onnx`) is downloaded from
https://huggingface.co/skytnt/anime-seg.

## Tool: extract_character

Takes a folder of frames (e.g. output of the Frame Extractor MCP) and produces
a folder of transparent-background PNG cutouts of the character(s).
