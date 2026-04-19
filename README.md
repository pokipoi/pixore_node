# Pixore Node Repository

GitHub 托管的在线节点仓库，客户端直接从 GitHub 获取节点数据和文件。

## 📋 项目结构

```
pixore_node/
├── 📂 nodes/                       # 节点集合（按分类组织）
│   ├── 📂 inputs/                  # 输入类节点
│   │   ├── 📂 string-input/
│   │   │   ├── main.py             # 节点实现
│   │   │   ├── manifest.json       # 节点元数据
│   │   │   ├── icon.png            # 节点图标
│   │   │   └── README.md           # 节点说明
│   │   └── 📂 file-input/
│   │
│   ├── 📂 processing/              # 处理类节点
│   │   ├── 📂 pil-image-resize/
│   │   └── 📂 path-collector/
│   │
│   └── 📂 utilities/               # 工具类节点
│       └── 📂 svn-upload/
│
├── 📂 scripts/                     # 自动化脚本
│   └── generate_index.py           # 生成 GitHub 友好的索引
│
├── 📂 schemas/                     # 数据定义
│   └── manifest-schema.json        # manifest.json Schema
│
├── 📂 docs/                        # 文档
│   ├── CLIENT_INTEGRATION.md       # 客户端集成指南
│   └── NODE_TEMPLATE.md            # 创建新节点模板
│
├── 📄 index.json                   # 完整节点索引（在 GitHub 中可访问）
├── 📄 README.md                    # 本文件
├── 📄 package.json                 # 项目信息
└── 📄 LICENSE

```

## 🎨 两种展示样式

节点数据支持两种展示格式：

### 1️⃣ **简略样式（List View）** 

用于列表页面展示，包含基本信息：

```json
{
  "id": "string-input",
  "name": "String Input",
  "author": "pokipoi",
  "version": "1.0.0",
  "downloads": 23567,
  "icon": "icon.png",
  "description": "字符串输入节点",
  "category": "inputs",
  "rating": 4.8,
  "tags": ["input", "text"],
  "manifestUrl": "nodes/inputs/string-input/manifest.json",
  "readmeUrl": "nodes/inputs/string-input/README.md"
}
```

### 2️⃣ **详情样式（Detail View）**

用于详情页面展示，包含完整信息：

从 `nodes/{category}/{node-id}/manifest.json` 获取完整 manifest 文件，包含：
- 完整描述和 Markdown 格式的详细说明
- 输入/输出端口定义
- 依赖列表和版本历史
- 网站、文档、仓库链接
- 截图等

## 🚀 快速开始

### 获取节点列表

客户端从 GitHub 直接获取索引：

```
https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main/index.json
```

### 获取节点详情

```
https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main/nodes/{category}/{node-id}/manifest.json
```

### 获取节点文档

每个节点包含 README.md 文档，可通过 index.json 的 `readmeUrl` 字段快速访问：

```
https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main/nodes/{category}/{node-id}/README.md
```

### 下载节点

```
https://github.com/YOUR_USERNAME/pixore_node/archive/main.zip
```

## 🔗 GitHub URLs

所有文件都通过 GitHub Raw Content 访问：

| 内容 | URL |
|------|-----|
| 节点索引 | `https://raw.githubusercontent.com/{user}/{repo}/main/index.json` |
| 节点详情 | `https://raw.githubusercontent.com/{user}/{repo}/main/nodes/{category}/{node-id}/manifest.json` |
| 节点文档 | `https://raw.githubusercontent.com/{user}/{repo}/main/nodes/{category}/{node-id}/README.md` |
| 节点图标 | `https://raw.githubusercontent.com/{user}/{repo}/main/nodes/{category}/{node-id}/icon.png` |
| 节点代码 | `https://raw.githubusercontent.com/{user}/{repo}/main/nodes/{category}/{node-id}/main.py` |

## 📝 创建新节点

### 1. 创建目录结构

```
nodes/
└── category/          # inputs, processing, utilities 等
    └── node-id/       # 使用 kebab-case
        ├── main.py
        ├── manifest.json
        ├── icon.png
        └── README.md
```

### 2. 编写 manifest.json

参考 [NODE_TEMPLATE.md](docs/NODE_TEMPLATE.md)

### 3. 生成索引

```bash
python scripts/generate_index.py
```

### 4. Push 到 GitHub

```bash
git add nodes/
git commit -m "Add new node: {node-name}"
git push origin main
```

索引文件会自动更新。

## 📱 客户端集成

见 [CLIENT_INTEGRATION.md](docs/CLIENT_INTEGRATION.md)

## 📊 API 端点一览

| 端点 | 说明 |
|------|------|
| GET `index.json` | 获取所有节点列表（简略） |
| GET `nodes/{category}/{id}/manifest.json` | 获取节点详情（详情） |

## 🔍 数据规范

- **Manifest Schema**: [schemas/manifest-schema.json](schemas/manifest-schema.json)
- **节点模板**: [docs/NODE_TEMPLATE.md](docs/NODE_TEMPLATE.md)

## 🎯 特性

✅ GitHub 原生托管，无需额外服务
✅ 两种展示样式（简略/详情）
✅ 自动索引生成
✅ 节点分类管理
✅ 版本管理
✅ 原生支持 GitHub 功能（发行版、标签等）

## 📄 许可证

MIT License
