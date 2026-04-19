# 客户端集成指南

## GitHub 数据源

所有节点数据直接从 GitHub 获取，无需额外服务器。

## 🔗 URL 模式

```
https://raw.githubusercontent.com/{user}/{repo}/main/...
```

- `{user}`: GitHub 用户名
- `{repo}`: 仓库名 (pixore_node)

## 📥 获取节点列表（简略样式）

### URL

```
https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main/index.json
```

### 响应格式

```json
{
  "version": "1.0.0",
  "generated": "2026-04-19T10:30:00Z",
  "categories": {
    "inputs": {
      "count": 2,
      "nodes": ["string-input", "file-input"]
    }
  },
  "nodes": [
    {
      "id": "string-input",
      "name": "String Input",
      "author": "pokipoi",
      "version": "1.0.0",
      "description": "字符串输入节点",
      "category": "inputs",
      "icon": "https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main/nodes/inputs/string-input/icon.png",
      "rating": 4.8,
      "downloads": 23567,
      "tags": ["input", "text"]
    }
  ]
}
```

### Python 示例

```python
import requests

REPO_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main"

def get_node_list():
    """获取节点列表"""
    response = requests.get(f"{REPO_URL}/index.json")
    return response.json()

def filter_nodes(nodes, category=None, search=None):
    """过滤节点"""
    results = nodes['nodes']
    
    if category:
        results = [n for n in results if n['category'] == category]
    
    if search:
        search_lower = search.lower()
        results = [n for n in results if 
                  search_lower in n['name'].lower() or
                  search_lower in n['description'].lower() or
                  any(search_lower in tag.lower() for tag in n.get('tags', []))]
    
    return results

# 使用
nodes = get_node_list()
input_nodes = filter_nodes(nodes, category='inputs')
image_nodes = filter_nodes(nodes, search='image')
```

### JavaScript 示例

```javascript
const REPO_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main";

async function getNodeList() {
  const response = await fetch(`${REPO_URL}/index.json`);
  return response.json();
}

async function filterNodes(category = null, search = null) {
  const data = await getNodeList();
  let results = data.nodes;
  
  if (category) {
    results = results.filter(n => n.category === category);
  }
  
  if (search) {
    const searchLower = search.toLowerCase();
    results = results.filter(n =>
      n.name.toLowerCase().includes(searchLower) ||
      n.description.toLowerCase().includes(searchLower) ||
      (n.tags || []).some(t => t.toLowerCase().includes(searchLower))
    );
  }
  
  return results;
}

// 使用
const nodes = await getNodeList();
const inputNodes = await filterNodes('inputs');
const imageNodes = await filterNodes(null, 'image');
```

## 📄 获取节点详情（详情样式）

### URL

```
https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main/nodes/{category}/{node-id}/manifest.json
```

### 响应格式

完整的 manifest.json 文件包含所有详情信息。

### Python 示例

```python
def get_node_detail(category, node_id):
    """获取节点详情"""
    url = f"{REPO_URL}/nodes/{category}/{node_id}/manifest.json"
    response = requests.get(url)
    return response.json()

# 使用
detail = get_node_detail('inputs', 'string-input')
print(detail['name'])
print(detail['description'])
print(detail['inputs'])  # 输入端口
print(detail['outputs'])  # 输出端口
```

### JavaScript 示例

```javascript
async function getNodeDetail(category, nodeId) {
  const url = `${REPO_URL}/nodes/${category}/${nodeId}/manifest.json`;
  const response = await fetch(url);
  return response.json();
}

// 使用
const detail = await getNodeDetail('inputs', 'string-input');
console.log(detail.inputs);
console.log(detail.outputs);
```

## 🖼️ 获取节点图标

### URL

```
https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main/nodes/{category}/{node-id}/icon.png
```

### 示例

```html
<img src="https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main/nodes/inputs/string-input/icon.png" />
```

## 📥 获取节点代码

### URL

```
https://raw.githubusercontent.com/YOUR_USERNAME/pixore_node/main/nodes/{category}/{node-id}/main.py
```

## 🌲 完整客户端示例

### Python

