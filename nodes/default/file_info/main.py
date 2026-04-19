"""
FileInfoNode — 读取文件的结构化信息，输出为独立字段。

支持：
    - 接收上游 FILE 类型端口输入（file_input / 其他节点输出的路径）
    - 独立输出：文件名、扩展名、大小、尺寸、页数、字数、MIME 类型、是否存在

依赖（可选，未安装时相关字段返回 0 / 空字符串）：
    - PyMuPDF (fitz)  → PDF 页数
    - chardet        → 文本编码检测（用于字数统计）
"""

import os
import mimetypes

from PIL import Image


class FileInfoNode:
    """文件信息节点 — 读取文件结构化信息，输出为独立字段。"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "file": ("FILE", {
                    "default": "",
                    "placeholder": "输入文件路径（可由上游连线提供）...",
                    "tooltip": "接收上游 FILE 类型端口的文件路径",
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT",
                    "INT", "INT", "INT", "INT", "STRING", "BOOLEAN")
    RETURN_NAMES = ("basename", "extension", "size", "size_bytes",
                    "width", "height", "pages", "word_count",
                    "mime_type", "exists")
    FUNCTION = "process"
    CATEGORY = "Utils"
    OUTPUT_NODE = False

    def process(self, file: str = "", ctx=None, payload=None, **legacy):
        """
        读取文件结构化信息。

        支持三种来源优先级：
          1. ctx.batch_files（截流模式文件列表，取首文件）
          2. 连线注入的 file 参数
          3. payload.filepath（管线模式当前文件）

        Returns:
            (basename, extension, size, size_bytes,
             width, height, pages, word_count, mime_type, exists)
        """
        # ── 路径解析优先级 ──────────────────────────────────────
        path = self._resolve_path(file, ctx, payload)

        # 基础信息（必然返回）
        exists = os.path.isfile(path)
        basename = os.path.basename(path) if path else ""
        name_only = os.path.splitext(basename)[0]
        ext = os.path.splitext(basename)[1].lstrip(".").upper()

        mime_type = ""
        size_bytes = 0
        size_str = ""
        width = 0
        height = 0
        pages = 0
        word_count = 0

        if not exists:
            return (basename, ext, size_str, size_bytes,
                    width, height, pages, word_count, mime_type, False)

        mime_type = self._guess_mime(path) or ""

        try:
            size_bytes = os.path.getsize(path)
            size_str = self._format_size(size_bytes)
        except Exception:
            size_bytes = 0
            size_str = ""

        # ── 图片尺寸 ────────────────────────────────────────────
        dims = self._get_image_dimensions(path)
        if dims:
            width, height = dims

        # ── PDF 页数 ─────────────────────────────────────────────
        if ext == "PDF":
            pages = self._get_pdf_pages(path)

        # ── 文本字数 ─────────────────────────────────────────────
        if ext in ("TXT", "MD", "CSV", "JSON", "XML", "PY", "JS", "TS",
                   "HTML", "CSS", "C", "CPP", "H", "JAVA", "KT", "RS",
                   "GO", "CSHARP", "LOG"):
            word_count = self._get_text_word_count(path)

        return (name_only, ext, size_str, size_bytes,
                width, height, pages, word_count, mime_type, True)

    # ── 路径解析 ───────────────────────────────────────────────────────────

    def _resolve_path(self, file_arg, ctx, payload) -> str:
        """按优先级解析文件路径。"""
        # 1. 连线注入：可能是 str / list[str] / PIL.Image（入口节点 files 端口常为 Image）
        coerced = self._coerce_file_arg_to_path(file_arg)
        if coerced:
            return coerced

        # 2. 截流模式文件列表
        if ctx:
            batch = ctx.get_output("batch_files")
            if batch and isinstance(batch, list) and len(batch) > 0:
                return str(batch[0])
            all_files = ctx.get_output("all_files")
            if all_files and isinstance(all_files, list) and len(all_files) > 0:
                return str(all_files[0])

        # 3. payload（管线模式）
        if payload and hasattr(payload, "filepath") and payload.filepath:
            return str(payload.filepath)

        return ""

    @staticmethod
    def _coerce_file_arg_to_path(file_arg) -> str:
        """将连线数据规范为磁盘路径字符串。"""
        if file_arg is None:
            return ""

        # PIL Image（file_input 的 files 端口实际输出）
        if isinstance(file_arg, Image.Image):
            fn = getattr(file_arg, "filename", None)
            if fn and str(fn).strip() and os.path.isfile(str(fn)):
                return os.path.normpath(str(fn))
            return ""

        # 路径列表（FILES 语义）
        if isinstance(file_arg, (list, tuple)):
            for item in file_arg:
                s = str(item).strip() if item is not None else ""
                if s and os.path.isfile(s):
                    return os.path.normpath(s)
            return ""

        s = str(file_arg).strip()
        if s and os.path.isfile(s):
            return os.path.normpath(s)
        return ""

    # ── 辅助方法 ─────────────────────────────────────────────────────────

    @staticmethod
    def _guess_mime(path: str) -> str:
        mime, _ = mimetypes.guess_type(path)
        return mime or ""

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        if size_bytes < 0:
            return "0 B"
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    @staticmethod
    def _get_image_dimensions(path: str):
        """读取图片 (width, height)。返回 None 表示非图片。"""
        try:
            with Image.open(path) as img:
                return img.size  # (w, h)
        except Exception:
            return None

    @staticmethod
    def _get_pdf_pages(path: str) -> int:
        """使用 PyMuPDF 读取 PDF 页数。"""
        try:
            import fitz
            with fitz.open(path) as doc:
                return len(doc)
        except Exception:
            return 0

    @staticmethod
    def _get_text_word_count(path: str) -> int:
        """统计文本文件字数（以空格 / 换行分词）。"""
        try:
            with open(path, "rb") as f:
                raw = f.read()

            # 尝试用 chardet 检测编码
            encoding = "utf-8"
            try:
                import chardet
                detected = chardet.detect(raw)
                if detected and detected.get("encoding"):
                    encoding = detected["encoding"]
            except Exception:
                pass

            text = raw.decode(encoding, errors="replace")
            # 中文字符 + 英文单词
            import re
            words = re.findall(r"[\u4e00-\u9fff]+|[a-zA-Z0-9_]+", text)
            return len(words)
        except Exception:
            return 0


NODE_CLASS_MAPPINGS = {
    "FileInfoNode": FileInfoNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FileInfoNode": "File Info (文件信息)"
}