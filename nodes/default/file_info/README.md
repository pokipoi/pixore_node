# File Info Node

文件信息读取节点 - 读取文件基本信息（名称、路径、大小、尺寸、页数、字数等）。

## 功能

读取文件的各种元数据信息，支持图片、PDF、文档等多种文件类型。支持接收上游文件路径并输出为独立字段。

## 输入

| 端口 | 类型 | 说明 |
|------|------|------|
| file | FILE | 输入文件路径（可由上游连线提供） |

## 输出

| 端口 | 类型 | 说明 |
|------|------|------|
| basename | STRING | 文件名（不含路径） |
| extension | STRING | 文件扩展名（不含点） |
| size | STRING | 人类可读文件大小（如 1.23 MB） |
| size_bytes | INT | 文件大小（字节） |
| width | INT | 图片宽度（像素，非图片为 0） |
| height | INT | 图片高度（像素，非图片为 0） |
| pages | INT | 页数（图片/PDF，多页 GIF 为帧数） |

## 使用示例

### 获取图片信息

```
File Input → File Info → (Output)
                ↓ width
                ↓ height
```

### 按文件大小过滤

```
File Input → File Info → (size_bytes) → Filter → Output
```

### 提取文件名

```
File Input → File Info → (basename) → Display
```

## 支持的文件类型

### 图片
- JPEG, PNG, GIF, BMP, WebP, TIFF
- 输出: width, height, pages（GIF 为帧数）

### 文档
- PDF, DOCX, XLSX, TXT 等
- 输出: pages（页数）

### 其他
- 所有文件: basename, extension, size, size_bytes

## 工作原理

1. 接收文件路径
2. 读取文件元数据
3. 根据文件类型提取相应信息
4. 通过独立端口输出各项信息

## 性能考虑

- 对大文件首先检查大小，避免完全读取
- 图片尺寸通过文件头快速读取，无需加载整个文件

## 版本信息

- **版本**: 1.1.0
- **作者**: system
- **分类**: Utils

## 相关节点

- [File Input](../file_input) - 文件输入节点
- [Path Collector](../path_collector) - 路径收集节点

## 常见问题

**Q: 为什么某些图片无法读取尺寸？**
A: 确保文件格式被支持，损坏的文件可能无法读取

**Q: 如何根据文件大小过滤？**
A: 使用 `size_bytes` 输出端口连接到过滤节点

**Q: PDF 页数读取是否准确？**
A: 大多数标准 PDF 文件都能准确读取，某些加密或特殊格式可能有限制

## 许可证

MIT
