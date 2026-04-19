"""
PILImageResize — 基于 PIL 的图片缩放节点

fit 模式：
  stretch     — 直接拉伸到目标尺寸，不保持比例
  fit         — 等比缩放后居中放入目标尺寸画布，空白区域由 pad_color 决定
  fill        — 等比缩放至覆盖目标区域，中心裁剪多余部分，输出尺寸 == 目标
"""

from PIL import Image


METHOD_MAP = {
    "lanczos":  Image.LANCZOS,
    "bilinear": Image.BILINEAR,
    "bicubic":  Image.BICUBIC,
    "nearest":  Image.NEAREST,
    "box":      Image.BOX,
}

# pad_color 选项 → RGBA 值
PAD_COLOR_MAP = {
    "black":       (0,   0,   0,   255),
    "white":       (255, 255, 255, 255),
    "transparent": (0,   0,   0,   0),
}


def _coerce_int(v, default: int = 0) -> int:
    if v is None or v == "":
        return default
    try:
        return int(float(str(v).strip()))
    except (TypeError, ValueError):
        return default


class PILImageResize:
    NAME = "Image Resize (PIL)"
    CATEGORY = "Image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "measurement": (["pixels", "percentage"], {
                    "tooltip": (
                        "'pixels' — 以像素为单位指定尺寸\n"
                        "'percentage' — 以原图尺寸的百分比指定尺寸"
                    ),
                }),
                "width": ("INT", {
                    "default": 512, "min": 0, "max": 16384, "step": 1,
                    "tooltip": "目标宽度。设为 0 时根据高度等比计算",
                }),
                "height": ("INT", {
                    "default": 512, "min": 0, "max": 16384, "step": 1,
                    "tooltip": "目标高度。设为 0 时根据宽度等比计算",
                }),
                "fit": (["stretch", "fit", "fill"], {
                    "tooltip": (
                        "'stretch' — 直接拉伸到目标尺寸，不保持比例\n"
                        "'fit'     — 等比缩放后居中放入目标尺寸画布，空白由 pad_color 填充\n"
                        "'fill'    — 等比缩放至覆盖目标区域，中心裁剪多余部分"
                    ),
                }),
                "pad_color": (["black", "white", "transparent"], {
                    "tooltip": (
                        "fit 模式下画布空白区域的填充颜色\n"
                        "'transparent' 时输出 RGBA PNG，其余输出 RGB"
                    ),
                }),
                "method": (["lanczos", "bilinear", "bicubic", "nearest", "box"], {
                    "default": "lanczos",
                    "tooltip": (
                        "lanczos  — 质量最高，适合放大\n"
                        "bicubic  — 双三次插值，质量好，速度适中\n"
                        "bilinear — 双线性插值，速度快\n"
                        "box      — 适合缩小\n"
                        "nearest  — 最近邻，速度最快，质量最低"
                    ),
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height")
    FUNCTION = "resize"
    DESCRIPTION = "使用 PIL 对图片进行高质量缩放，支持 stretch / fit / fill 三种模式"

    def resize(self, image, measurement: str, width, height,
               fit: str, pad_color: str, method: str):
        measurement = str(measurement or "pixels").strip()
        fit         = str(fit or "fit").strip()
        pad_color   = str(pad_color or "black").strip()
        method      = str(method or "lanczos").strip()
        width       = _coerce_int(width, 0)
        height      = _coerce_int(height, 0)

        pil_img = self._to_pil(image)
        orig_w, orig_h = pil_img.size

        # ── 解析目标尺寸 ────────────────────────────────────
        if measurement == "percentage":
            target_w = round(width  * orig_w / 100) if width  > 0 else 0
            target_h = round(height * orig_h / 100) if height > 0 else 0
        else:
            target_w, target_h = width, height

        # ── 零值等比计算 ────────────────────────────────────
        if target_w == 0 and target_h == 0:
            return (pil_img, orig_w, orig_h)

        if target_w == 0 or target_h == 0:
            ratio = orig_w / orig_h
            target_w = max(1, round(target_h * ratio)) if target_w == 0 else target_w
            target_h = max(1, round(target_w / ratio)) if target_h == 0 else target_h
            fit = "fit"

        if target_w == orig_w and target_h == orig_h:
            return (pil_img, orig_w, orig_h)

        resample     = METHOD_MAP.get(method, Image.LANCZOS)
        orig_ratio   = orig_w / orig_h
        target_ratio = target_w / target_h

        # ── stretch：直接拉伸 ────────────────────────────────
        if fit == "stretch":
            out = pil_img.resize((target_w, target_h), resample)
            return (out, target_w, target_h)

        # ── fit：等比缩放 + 画布居中 ─────────────────────────
        if fit == "fit":
            # 计算等比缩放后的尺寸（完整容纳在目标框内）
            if orig_ratio > target_ratio:
                new_w = target_w
                new_h = max(1, round(target_w / orig_ratio))
            else:
                new_h = target_h
                new_w = max(1, round(target_h * orig_ratio))

            scaled = pil_img.resize((new_w, new_h), resample)

            # 创建目标尺寸画布
            fill_rgba = PAD_COLOR_MAP.get(pad_color, (0, 0, 0, 255))
            use_alpha = (pad_color == "transparent")

            if use_alpha:
                canvas = Image.new("RGBA", (target_w, target_h), fill_rgba)
                # 确保 scaled 也是 RGBA 以便正确粘贴
                if scaled.mode != "RGBA":
                    scaled = scaled.convert("RGBA")
                paste_x = (target_w - new_w) // 2
                paste_y = (target_h - new_h) // 2
                canvas.paste(scaled, (paste_x, paste_y), mask=scaled)
            else:
                canvas = Image.new("RGB", (target_w, target_h), fill_rgba[:3])
                if scaled.mode != "RGB":
                    scaled = scaled.convert("RGB")
                paste_x = (target_w - new_w) // 2
                paste_y = (target_h - new_h) // 2
                canvas.paste(scaled, (paste_x, paste_y))

            return (canvas, target_w, target_h)

        # ── fill：等比缩放至覆盖，中心裁剪 ──────────────────
        if fit == "fill":
            if orig_ratio > target_ratio:
                new_h = target_h
                new_w = max(1, round(target_h * orig_ratio))
            else:
                new_w = target_w
                new_h = max(1, round(target_w / orig_ratio))

            scaled = pil_img.resize((new_w, new_h), resample)
            left = (new_w - target_w) // 2
            top  = (new_h - target_h) // 2
            out  = scaled.crop((left, top, left + target_w, top + target_h))
            return (out, target_w, target_h)

        # fallback
        out = pil_img.resize((target_w, target_h), resample)
        return (out, target_w, target_h)

    def _to_pil(self, image):
        if isinstance(image, Image.Image):
            return image

        import numpy as np

        if hasattr(image, "numpy"):
            arr = image.numpy()
        else:
            arr = np.asarray(image)

        if arr.ndim == 4:
            arr = arr[0]
        if arr.ndim == 3 and arr.shape[0] in (1, 3, 4):
            arr = np.transpose(arr, (1, 2, 0))
        elif arr.ndim == 2:
            arr = np.stack([arr, arr, arr], axis=-1)

        if arr.dtype != np.uint8:
            arr = (arr * 255).astype(np.uint8) if arr.max() <= 1.0 else arr.astype(np.uint8)

        if arr.shape[-1] == 4:
            return Image.fromarray(arr, mode="RGBA")
        return Image.fromarray(arr, mode="RGB")


NODE_CLASS_MAPPINGS = {"PILImageResize": PILImageResize}
NODE_DISPLAY_NAME_MAPPINGS = {"PILImageResize": "Image Resize (PIL) 图片缩放"}
