import os
import numpy as np
from PIL import Image
import onnxruntime as ort

_session = None
_input_name = None
_output_name = None


def _model_path():
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    # src/character_extractor_mcp -> src -> Character_Extractor_MCP -> models
    return os.path.abspath(os.path.join(cur_dir, "..", "..", "models", "isnetis.onnx"))


def _get_session():
    global _session, _input_name, _output_name
    if _session is None:
        model_path = _model_path()
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"未找到分割模型: {model_path}")
        _session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        _input_name = _session.get_inputs()[0].name
        _output_name = _session.get_outputs()[0].name
    return _session


def _get_mask(img: np.ndarray, size: int = 1024) -> np.ndarray:
    """
    img: HxWx3 uint8 RGB
    返回: HxW float32 [0,1] 的 mask（人物前景概率）
    """
    session = _get_session()
    h0, w0 = img.shape[:2]

    if h0 > w0:
        h, w = size, int(size * w0 / h0)
    else:
        h, w = int(size * h0 / w0), size
    h, w = max(h, 1), max(w, 1)

    # 模型输入为 0-255 范围的 float32（不做 /255 归一化）
    resized = np.array(Image.fromarray(img).resize((w, h), Image.BILINEAR)).astype(np.float32)

    ph, pw = size - h, size - w
    padded = np.zeros((size, size, 3), dtype=np.float32)
    padded[ph // 2: ph // 2 + h, pw // 2: pw // 2 + w] = resized

    blob = padded.transpose(2, 0, 1)[np.newaxis, :, :, :]
    pred = session.run([_output_name], {_input_name: blob})[0]
    pred = pred[0, 0]

    pred = pred[ph // 2: ph // 2 + h, pw // 2: pw // 2 + w]
    pred = np.array(Image.fromarray((pred * 255).astype(np.uint8)).resize((w0, h0), Image.BILINEAR)).astype(np.float32) / 255.0
    return np.clip(pred, 0.0, 1.0)


def split_character_and_background(image_path, character_path, background_path=None, size=1024, threshold=0.0):
    """
    将单张图片中的人物和背景分离。

    image_path: 输入图片路径
    character_path: 输出人物图片路径（RGBA，背景透明）
    background_path: 输出背景图片路径（RGBA，人物区域透明），不传则不生成
    size: 模型推理分辨率，默认1024
    threshold: mask二值化阈值，0表示使用原始alpha（软边缘），>0则二值化
    """
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    mask = _get_mask(arr, size=size)

    if threshold > 0:
        mask = (mask > threshold).astype(np.float32)

    alpha = (mask * 255).astype(np.uint8)

    character = np.dstack([arr, alpha])
    Image.fromarray(character, "RGBA").save(character_path)

    if background_path:
        bg_alpha = (255 - alpha)
        background = np.dstack([arr, bg_alpha])
        Image.fromarray(background, "RGBA").save(background_path)