```python
import requests
from typing import List, Dict, Optional

class NodeRepositoryClient:
    """Pixore 节点仓库客户端"""
    
    def __init__(self, username: str, repo: str = "pixore_node", branch: str = "main"):
        self.repo_url = f"https://raw.githubusercontent.com/{username}/{repo}/{branch}"
        self._cache = None
    
    def get_all_nodes(self, use_cache: bool = True) -> Dict:
        """获取所有节点"""
        if use_cache and self._cache:
            return self._cache
        
        response = requests.get(f"{self.repo_url}/index.json")
        response.raise_for_status()
        self._cache = response.json()
        return self._cache
    
    def get_node_list(self, category: Optional[str] = None, 
                     search: Optional[str] = None) -> List[Dict]:
        """获取节点列表"""
        data = self.get_all_nodes()
        nodes = data['nodes']
        
        if category:
            nodes = [n for n in nodes if n['category'] == category]
        
        if search:
            search_lower = search.lower()
            nodes = [n for n in nodes if
                    search_lower in n['name'].lower() or
                    search_lower in n['description'].lower()]
        
        return nodes
    
    def get_node_detail(self, category: str, node_id: str) -> Dict:
        """获取节点详情"""
        url = f"{self.repo_url}/nodes/{category}/{node_id}/manifest.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_categories(self) -> Dict:
        """获取分类统计"""
        data = self.get_all_nodes()
        return data.get('categories', {})
    
    def get_node_icon_url(self, category: str, node_id: str) -> str:
        """获取节点图标 URL"""
        return f"{self.repo_url}/nodes/{category}/{node_id}/icon.png"
    
    def get_node_code_url(self, category: str, node_id: str) -> str:
        """获取节点代码 URL"""
        return f"{self.repo_url}/nodes/{category}/{node_id}/main.py"

# 使用示例
if __name__ == '__main__':
    client = NodeRepositoryClient('YOUR_USERNAME')
    
    # 获取所有节点
    all_nodes = client.get_node_list()
    print(f"总共 {len(all_nodes)} 个节点")
    
    # 按分类获取
    input_nodes = client.get_node_list(category='inputs')
    print(f"输入节点: {len(input_nodes)} 个")
    
    # 搜索
    image_nodes = client.get_node_list(search='image')
    print(f"搜索 'image': {len(image_nodes)} 个")
    
    # 获取详情
    if input_nodes:
        detail = client.get_node_detail(input_nodes[0]['category'], input_nodes[0]['id'])
        print(f"\n详情: {detail['name']}")
        print(f"作者: {detail['author']}")
        print(f"输入: {detail.get('inputs', [])}")
```

### JavaScript/前端框架

```javascript
class NodeRepositoryClient {
  constructor(username, repo = 'pixore_node', branch = 'main') {
    this.repoUrl = `https://raw.githubusercontent.com/${username}/${repo}/${branch}`;
    this.cache = null;
  }

  async getAllNodes(useCache = true) {
    if (useCache && this.cache) return this.cache;
    const res = await fetch(`${this.repoUrl}/index.json`);
    this.cache = await res.json();
    return this.cache;
  }

  async getNodeList(category = null, search = null) {
    const data = await this.getAllNodes();
    let nodes = data.nodes;

    if (category) {
      nodes = nodes.filter(n => n.category === category);
    }

    if (search) {
      const searchLower = search.toLowerCase();
      nodes = nodes.filter(n =>
        n.name.toLowerCase().includes(searchLower) ||
        n.description.toLowerCase().includes(searchLower)
      );
    }

    return nodes;
  }

  async getNodeDetail(category, nodeId) {
    const url = `${this.repoUrl}/nodes/${category}/${nodeId}/manifest.json`;
    const res = await fetch(url);
    return res.json();
  }

  getNodeIconUrl(category, nodeId) {
    return `${this.repoUrl}/nodes/${category}/${nodeId}/icon.png`;
  }

  async getCategories() {
    const data = await this.getAllNodes();
    return data.categories || {};
  }
}

// 使用示例
const client = new NodeRepositoryClient('YOUR_USERNAME');

// 获取列表
const nodes = await client.getNodeList('inputs');
nodes.forEach(node => {
  console.log(`${node.name} (${node.version})`);
});

// 获取详情
const detail = await client.getNodeDetail('inputs', 'string-input');
console.log(detail.description);
```

## 💡 最佳实践

### 1. 缓存索引

避免频繁请求 index.json：

```python
import time
from datetime import timedelta

class CachedClient(NodeRepositoryClient):
    def __init__(self, *args, cache_ttl=3600, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_ttl = cache_ttl
        self.cache_time = 0
    
    def get_all_nodes(self, use_cache=True):
        now = time.time()
        if use_cache and self._cache and (now - self.cache_time) < self.cache_ttl:
            return self._cache
        
        result = super().get_all_nodes(use_cache=False)
        self.cache_time = now
        return result
```

### 2. 错误处理

```python
try:
    detail = client.get_node_detail('inputs', 'string-input')
except requests.exceptions.HTTPError as e:
    print(f"节点不存在: {e}")
except requests.exceptions.ConnectionError:
    print("网络连接失败")
```

### 3. 离线支持

```python
import json

def save_cache(client, filename='nodes_cache.json'):
    """保存索引到本地"""
    data = client.get_all_nodes()
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_cache(filename='nodes_cache.json'):
    """从本地加载缓存"""
    with open(filename, 'r') as f:
        return json.load(f)
```

## 🔐 安全考虑

- 使用 HTTPS 访问所有资源
- 验证 manifest.json 的完整性
- 对 node_id 进行验证（只允许 alphanumeric 和 dash）

## 📊 性能优化

- 缓存索引文件（1 小时更新一次）
- 仅在需要时获取详情
- 使用 CDN 加速（GitHub 已自带 CDN）

## ❓ 常见问题

**Q: 索引多久更新一次？**
A: 每次 push 代码到 GitHub 后，下一次拉取会获取最新数据。

**Q: 如何离线使用？**
A: 保存 index.json 和相关 manifest.json 文件到本地。

**Q: 如何处理私有仓库？**
A: 使用 GitHub Token 认证请求。

```python
headers = {'Authorization': f'token {GITHUB_TOKEN}'}
response = requests.get(url, headers=headers)
```
