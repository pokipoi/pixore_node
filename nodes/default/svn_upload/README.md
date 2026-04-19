# SVN Upload Node

SVN 上传节点 - 将文件列表提交到 SVN 仓库（svn add + svn commit）。

## 功能

自动化的 SVN 文件提交流程，支持：
- 批量提交多个文件
- 自定义提交说明
- SVN 身份验证
- 文件存在性验证

典型场景：
- 自动化版本控制工作流
- 资源文件批量提交
- 构建输出自动归档

## 输入

| 端口 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| paths | FILES | - | 要上传的文件路径列表（来自 PathCollector） |
| repo_url | STRING | "" | SVN 仓库 URL，留空则使用文件所在工作副本 |
| commit_msg | STRING | "Auto commit by workflow" | 提交说明 |
| username | STRING | "" | SVN 用户名（留空使用系统凭据） |
| password | STRING | "" | SVN 密码（留空使用系统凭据） |
| verify_exists | BOOLEAN | true | 提交前验证文件存在，防止上传不完整 |

## 输出

| 端口 | 类型 | 说明 |
|------|------|------|
| status | STRING | 执行结果描述 |
| committed | INT | 成功提交的文件数 |

## 使用示例

### 基础提交

```json
{
  "commit_msg": "Update resource files"
}
```

### 提交到特定仓库

```json
{
  "repo_url": "svn://svn.example.com/project/trunk",
  "commit_msg": "Deploy build artifacts",
  "username": "deploy_user"
}
```

### 带身份验证的提交

```json
{
  "repo_url": "https://svn.example.com/repo",
  "commit_msg": "Auto-generated assets",
  "username": "user@example.com",
  "password": "${SVN_PASSWORD}",
  "verify_exists": true
}
```

## 典型工作流

```
File Input → Path Collector → SVN Upload → status & committed count
```

### 完整示例流程

```
1. File Input
   ↓ 扫描工作目录，收集修改的文件

2. Path Collector
   ↓ 整合来自多个来源的文件列表

3. SVN Upload
   ├─ 验证文件存在 (verify_exists=true)
   ├─ 执行 svn add
   ├─ 执行 svn commit
   └─ 输出结果和统计信息

4. 后续处理
   ├─ status → 结果通知
   └─ committed → 统计报告
```

## SVN 命令流程

### 逐步执行过程

```bash
# 1. 验证文件存在
if verify_exists:
    for each file in paths:
        check if file exists

# 2. 添加文件到 SVN
svn add file1 file2 file3

# 3. 提交到仓库
svn commit -m "Auto commit by workflow" file1 file2 file3
```

## 身份验证

### 使用系统凭据（推荐）

```json
{
  "username": "",
  "password": ""
}
```

条件：
- 系统已配置 SVN 凭据缓存
- 或已登录 SVN 账户

### 使用指定凭据

```json
{
  "username": "myuser",
  "password": "mypass"
}
```

⚠️ 注意：密码会在日志中显示，生产环境建议使用环境变量

### 使用环境变量

```json
{
  "username": "${SVN_USER}",
  "password": "${SVN_PASSWORD}"
}
```

## 仓库 URL 说明

### 本地工作副本

```json
{
  "repo_url": ""
}
```

提交到当前工作目录所属的仓库

### 远程仓库

```json
{
  "repo_url": "svn://svn.example.com/project/trunk"
}
```

支持的协议：
- `svn://` - SVN 协议
- `http://` / `https://` - HTTP(S) 协议
- `file://` - 本地文件系统

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| "File not found" | 文件不存在 | 检查文件路径，启用 `verify_exists` |
| "Permission denied" | 权限不足 | 检查 SVN 账户权限 |
| "Authentication failed" | 身份验证失败 | 检查用户名和密码 |
| "Working copy locked" | SVN 工作副本被锁定 | 运行 `svn cleanup` |

## 性能优化

- **批量提交**: 一次提交多个文件比单个文件多次提交更快
- **文件验证**: 启用 `verify_exists` 会增加一点开销，但可防止失败
- **网络考虑**: 远程仓库提交速度取决于网络和文件大小

## 版本信息

- **版本**: 1.0.0
- **作者**: builtin
- **分类**: Output

## 相关节点

- [Path Collector](../path_collector) - 收集路径列表
- [File Input](../file_input) - 文件输入节点
- [File Info](../file_info) - 文件信息节点

## 常见问题

**Q: 如何提交到特定 SVN 分支？**
A: 在 `repo_url` 中指定完整的分支路径

**Q: 如果提交失败，文件会被回滚吗？**
A: SVN 会自动回滚失败的提交，请检查错误日志

**Q: 可以提交到多个仓库吗？**
A: 使用多个 SVN Upload 节点

**Q: 如何使用 SSH 认证？**
A: 确保 SVN 客户端配置了 SSH 密钥，使用 `svn+ssh://` 协议

**Q: 工作流中如何条件性跳过提交？**
A: 检查 `committed` 输出，如果为 0 则没有文件被提交

## 安全建议

⚠️ **安全提示**：
- 不要在代码或配置文件中硬编码密码
- 使用环境变量存储敏感信息
- 优先使用系统凭据缓存
- 在生产环境使用 SSH 密钥认证
- 定期审计 SVN 提交日志

## 许可证

MIT
