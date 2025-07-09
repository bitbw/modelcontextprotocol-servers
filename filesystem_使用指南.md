# 本地 Filesystem MCP 服务器使用指南

## 🎯 什么是 Filesystem 服务器？

Filesystem 服务器让 Claude 能够安全地操作您的文件系统，包括：

- 📁 **读取文件** - 查看文件内容
- ✏️ **编辑文件** - 修改文件内容（支持预览模式）
- 📝 **创建文件** - 写入新文件
- 📂 **目录操作** - 创建、列出、移动文件夹
- 🔍 **搜索文件** - 在目录中搜索文件

## 🔒 安全特性

- ✅ **沙盒模式** - 只能访问您指定的目录
- ❌ **访问控制** - 无法访问系统敏感文件
- 🔐 **路径验证** - 防止路径遍历攻击

## 🚀 配置步骤

### 1. 编译服务器（已完成）

已编译到：`D:/bowen/MCP/servers/src/filesystem/dist/index.js`

### 2. Claude Desktop 配置

将以下配置添加到您的 `claude_desktop_config.json` 文件：

#### 基础配置（仅测试目录）：
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": [
        "D:/bowen/MCP/servers/src/filesystem/dist/index.js",
        "D:/bowen/MCP/servers/src/filesystem/test_files"
      ]
    }
  }
}
```

#### 实用配置（多个目录）：
```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time"]
    },
    "filesystem": {
      "command": "node",
      "args": [
        "D:/bowen/MCP/servers/src/filesystem/dist/index.js",
        "C:/Users/YourUsername/Desktop",
        "C:/Users/YourUsername/Documents",
        "D:/bowen/MCP"
      ]
    }
  }
}
```

### 3. 重启 Claude Desktop

配置完成后，重启 Claude Desktop 加载新服务器。

## 🧪 测试功能

### 基础文件操作
**读取文件：**
```
请帮我读取 test_files/hello.txt 的内容
```

**列出目录：**
```
请列出 test_files 目录下的所有文件
```

**创建文件：**
```
请在 test_files 目录下创建一个名为 note.txt 的文件，内容是 "这是我的笔记"
```

**编辑文件：**
```
请将 test_files/hello.txt 中的 "Hello" 替换为 "你好"
```

### 高级功能
**搜索文件：**
```
请在 test_files 目录中搜索所有包含 "test" 的文件
```

**文件信息：**
```
请告诉我 test_files/hello.txt 的详细信息（大小、修改时间等）
```

**预览编辑：**
```
请预览将 test_files/config.json 中的 "JSON" 替换为 "YAML" 的效果，不要实际修改文件
```

## 🛠️ 可用工具列表

| 工具名称 | 功能 | 示例用法 |
|---------|-----|----------|
| `read_file` | 读取文件内容 | "读取 README.md" |
| `write_file` | 写入文件 | "创建一个新的配置文件" |
| `edit_file` | 编辑文件 | "修改代码中的变量名" |
| `list_directory` | 列出目录 | "显示文件夹内容" |
| `create_directory` | 创建目录 | "创建新文件夹" |
| `search_files` | 搜索文件 | "查找所有 .txt 文件" |
| `get_file_info` | 文件信息 | "显示文件大小和修改时间" |
| `move_file` | 移动/重命名 | "重命名文件" |

## 💡 实际应用场景

### 1. 代码管理
```
请帮我查看项目中所有的 .js 文件，并列出它们的功能
```

### 2. 文档整理
```
请帮我整理文档文件夹，创建一个按类型分类的目录结构
```

### 3. 配置文件管理
```
请帮我修改配置文件，将数据库连接从 localhost 改为 production 服务器
```

### 4. 日志分析
```
请帮我读取日志文件，找出所有错误信息
```

## ⚠️ 注意事项

1. **路径限制**: 服务器只能访问配置中指定的目录
2. **文件权限**: 确保 Claude Desktop 有读写权限
3. **备份重要文件**: 使用编辑功能前建议备份
4. **预览模式**: 使用 `dryRun` 预览编辑效果

## 🔧 故障排除

### 常见问题：

1. **"Access denied"错误**
   - 检查文件路径是否在允许的目录中
   - 确认目录路径是否正确

2. **服务器无法启动**
   - 确认 Node.js 已安装
   - 检查编译后的文件是否存在

3. **文件操作失败**
   - 检查文件权限
   - 确认目录是否存在

### 测试服务器：
```bash
# 在 filesystem 目录中运行
node dist/index.js test_files
```

应该显示：
```
Secure MCP Filesystem Server running on stdio
Allowed directories: [ 'D:\\bowen\\MCP\\servers\\src\\filesystem\\test_files' ]
```

## 🎉 享受使用！

配置完成后，您现在可以让 Claude 帮您管理文件了！这是一个强大的工具，可以大大提高您的工作效率。 