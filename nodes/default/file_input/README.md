# File Input Node

文件输入节点 - 统一处理各种文件输入方式，支持文件夹、文件列表、网络路径等。

## 功能

统一的文件输入接口，支持：
- 本地文件和文件夹（包括递归扫描）
- 按扩展名过滤
- 文件数量限制
- 多种排序方式
- 自动去重

## 输入

| 端口 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| input_paths | FILES | - | 输入的文件或文件夹路径（由拖拽自动传入） |
| extensions | STRING | "jpg,jpeg,png,gif,bmp,webp,tiff" | 要处理的文件扩展名，用逗号分隔。留空则处理所有文件。 |
| recursive | BOOLEAN | true | 是否递归扫描子文件夹 |
| max_files | INT | 0 | 最大文件数量。0 表示不限制 |
| sort_by | STRING | "name" | 排序方式: name(文件名), date(修改时间), size(文件大小), random(随机) |
| dedup | BOOLEAN | true | 是否按完整路径去重 |
| mode | STRING | - | 文件模式选择 |

## 输出

返回过滤和排序后的文件列表，供下游节点处理。

## 使用示例

### 处理特定格式的图片

```json
{
  "extensions": "jpg,jpeg,png",
  "recursive": true,
  "max_files": 100,
  "sort_by": "name"
}
```

### 随机抽样文件

```json
{
  "max_files": 50,
  "sort_by": "random"
}
```

### 获取最近修改的文件

```json
{
  "sort_by": "date",
  "max_files": 10
}
```

## 典型工作流

```
文件拖拽 → File Input (按扩展名过滤) → 文件列表 → 下游处理
              ↓ (设置递归)
            (搜索子目录)
```

## 扩展名过滤

### 图片格式
```
jpg,jpeg,png,gif,bmp,webp,tiff
```

### 文档格式
```
pdf,doc,docx,xls,xlsx,ppt,pptx
```

### 视频格式
```
mp4,avi,mov,mkv,wmv,flv
```

### 所有文件
```
(留空)
```

## 排序方式

| 方式 | 说明 |
|------|------|
| name | 按文件名字母序排序 |
| date | 按修改时间排序（最新优先） |
| size | 按文件大小排序（最大优先） |
| random | 随机排序 |

## 性能优化

- **限制文件数**: 使用 `max_files` 避免处理过多文件
- **有选择地递归**: 禁用 `recursive` 提高速度
- **扩展名过滤**: 先过滤减少后续处理量

## 版本信息

- **版本**: 1.0.0
- **作者**: system
- **分类**: Input

## 相关节点

- [File Info](../file_info) - 获取文件详细信息
- [Path Collector](../path_collector) - 收集多个路径

## 常见问题

**Q: 如何递归搜索所有子文件夹中的文件？**
A: 设置 `recursive: true`

**Q: 如何限制处理文件数量？**
A: 使用 `max_files` 参数，设为 0 表示无限制

**Q: 如何随机抽取文件？**
A: 设置 `sort_by: "random"`，再用 `max_files` 限制数量

**Q: 去重有什么用？**
A: 防止在多个输入源中处理同一文件两次

## 许可证

MIT
