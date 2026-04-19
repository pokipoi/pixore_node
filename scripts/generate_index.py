"""
节点索引生成脚本
扫描所有节点并生成 GitHub 友好的索引文件（index.json）

用法:
  python generate_index.py              # 生成索引
  python generate_index.py validate     # 验证所有 manifest
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


def generate_index(nodes_dir: Path, output_file: Path, github_user: Optional[str] = None):
    """
    生成节点索引
    
    Args:
        nodes_dir: 节点目录
        output_file: 输出索引文件路径
        github_user: GitHub 用户名（用于生成完整 URL）
    """
    index = {
        'version': '1.0.0',
        'generated': datetime.now().isoformat(),
        'categories': {},
        'nodes': [],
    }
    
    # 遍历所有分类和节点
    for category_dir in sorted(nodes_dir.iterdir()):
        if not category_dir.is_dir():
            continue
        
        category = category_dir.name
        category_nodes = []
        
        # 遍历该分类下的所有节点
        for node_dir in sorted(category_dir.iterdir()):
            if not node_dir.is_dir():
                continue
            
            manifest_path = node_dir / 'manifest.json'
            if not manifest_path.exists():
                print(f"⚠️  Warning: Missing manifest at {manifest_path}")
                continue
            
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                
                # 验证必需字段
                required_fields = ['id', 'name', 'version', 'description', 'author']
                missing = [field for field in required_fields if field not in manifest]
                if missing:
                    print(f"❌ Error: Missing fields {missing} in {manifest_path}")
                    continue
                
                # 构建索引项（简略样式）
                node_id = manifest['id']
                node_entry = {
                    'id': node_id,
                    'name': manifest['name'],
                    'version': manifest['version'],
                    'author': manifest['author'],
                    'description': manifest['description'],
                    'category': category,
                    'tags': manifest.get('tags', []),
                    'rating': manifest.get('rating', 0.0),
                    'downloads': manifest.get('downloads', 0),
                }
                
                # 如果提供了 GitHub 用户名，生成完整 URL
                if github_user:
                    base_url = f"https://raw.githubusercontent.com/{github_user}/pixore_node/main"
                    node_entry['icon'] = f"{base_url}/nodes/{category}/{node_id}/icon.png"
                    node_entry['manifestUrl'] = f"{base_url}/nodes/{category}/{node_id}/manifest.json"
                    node_entry['readmeUrl'] = f"{base_url}/nodes/{category}/{node_id}/README.md"
                else:
                    node_entry['icon'] = f"nodes/{category}/{node_id}/icon.png"
                    node_entry['manifestUrl'] = f"nodes/{category}/{node_id}/manifest.json"
                    node_entry['readmeUrl'] = f"nodes/{category}/{node_id}/README.md"
                
                index['nodes'].append(node_entry)
                category_nodes.append(node_id)
                
                print(f"✅ Indexed: {category}/{node_id} v{node_entry['version']}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Error: Invalid JSON in {manifest_path}: {e}")
            except Exception as e:
                print(f"❌ Error processing {manifest_path}: {e}")
        
        # 添加分类信息
        if category_nodes:
            index['categories'][category] = {
                'count': len(category_nodes),
                'nodes': category_nodes,
            }
    
    # 写入索引文件
    os.makedirs(output_file.parent, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n✨ Index generated: {output_file}")
    print(f"   Total nodes: {len(index['nodes'])}")
    print(f"   Categories: {len(index['categories'])}")
    
    # 打印分类摘要
    if index['categories']:
        print(f"\n   📊 Categories:")
        for cat, info in index['categories'].items():
            print(f"      {cat}: {info['count']} nodes")
    
    return index


def validate_manifest(manifest_path: Path) -> bool:
    """验证单个 manifest.json"""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # 必需字段
        required = ['id', 'name', 'author', 'version', 'description', 
                   'category', 'entry_point', 'node_class']
        missing = [field for field in required if field not in manifest]
        
        if missing:
            print(f"❌ {manifest_path.parent.name}: Missing fields: {missing}")
            return False
        
        # 验证 ID 格式（kebab-case）
        node_id = manifest['id']
        if not all(c.islower() or c.isdigit() or c == '-' for c in node_id):
            print(f"❌ {manifest_path.parent.name}: Invalid id format (use kebab-case)")
            return False
        
        # 验证版本格式（semantic versioning）
        version = manifest['version']
        parts = version.split('.')
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            print(f"❌ {manifest_path.parent.name}: Invalid version format (use X.Y.Z)")
            return False
        
        # 验证分类
        valid_categories = ['inputs', 'processing', 'outputs', 'utilities', 'other']
        if manifest['category'] not in valid_categories:
            print(f"❌ {manifest_path.parent.name}: Invalid category (use one of {valid_categories})")
            return False
        
        print(f"✅ Valid: {node_id}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ {manifest_path.parent.name}: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"❌ {manifest_path.parent.name}: {e}")
        return False


def validate_all_manifests(nodes_dir: Path) -> int:
    """验证所有 manifest.json"""
    valid_count = 0
    invalid_count = 0
    
    print("🔍 Validating all manifest.json files...\n")
    
    for category_dir in sorted(nodes_dir.iterdir()):
        if not category_dir.is_dir():
            continue
        
        for node_dir in sorted(category_dir.iterdir()):
            if not node_dir.is_dir():
                continue
            
            manifest_path = node_dir / 'manifest.json'
            if manifest_path.exists():
                if validate_manifest(manifest_path):
                    valid_count += 1
                else:
                    invalid_count += 1
            else:
                print(f"⚠️  Warning: Missing manifest.json in {node_dir.name}")
    
    print(f"\n📊 Validation result: {valid_count} valid, {invalid_count} invalid")
    return invalid_count


def print_summary(index: Dict):
    """打印索引摘要"""
    print("\n" + "="*50)
    print("📋 INDEX SUMMARY")
    print("="*50)
    print(f"Generated: {index['generated']}")
    print(f"Total nodes: {len(index['nodes'])}")
    print(f"Total categories: {len(index['categories'])}")
    print()
    
    if index['categories']:
        print("Categories:")
        for cat in sorted(index['categories'].keys()):
            count = index['categories'][cat]['count']
            nodes = ', '.join(index['categories'][cat]['nodes'][:3])
            if len(index['categories'][cat]['nodes']) > 3:
                nodes += f", ... (+{len(index['categories'][cat]['nodes']) - 3} more)"
            print(f"  {cat:12} {count:2} nodes  [{nodes}]")
    print()


if __name__ == '__main__':
    import sys
    
    # 获取项目根目录
    root_dir = Path(__file__).parent.parent
    nodes_dir = root_dir / 'nodes'
    index_file = root_dir / 'index.json'
    
    if len(sys.argv) > 1 and sys.argv[1] == 'validate':
        # 验证模式
        invalid_count = validate_all_manifests(nodes_dir)
        sys.exit(invalid_count)
    else:
        # 生成索引
        print("📝 Generating node index...\n")
        
        # 可选：提供 GitHub 用户名来生成完整 URL
        # 从环境变量或命令行参数获取
        github_user = os.environ.get('GITHUB_USER') or (sys.argv[1] if len(sys.argv) > 1 else None)
        
        index = generate_index(nodes_dir, index_file, github_user)
        print_summary(index)
        print(f"✨ Done! Push this to GitHub to update your node repository.")

