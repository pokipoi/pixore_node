# 创建新节点模板

## 📁 目录结构

```
nodes/
└── {category}/          # inputs, processing, utilities, outputs
    └── {node-id}/       # 使用 kebab-case，如 my-custom-node
        ├── main.py                 # 必需：节点实现
        ├── manifest.json           # 必需：节点元数据
        ├── icon.png               # 建议：节点图标（256x256px）
        ├── README.md              # 可选：节点文档
        └── requirements.txt       # 可选：Python 依赖
```

## 📝 manifest.json 模板

### 最小化版本

```json
{
  "id": "my-custom-node",
  "name": "My Custom Node",
  "author": "Your Name",
  "version": "1.0.0",
  "description": "简短描述（≤100字）",
  "category": "processing",
  "entry_point": "main.py",
  "node_class": "MyCustomNode",
  
  "inputs": [
    {
      "name": "input1",
      "type": "STRING",
      "description": "输入说明"
    }
  ],
  
  "outputs": [
    {
      "name": "output1",
      "type": "STRING",
      "description": "输出说明"
    }
  ]
}
```

### 完整版本

```json
{
  "id": "image-processor",
  "name": "Image Processor",
  "author": "Your Name / Team",
  "version": "2.1.0",
  "description": "图像处理节点：调整大小、旋转、裁剪等操作。",
  "longDescription": "# Image Processor\n\n这是一个功能完整的图像处理节点，支持多种图像变换操作...\n\n## 特性\n\n- 快速高效的处理\n- 支持多种格式\n- GPU 加速",
  
  "category": "processing",
  "tags": ["image", "processing", "transform"],
  
  "entry_point": "main.py",
  "node_class": "ImageProcessorNode",
  
  "pythonVersion": "3.8",
  
  "icon": "icon.png",
  "website": "https://example.com",
  "documentation": "https://docs.example.com/nodes/image-processor",
  "repository": "https://github.com/user/image-processor",
  "license": "MIT",
  
  "inputs": [
    {
      "name": "image",
      "type": "IMAGE",
      "description": "输入图像",
      "required": true
    },
    {
      "name": "width",
      "type": "NUMBER",
      "description": "目标宽度（像素）",
      "default": 512,
      "required": false
    },
    {
      "name": "height",
      "type": "NUMBER",
      "description": "目标高度（像素）",
      "default": 512,
      "required": false
    }
  ],
  
  "outputs": [
    {
      "name": "image",
      "type": "IMAGE",
      "description": "处理后的图像"
    },
    {
      "name": "size",
      "type": "JSON",
      "description": "输出图像尺寸信息"
    }
  ],
  
  "dependencies": {
    "Pillow": ">=9.0",
    "numpy": ">=1.21"
  },
  
  "screenshots": [
    {
      "url": "screenshot-1.png",
      "caption": "处理前后对比"
    }
  ]
}
```

## 🐍 main.py 模板

### 基础节点实现

```python
"""
Image Processor Node
处理和变换图像
"""
from typing import Any, Dict, Tuple


class ImageProcessorNode:
    """图像处理节点"""
    
    def __init__(self):
        """初始化节点"""
        self.name = "Image Processor"
        self.version = "1.0.0"
    
    def process(self, image: Any, width: int = 512, height: int = 512) -> Dict[str, Any]:
        """
        处理图像
        
        Args:
            image: 输入图像对象（或路径）
            width: 目标宽度
            height: 目标高度
        
        Returns:
            dict: 包含处理结果的字典
                - image: 处理后的图像
                - size: 图像尺寸信息
        """
        try:
            from PIL import Image
            import numpy as np
            
            # 如果输入是路径，加载图像
            if isinstance(image, str):
                img = Image.open(image)
            else:
                img = image
            
            # 调整大小
            img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # 获取信息
            size_info = {
                'original': {
                    'width': img.width,
                    'height': img.height
                },
                'processed': {
                    'width': img_resized.width,
                    'height': img_resized.height
                }
            }
            
            return {
                'image': img_resized,
                'size': size_info
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'image': None,
                'size': None
            }


# 导出节点类（必需）
__all__ = ['ImageProcessorNode']
```

### 具有配置的节点

