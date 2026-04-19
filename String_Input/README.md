# String Input 节点

本节点用于在工作流中手动输入字符串值并将其输出给下游节点。

**文件**
- `main.py`：节点实现，类名 `StringInputNode`。
- `manifest.json`：节点元数据及端口定义。

**功能**
- 一个必需输入：`text`（`STRING`），用于输入文本。
- 一个输出：`text`（`STRING`），直接返回输入的字符串。

示例 `manifest.json`（节点当前使用版本）：

```json
{
  "id": "string-input",
  "name": "String Input",
  "author": "user",
  "version": "1.0.0",
  "description": "字符串输入节点：提供一个文本输入框并输出字符串值。",
  "category": "Inputs",
  "entry_point": "main.py",
  "node_class": "StringInputNode",
  "inputs": [
    {"name": "text", "type": "STRING", "default": "", "multiline": false, "description": "在此输入文本"}
  ],
  "outputs": [
    {"name": "text", "type": "STRING", "description": "输出文本"}
  ]
}
```

使用说明：把节点拖入画布，在 `text` 框中输入要传递的字符串，连接到下游节点的字符串输入端口即可。

可定制项（如需我修改，请告知）
- 开启多行输入：把 `manifest.json` 中 `multiline` 改为 `true`，并将 `main.py` 中 `multiline` 设置为 `True`。
- 更改分类：调整 `category` 字段。

文件位置： [nodes_library/String_Input/main.py](nodes_library/String_Input/main.py#L1) 及 [nodes_library/String_Input/manifest.json](nodes_library/String_Input/manifest.json#L1)