"""
FileInputNode — 通用文件输入节点
统一处理各种文件输入方式：
    - 单个或多个文件
    - 单个或多个文件夹
    - 文件和文件夹混合
    - 本地路径或网络路径 (UNC)

支持:
    - 按扩展名过滤
    - 递归扫描子文件夹
    - 文件数量限制
    - 多种排序方式
    - 去重处理
"""

import os
import glob
from typing import List, Optional
from PIL import Image
import random


class FileInputNode:
    """
    文件输入节点 - 工作流的入口节点。

    主要功能:
        1. 展开文件夹为文件列表
        2. 按扩展名过滤
        3. 排序和限制数量
        4. 去重处理
    """

    # 支持的图片扩展名
    IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    VIDEO_EXTS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
    AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a'}
    PDF_EXTS = {'.pdf'}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                # 注意：不要定义任何类型化的输入参数（如 IMAGE, FILES 等）
                # 因为引擎会将 current_data 传递过来，但这不是我们需要的
                # 我们只使用 payload.filepath
                "extensions":  ("STRING", {"default": ""}),
                "recursive":   ("BOOLEAN", {"default": True}),
                "max_files":   ("INT", {"default": 0, "min": 0, "max": 99999}),
                "sort_by":     ("STRING", {"default": "name"}),
                "dedup":       ("BOOLEAN", {"default": True}),
                # 截流参数（由引擎从 workflow 配置中读取）
                "mode":        ("STRING", {"default": "pipeline"}),      # pipeline | throttle
                "throttle_count": ("INT", {"default": 0, "min": 0, "max": 9999}),   # 截流数量阈值
                "throttle_timeout": ("FLOAT", {"default": 5.0, "min": 0, "max": 300}),  # 截流超时（秒）
            }
        }

    RETURN_TYPES = ("FILES", "INT", "STRING")
    RETURN_NAMES = ("files", "count", "summary")
    FUNCTION = "process"
    CATEGORY = "Input"
    OUTPUT_NODE = True

    def process(self, extensions: str = "",
                recursive: bool = True, max_files: int = 0,
                sort_by: str = "name", dedup: bool = True,
                mode: str = "pipeline",
                throttle_count: int = 0,
                throttle_timeout: float = 5.0,
                ctx=None, payload=None):
        """
        处理文件输入。

        架构说明:
            - 优先使用 ctx.batch_files（截流模式传入的批次文件列表）
            - 否则使用 payload.filepath（管线模式）
        """
        # 解析扩展名过滤
        ext_filter = None
        if extensions and extensions.strip():
            ext_filter = {f".{ext.strip().lower().lstrip('.')}" for ext in extensions.split(',')}
            ext_filter = {e if e.startswith('.') else f'.{e}' for e in ext_filter}

        # 1. 优先使用 ctx.batch_files（截流模式）
        batch_files = ctx.get_output("batch_files") if ctx else None

        if batch_files and isinstance(batch_files, list) and len(batch_files) > 0:
            # 截流模式：使用批次文件列表
            files = batch_files.copy()
            if ctx:
                ctx.send_log(f"  📥 截流模式: 使用批次 {len(files)} 个文件")
        else:
            # 管线模式：使用 payload.filepath
            source_path = None
            if payload and hasattr(payload, 'filepath') and payload.filepath:
                source_path = str(payload.filepath)

            if not source_path:
                if ctx:
                    ctx.send_log(f"  ⚠ 无法获取文件路径")
                return ("", 0, "无文件路径")

            files = self._collect_files(source_path, extensions, recursive)

        # 5. 去重
        if dedup:
            seen = set()
            unique_files = []
            for f in files:
                normalized = os.path.normpath(os.path.abspath(f))
                if normalized not in seen:
                    seen.add(normalized)
                    unique_files.append(f)
            files = unique_files

        # 6. 排序
        files = self._sort_files(files, sort_by)

        # 7. 限制数量
        original_count = len(files)
        if max_files > 0 and len(files) > max_files:
            files = files[:max_files]

        # 8. 将文件列表存储到 ctx 中
        if ctx:
            ctx.set_output("file_list", files)
            ctx.set_output("all_files", files)
            ctx.send_log(f"  📁 文件输入: 找到 {len(files)} 个文件")
            if original_count != len(files):
                ctx.send_log(f"  📁 (共扫描 {original_count} 个文件)")

        # 9. 生成摘要
        summary = self._generate_summary(original_count, len(files), max_files, ext_filter)

        # 10. 返回第一个文件的图像对象（引擎需要 PIL Image）
        if files:
            try:
                first_image = Image.open(files[0])
                if ctx:
                    ctx.send_log(f"  📁 文件输入: 找到 {len(files)} 个文件，加载 {files[0]}")
                return (first_image, len(files), summary)
            except Exception as e:
                if ctx:
                    ctx.send_log(f"  ⚠ 无法加载图片 {files[0]}: {e}")
                return ("", 0, f"加载失败: {e}")
        else:
            return ("", 0, "未找到文件")

        return (files, len(files), summary)

    def _collect_files(self, source_path: str, extensions: str,
                       recursive: bool) -> List[str]:
        """
        收集文件（管线模式专用）。
        将路径展开为文件列表。
        """
        ext_filter = None
        if extensions and extensions.strip():
            ext_filter = {f".{ext.strip().lower().lstrip('.')}" for ext in extensions.split(',')}
            ext_filter = {e if e.startswith('.') else f'.{e}' for e in ext_filter}

        files = []

        if self._is_network_path(source_path):
            files.extend(self._scan_network_path(source_path, ext_filter, recursive))
        elif os.path.isdir(source_path):
            files.extend(self._scan_directory(source_path, ext_filter, recursive))
        elif os.path.isfile(source_path):
            ext = os.path.splitext(source_path)[1].lower()
            if ext_filter is None or ext in ext_filter:
                files.append(source_path)
        else:
            import glob as glob_module
            matched = glob_module.glob(source_path)
            for f in matched:
                if os.path.isfile(f):
                    ext = os.path.splitext(f)[1].lower()
                    if ext_filter is None or ext in ext_filter:
                        files.append(f)

        return files

    def _is_network_path(self, path: str) -> bool:
        """判断是否为网络路径 (UNC)"""
        return path.startswith('\\\\') or path.startswith('//')

    def _scan_directory(self, directory: str, ext_filter: Optional[set],
                        recursive: bool) -> List[str]:
        """扫描本地目录"""
        results = []

        try:
            if recursive:
                # 递归扫描
                for root, dirs, filenames in os.walk(directory):
                    for filename in filenames:
                        filepath = os.path.join(root, filename)
                        if ext_filter is None or os.path.splitext(filename)[1].lower() in ext_filter:
                            results.append(filepath)
            else:
                # 只扫描当前目录
                for entry in os.scandir(directory):
                    if entry.is_file():
                        if ext_filter is None or os.path.splitext(entry.name)[1].lower() in ext_filter:
                            results.append(entry.path)
        except PermissionError:
            pass
        except Exception as e:
            pass

        return results

    def _scan_network_path(self, unc_path: str, ext_filter: Optional[set],
                           recursive: bool) -> List[str]:
        """扫描网络路径 (UNC)"""
        # 使用 glob 处理网络路径
        results = []

        try:
            if recursive:
                pattern = os.path.join(unc_path, '**', '*')
            else:
                pattern = os.path.join(unc_path, '*')

            for filepath in glob.glob(pattern, recursive=recursive):
                if os.path.isfile(filepath):
                    if ext_filter is None or os.path.splitext(filepath)[1].lower() in ext_filter:
                        results.append(filepath)
        except Exception:
            pass

        return results

    def _sort_files(self, files: List[str], sort_by: str) -> List[str]:
        """对文件列表排序"""
        if not files:
            return files

        sort_by = sort_by.lower().strip()

        try:
            if sort_by == 'name':
                return sorted(files, key=lambda x: os.path.basename(x).lower())
            elif sort_by == 'date':
                return sorted(files, key=lambda x: os.path.getmtime(x), reverse=True)
            elif sort_by == 'size':
                return sorted(files, key=lambda x: os.path.getsize(x), reverse=True)
            elif sort_by == 'random':
                random.shuffle(files)
                return files
            else:
                return sorted(files, key=lambda x: os.path.basename(x).lower())
        except Exception:
            return files

    def _generate_summary(self, total: int, after: int, max_files: int,
                         ext_filter: Optional[set]) -> str:
        """生成处理摘要"""
        parts = []

        if max_files > 0 and total > max_files:
            parts.append(f"限制 {max_files} 个文件")
            parts.append(f"扫描 {total} 个")
        else:
            parts.append(f"共 {total} 个文件")

        if ext_filter:
            exts = ', '.join(sorted(ext_filter))
            parts.append(f"扩展名: {exts}")

        parts.append(f"处理 {after} 个")

        return ' | '.join(parts)


NODE_CLASS_MAPPINGS = {
    "FileInputNode": FileInputNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FileInputNode": "File Input (文件输入)"
}