```python
"""
Custom Processing Node
带配置参数的节点
"""
from typing import Any, Dict, List


class CustomProcessingNode:
    """自定义处理节点"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        'mode': 'fast',
        'quality': 85,
        'enable_cache': True,
    }
    
    def __init__(self, config: Dict = None):
        """
        初始化节点
        
        Args:
            config: 配置字典
        """
        self.config = {**self.DEFAULT_CONFIG}
        if config:
            self.config.update(config)
    
    def process(self, data: Any, operation: str = None) -> Dict[str, Any]:
        """处理数据"""
        try:
            if operation == 'transform':
                return self._transform(data)
            elif operation == 'analyze':
                return self._analyze(data)
            else:
                return {'error': 'Unknown operation'}
        
        except Exception as e:
            return {'error': str(e)}
    
    def _transform(self, data: Any) -> Dict:
        """变换操作"""
        # 实现你的逻辑
        return {'result': data, 'operation': 'transform'}
    
    def _analyze(self, data: Any) -> Dict:
        """分析操作"""
        # 实现你的逻辑
        return {'result': data, 'operation': 'analyze'}


__all__ = ['CustomProcessingNode']
```

## 📋 requirements.txt 模板

如果你的节点需要额外的 Python 依赖：

```
Pillow>=9.0
numpy>=1.21
opencv-python>=4.5
pandas>=1.3
scikit-image>=0.19
```

## 📖 README.md 模板

```markdown
# Image Processor Node

处理和变换图像的节点。

## 功能

- ✅ 调整大小
- ✅ 旋转
- ✅ 裁剪
- ✅ 格式转换

## 输入

- **image** (IMAGE): 输入图像
- **width** (NUMBER): 目标宽度，默认 512
- **height** (NUMBER): 目标高度，默认 512

## 输出

- **image** (IMAGE): 处理后的图像
- **size** (JSON): 尺寸信息

## 依赖

- Python >= 3.8
- Pillow >= 9.0

## 安装

将此节点放在 `nodes/processing/` 目录中。

## 用法

```python
from main import ImageProcessorNode

node = ImageProcessorNode()
result = node.process('input.jpg', width=1024, height=768)
print(result['size'])
```

## 配置

修改 manifest.json 来自定义节点行为。

## 许可证

MIT

## 作者

Your Name
```

## ✅ 验证清单

创建新节点时，确保：

- [ ] 节点目录使用 kebab-case（如 `my-awesome-node`）
- [ ] manifest.json 包含所有必需字段
- [ ] 版本号遵循语义版本（X.Y.Z）
- [ ] 分类在允许的列表中
- [ ] main.py 导出正确的类名
- [ ] 图标是 PNG 格式（建议 256x256px）
- [ ] ID 和节点目录名称一致
- [ ] description 字段少于 100 字符

## 🚀 发布步骤

### 1. 创建分支

```bash
git checkout -b feature/add-new-node
```

### 2. 添加节点文件

```bash
mkdir -p nodes/processing/my-new-node
# 添加 main.py, manifest.json, icon.png 等
```

### 3. 生成索引

```bash
python scripts/generate_index.py
```

### 4. 提交和推送

```bash
git add nodes/ index.json
git commit -m "Add new node: My New Node"
git push origin feature/add-new-node
```

### 5. 创建 Pull Request

在 GitHub 上创建 PR，描述你的新节点。

## 📚 数据类型

支持的数据类型：

| 类型 | 说明 |
|------|------|
| STRING | 文本字符串 |
| NUMBER | 数字（整数或浮点数） |
| BOOLEAN | 布尔值 |
| IMAGE | 图像对象 |
| FILE | 文件对象或路径 |
| JSON | JSON 对象或数组 |
| ARRAY | 数组/列表 |
| ANY | 任意类型 |

## 💡 最佳实践

### 1. 错误处理

```python
def process(self, data):
    try:
        return {'result': self._do_work(data)}
    except ValueError as e:
        return {'error': f'Invalid input: {e}'}
    except Exception as e:
        return {'error': f'Processing failed: {e}'}
```

### 2. 文档化

```python
def process(self, data: str, mode: str = 'fast') -> Dict:
    """
    处理数据
    
    Args:
        data: 输入数据
        mode: 处理模式 ('fast' 或 'accurate')
    
    Returns:
        处理结果字典
    """
```

### 3. 测试

```python
# test_node.py
from main import MyCustomNode

def test_basic():
    node = MyCustomNode()
    result = node.process('input')
    assert 'result' in result
    assert result['error'] is None
```

## 📞 获取帮助

- 查看现有节点的实现
- 参考 [schemas/manifest-schema.json](../../schemas/manifest-schema.json)
- 提交 Issue 提出问题
