"""
PathCollectorNode — 多路径汇聚节点

将多条上游 saved_path 连线收集为一个列表，
确保所有上游 Save File 节点执行完毕后再传给下游（如 SVN Upload）。

由于引擎是单线程拓扑顺序执行，本节点排在所有 Save File 之后，
因此收到的路径一定已写入磁盘。
"""

import os


class PathCollectorNode:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "path_0": ("STRING", {"default": ""}),
                "path_1": ("STRING", {"default": ""}),
                "path_2": ("STRING", {"default": ""}),
                "path_3": ("STRING", {"default": ""}),
                "path_4": ("STRING", {"default": ""}),
                "path_5": ("STRING", {"default": ""}),
                "path_6": ("STRING", {"default": ""}),
                "path_7": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("FILES", "INT")
    RETURN_NAMES = ("paths", "count")
    FUNCTION = "collect"
    CATEGORY = "Utils"

    def collect(self, path_0="", path_1="", path_2="", path_3="",
                path_4="", path_5="", path_6="", path_7="",
                ctx=None, **kwargs):
        candidates = [path_0, path_1, path_2, path_3,
                      path_4, path_5, path_6, path_7]
        # 过滤空值和不存在的路径，并去重保序
        seen = set()
        valid = []
        for p in candidates:
            if not p or not isinstance(p, str):
                continue
            p = p.strip()
            if not p or p in seen:
                continue
            if not os.path.exists(p):
                if ctx:
                    ctx.send_log(f"  ⚠ PathCollector: 路径不存在，跳过: {p}")
                continue
            seen.add(p)
            valid.append(p)

        if ctx:
            ctx.send_log(f"  📦 PathCollector: 收集到 {len(valid)} 个有效路径")
            for p in valid:
                ctx.send_log(f"    • {os.path.basename(p)}")

        return (valid, len(valid))


NODE_CLASS_MAPPINGS = {"path-collector": PathCollectorNode}
NODE_DISPLAY_NAME_MAPPINGS = {"path-collector": "Path Collector"}
