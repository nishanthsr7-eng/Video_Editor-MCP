# server.py
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path + "/..")

from mcp.server.fastmcp import FastMCP
import character_extractor_mcp.segmenter as segmenter

mcp = FastMCP("character-extractor-mcp")

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


@mcp.tool()
def extract_character(input_folder, output_folder=None, with_background=False, size=1024, threshold=0.0):
    """
    使用 anime-segmentation (ISNet) 模型将文件夹中每一帧图片的人物从背景中分离，
    输出带透明通道的人物抠图（PNG）。

    参数：
    input_folder(str) - 输入图像文件夹路径（通常是 extract_frames_from_video 的输出目录）
    output_folder(str) - 输出文件夹路径，不传则默认为 "<input_folder>_character"
    with_background(bool) - 是否同时输出去除人物后的背景图（人物区域透明）
    size(int) - 模型推理分辨率，默认1024，越大越精细但越慢
    threshold(float) - mask二值化阈值(0-1)，0表示保留原始软边缘（推荐，边缘更自然），>0则二值化为硬边缘
    返回：
    (status_code, message, output_folder)
    """
    if not os.path.isdir(input_folder):
        return -1, f"输入文件夹不存在: {input_folder}", ""

    if output_folder is None:
        output_folder = f"{input_folder.rstrip(os.sep).rstrip('/')}_character"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    background_folder = None
    if with_background:
        background_folder = f"{output_folder}_background"
        if not os.path.exists(background_folder):
            os.makedirs(background_folder)

    files = sorted(f for f in os.listdir(input_folder) if os.path.splitext(f)[1].lower() in IMG_EXTS)
    if not files:
        return -1, f"输入文件夹中没有图片: {input_folder}", ""

    processed = 0
    for name in files:
        stem = os.path.splitext(name)[0]
        in_path = os.path.join(input_folder, name)
        char_path = os.path.join(output_folder, f"{stem}.png")
        bg_path = os.path.join(background_folder, f"{stem}.png") if background_folder else None
        try:
            segmenter.split_character_and_background(in_path, char_path, bg_path, size=size, threshold=threshold)
            processed += 1
        except Exception as e:
            return -1, f"处理失败 {name}: {e}", output_folder

    msg = f"已处理 {processed}/{len(files)} 帧"
    if background_folder:
        msg += f"，背景输出目录: {background_folder}"
    return 0, msg, output_folder


def main():
    print("Character Extractor MCP server running")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
