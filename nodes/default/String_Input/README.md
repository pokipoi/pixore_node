# String Input Node

字符串输入节点 - 提供一个文本输入框并输出字符串值。

## 功能

提供一个文本输入界面，允许用户手动输入文本数据，用于工作流中的初始数据输入。

## 输入

| 端口 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| text | STRING | "" | 在此输入文本 |

## 输出

| 端口 | 类型 | 说明 |
|------|------|------|
| text | STRING | 输出文本 |

## 使用示例

### 基础用法

1. 添加 String Input 节点到工作流
2. 在节点界面输入任意文本
3. 连接到其他节点处理文本

### 典型工作流

```
String Input → Text Processing → Output
```

## 工作原理

- 节点提供文本输入框用于用户手动输入
- 输入的文本直接通过 `text` 输出端口传递
- 支持多行文本输入（可配置）

## 配置

可在 manifest.json 中调整：

```json
{
  "inputs": [
    {
      "name": "text",
      "type": "STRING",
      "default": "",
      "multiline": false
    }
  ]
}
```

- `multiline`: 是否允许多行输入（true/false）

## 版本信息

- **版本**: 1.0.0
- **作者**: user
- **分类**: Inputs

## 相关节点

- [Path Collector](../path_collector) - 收集多个路径
- [File Input](../file_input) - 文件输入节点

## 常见问题

**Q: 如何输入长文本？**
A: 修改 manifest.json 中的 `multiline` 属性为 `true`

**Q: 输入的文本能否作为文件路径使用？**
A: 可以，配合 File Input 或其他文件处理节点使用

## 许可证

MIT