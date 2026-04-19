# Path Collector Node

路径收集节点 - 将多条连线传入的文件路径收集为列表，供下游节点（如 SVN Upload）批量使用。

## 功能

收集来自多个上游节点的文件路径，整合成一个统一的路径列表供下游批量处理。

常用场景：
- 从多个 File Input 节点收集文件
- 合并不同来源的文件列表
- 为批量操作（如 SVN Upload）准备文件集合

## 输入

| 端口 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| path_0 | STRING | "" | 路径 0 |
| path_1 | STRING | "" | 路径 1 |
| path_2 | STRING | "" | 路径 2 |
| path_3 | STRING | "" | 路径 3 |
| path_4 | STRING | "" | 路径 4 |
| path_5 | STRING | "" | 路径 5 |
| path_6 | STRING | "" | 路径 6 |
| path_7 | STRING | "" | 路径 7 |

## 输出

| 端口 | 类型 | 说明 |
|------|------|------|
| paths | FILES | 收集到的有效路径列表 |
| count | INT | 有效路径数量 |

## 使用示例

### 合并多个文件来源

```
File Input 1 → ┐
File Input 2 → ├→ Path Collector → paths
File Input 3 → ┘        ↓
              count → Display
```

### 批量上传文件

```
File Input → Path Collector → SVN Upload
```

### 监控收集的文件数量

```
File Input → Path Collector → SVN Upload
                  ↓ count
            File Count Display
```

## 工作原理

1. 接收最多 8 条输入路径
2. 过滤掉空值和无效路径
3. 去除重复路径
4. 输出有效路径列表和数量

## 特性

- **多达 8 个输入端口**: 可同时合并来自 8 个不同节点的路径
- **自动去重**: 相同路径只保留一次
- **自动过滤**: 忽略空值和不存在的路径
- **计数输出**: 便于监控和条件控制

## 典型工作流

### 场景 1：处理来自两个不同文件夹的文件

```
File Input (folder A)
         ↓ (image files)
    path_0 ┐
File Input (folder B)     Path Collector → SVN Upload
         ↓ (image files)              ↓
    path_1 ┘                    combined paths
```

### 场景 2：从多个节点收集输出

```
Node A → string_0 → path_0 ┐
Node B → string_1 → path_1 ├→ Path Collector → SVN Upload
Node C → string_2 → path_2 ┘
```

## 配置建议

- **最多 8 个输入**: 如果需要合并超过 8 个来源，可使用多个 Path Collector 级联
- **级联使用**: 

```
Path Collector 1 → ┐
Path Collector 2 → ├→ Path Collector 3 → SVN Upload
Path Collector 3 → ┘
```

## 版本信息

- **版本**: 1.0.0
- **作者**: builtin
- **分类**: Utils

## 相关节点

- [File Input](../file_input) - 文件输入节点
- [SVN Upload](../svn_upload) - SVN 上传节点
- [File Info](../file_info) - 文件信息节点

## 常见问题

**Q: 为什么有的路径没有被收集？**
A: 检查路径是否正确、文件是否存在、是否被其他条件过滤

**Q: 如何收集超过 8 个路径？**
A: 使用多个 Path Collector 节点级联，或使用支持列表的节点

**Q: count 输出有什么用？**
A: 可用于条件判断（如路径数为 0 时跳过后续步骤）

**Q: 路径顺序会被改变吗？**
A: 会按输入顺序保留，但去重和过滤后可能有调整

## 许可证

MIT
