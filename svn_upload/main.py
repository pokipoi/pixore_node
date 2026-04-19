"""
SVNUploadNode — SVN 提交节点

接收 PathCollector 输出的路径列表，执行：
  1. 验证每个文件确实存在于磁盘（verify_exists=True 时）
  2. svn add（已在版本控制中的文件自动跳过）
  3. svn commit

依赖：系统已安装 svn 命令行工具（TortoiseSVN 命令行版 / CollabNet SVN）
"""

import os
import subprocess
import shutil


class SVNUploadNode:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "paths": ("FILES",),
            },
            "optional": {
                "repo_url":      ("STRING",  {"default": ""}),
                "commit_msg":    ("STRING",  {"default": "Auto commit by workflow"}),
                "username":      ("STRING",  {"default": ""}),
                "password":      ("STRING",  {"default": ""}),
                "verify_exists": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("status", "committed")
    FUNCTION = "upload"
    CATEGORY = "Output"

    def upload(self, paths=None, repo_url="", commit_msg="Auto commit by workflow",
               username="", password="", verify_exists=True, ctx=None, **kwargs):

        if not paths:
            if ctx:
                ctx.send_log("  ⚠ SVN Upload: 没有收到任何路径，跳过")
            return ("no files", 0)

        if isinstance(paths, str):
            paths = [paths]

        # ── 1. 验证文件存在 ──────────────────────────────────────────────
        if verify_exists:
            missing = [p for p in paths if not os.path.isfile(p)]
            if missing:
                msg = f"以下文件不存在，终止上传:\n" + "\n".join(missing)
                if ctx:
                    ctx.send_log(f"  ✖ SVN Upload: {msg}")
                return (f"error: missing files: {missing}", 0)

        if not shutil.which("svn"):
            if ctx:
                ctx.send_log("  ✖ SVN Upload: 未找到 svn 命令，请安装 SVN 命令行工具")
            return ("error: svn not found", 0)

        # ── 2. svn add（忽略已跟踪的文件）──────────────────────────────
        add_ok = []
        for p in paths:
            try:
                result = subprocess.run(
                    self._build_cmd(["svn", "add", "--force", p], username, password),
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    add_ok.append(p)
                    if ctx:
                        ctx.send_log(f"  ✔ svn add: {os.path.basename(p)}")
                else:
                    # 已在版本控制中也算正常
                    stderr = result.stderr.strip()
                    if "is already under version control" in stderr or \
                       "already versioned" in stderr.lower():
                        add_ok.append(p)
                    else:
                        if ctx:
                            ctx.send_log(f"  ⚠ svn add 警告 {os.path.basename(p)}: {stderr}")
                        add_ok.append(p)  # 仍尝试 commit
            except subprocess.TimeoutExpired:
                if ctx:
                    ctx.send_log(f"  ✖ svn add 超时: {p}")
            except Exception as e:
                if ctx:
                    ctx.send_log(f"  ✖ svn add 失败 {p}: {e}")

        if not add_ok:
            return ("error: all svn add failed", 0)

        # ── 3. svn commit ────────────────────────────────────────────────
        cmd = self._build_cmd(
            ["svn", "commit"] + add_ok + ["-m", commit_msg or "workflow commit"],
            username, password
        )
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                if ctx:
                    ctx.send_log(f"  ✔ SVN commit 成功: {len(add_ok)} 个文件")
                    ctx.send_log(f"    {result.stdout.strip()}")
                return (f"committed {len(add_ok)} files", len(add_ok))
            else:
                err = result.stderr.strip()
                if ctx:
                    ctx.send_log(f"  ✖ SVN commit 失败: {err}")
                return (f"error: {err}", 0)
        except subprocess.TimeoutExpired:
            if ctx:
                ctx.send_log("  ✖ SVN commit 超时（120s）")
            return ("error: commit timeout", 0)
        except Exception as e:
            if ctx:
                ctx.send_log(f"  ✖ SVN commit 异常: {e}")
            return (f"error: {e}", 0)

    @staticmethod
    def _build_cmd(base_cmd: list, username: str, password: str) -> list:
        cmd = list(base_cmd)
        if username:
            cmd += ["--username", username]
        if password:
            cmd += ["--password", password, "--no-auth-cache"]
        return cmd


NODE_CLASS_MAPPINGS = {"svn-upload": SVNUploadNode}
NODE_DISPLAY_NAME_MAPPINGS = {"svn-upload": "SVN Upload"}
