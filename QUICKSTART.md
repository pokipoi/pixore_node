# 项目结构快速参考

## 📁 目录说明

```
pixore_node/
│
├─── nodes/                    # ★ 节点源文件存储
│    ├─── inputs/              # 输入类节点
│    ├─── processing/          # 处理类节点
│    ├─── outputs/             # 输出类节点
│    └─── utilities/           # 工具节点
│
├─── scripts/                  # 自动化脚本
│    └─── generate_index.py    # 生成 GitHub 友好的索引
│
├─── schemas/                  # 数据规范定义
│    └─── manifest-schema.json # manifest.json 的 Schema
│
├─── docs/                     # 文档
│    ├─── CLIENT_INTEGRATION.md # ★ 客户端集成指南
│    ├─── NODE_TEMPLATE.md     # 创建新节点模板
│    └── README.md             # 项目说明
│
├─── index.json                # ★ 完整节点索引（在 GitHub 上）
├─── README.md                 # 项目说明
├─── package.json              # 项目元数据
└─── LICENSE
```

## 🎯 核心概念

### GitHub 托管架构
- ✅ 所有文件存储在 GitHub 仓库
- ✅ 无需额外服务器
- ✅ 客户端直接从 GitHub Raw URL 获取数据
- ✅ 通过 git push 自动发布更新

### 两种 API 响应格式

#### 简略样式（列表页面）
**来源**: `index.json`

```json
{
  "id": "string-input",
  "name": "String Input",
  "author": "pokipoi",
  "version": "1.0.0",
  "description": "字符串输入节点",
  "category": "inputs",
  "rating": 4.8,
  "downloads": 23567,
  "tags": ["input", "text"],
  "icon": "https://raw.githubusercontent.com/.../icon.png",
  "manifestUrl": "https://raw.githubusercontent.com/.../manifest.json"
}
```

#### 详情样式（详情页面）
**来源**: `nodes/{category}/{node-id}/manifest.json`

完整的 manifest.json 文件，包含：
- 完整描述和详细说明
- 输入/输出端口定义
- 依赖、版本历史、链接等

## 🚀 快速命令

```bash
# 生成/更新索引
python scripts/generate_index.py

# 验证所有 manifest
python scripts/generate_index.py validate

# 提交到 GitHub
git add .
git commit -m "Update nodes"
git push origin main
```

## 📝 创建新节点（5 步）

### 1️⃣ 创建目录

```bash
mkdir -p nodes/processing/my-node-id
cd nodes/processing/my-node-id
```

### 2️⃣ 创建 manifest.json

参考 [docs/NODE_TEMPLATE.md](docs/NODE_TEMPLATE.md)

```json
{
  "id": "my-node-id",
  "name": "My Node",
  "author": "Your Name",
  "version": "1.0.0",
  "description": "节点描述",
  "category": "processing",
  "entry_point": "main.py",
  "node_class": "MyNodeClass",
  "inputs": [...],
  "outputs": [...]
}
```

### 3️⃣ 创建 main.py

参考 [docs/NODE_TEMPLATE.md](docs/NODE_TEMPLATE.md)

```python
class MyNodeClass:
    def process(self, input_data):
        # 实现节点逻辑
        return {'output': result}
```

### 4️⃣ 生成索引

```bash
python scripts/generate_index.py
```

### 5️⃣ Push 到 GitHub

```bash
git add nodes/ index.json
git commit -m "Add node: My Node"
git push origin main
```

## 🔗 GitHub URLs

所有资源都通过 GitHub Raw Content URL 访问：

```
https://raw.githubusercontent.com/{user}/{repo}/main/{path}
```

| 资源 | URL |
|------|-----|
| 索引 | `.../index.json` |
| 详情 | `.../nodes/inputs/string-input/manifest.json` |
| 图标 | `.../nodes/inputs/string-input/icon.png` |
| 代码 | `.../nodes/inputs/string-input/main.py` |

## 📱 客户端使用

### Python 客户端

```python
import requests

REPO = "https://raw.githubusercontent.com/YOUR_USER/pixore_node/main"

# 获取所有节点
index = requests.get(f"{REPO}/index.json").json()
for node in index['nodes']:
    print(f"{node['name']} v{node['version']}")

# 获取节点详情
detail = requests.get(
    f"{REPO}/nodes/{node['category']}/{node['id']}/manifest.json"
).json()
print(detail['inputs'])
```

详见 [docs/CLIENT_INTEGRATION.md](docs/CLIENT_INTEGRATION.md)

### JavaScript 客户端

```javascript
const REPO = "https://raw.githubusercontent.com/YOUR_USER/pixore_node/main";

// 获取索引
const index = await fetch(`${REPO}/index.json`).then(r => r.json());

// 获取详情
const detail = await fetch(
  `${REPO}/nodes/${category}/${nodeId}/manifest.json`
).then(r => r.json());
```

详见 [docs/CLIENT_INTEGRATION.md](docs/CLIENT_INTEGRATION.md)

## 📊 Manifest 必需字段

```json
{
  "id": "kebab-case-id",
  "name": "Display Name",
  "author": "Author Name",
  "version": "1.0.0",
  "description": "Short description",
  "category": "inputs|processing|outputs|utilities",
  "entry_point": "main.py",
  "node_class": "ClassName"
}
```

## 🔍 文件位置速查

| 你需要... | 文件位置 |
|-----------|---------|
| 创建新节点 | `nodes/{category}/{node-id}/` |
| 节点模板 | `docs/NODE_TEMPLATE.md` |
| 客户端代码 | `docs/CLIENT_INTEGRATION.md` |
| Manifest Schema | `schemas/manifest-schema.json` |
| 生成索引 | `python scripts/generate_index.py` |
| 验证 manifest | `python scripts/generate_index.py validate` |

## 💾 GitHub 工作流

```
本地开发
  ↓
添加/修改节点
  ↓
运行: python scripts/generate_index.py
  ↓
git commit -m "message"
  ↓
git push origin main
  ↓
更新自动发布到 GitHub
  ↓
客户端自动获取最新数据
```

## 📈 下一步

- [ ] 重新组织现有节点到新结构
- [ ] 验证所有 manifest 文件
- [ ] Push 到 GitHub
- [ ] 更新 GitHub 用户名（用于生成完整 URLs）
- [ ] 测试客户端集成
- [ ] 添加 README 到各节点目录
- [ ] 创建发行版（Release）

## ❓ 常见问题

**Q: 如何更新已发布的节点？**
A: 修改节点文件，运行 `generate_index.py`，push 到 GitHub。客户端将自动获取最新版本。

**Q: 如何支持多个 Python 版本？**
A: 在 manifest.json 中指定 `pythonVersion` 字段。

**Q: 如何添加节点依赖？**
A: 在 manifest.json 中的 `dependencies` 字段列出，或创建 requirements.txt。

**Q: 客户端如何处理离线？**
A: 缓存 index.json 和相关 manifest.json 文件到本地。

## 📞 帮助

- 查看 [docs/NODE_TEMPLATE.md](docs/NODE_TEMPLATE.md) 了解如何创建节点
- 查看 [docs/CLIENT_INTEGRATION.md](docs/CLIENT_INTEGRATION.md) 了解如何集成客户端
- 查看现有节点实现作为参考

