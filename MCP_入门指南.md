# MCP (Model Context Protocol) 入门指南

## 🎯 什么是 MCP？

Model Context Protocol (MCP) 是一个开放标准，让 AI 助手能够安全地访问外部工具、数据和服务。简单来说，MCP 让 Claude 等 AI 助手能够"使用工具"。

## 🚀 快速开始 - Time 服务器

### 1. 环境准备

确保您已经安装：
- ✅ Claude Desktop
- ✅ 已下载的 MCP servers 仓库

### 2. 配置 Claude Desktop

#### Windows 用户：
1. 打开文件资源管理器
2. 在地址栏输入：`%APPDATA%\Claude`
3. 如果目录不存在，请创建它
4. 创建或编辑 `claude_desktop_config.json` 文件

#### 配置内容：
```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time"]
    }
  }
}
```

### 3. 重启 Claude Desktop

⚠️ **重要**：配置完成后，必须完全关闭并重新启动 Claude Desktop

### 4. 测试功能

重启后，在 Claude Desktop 中尝试：

**基础测试：**
- "现在北京时间是几点？"
- "纽约现在几点了？"

**进阶测试：**
- "帮我把北京时间上午9点转换成纽约时间"
- "告诉我现在伦敦、东京、悉尼的时间"

## 🛠️ 其他推荐的 MCP 服务器

### Memory 服务器 - 记忆功能
```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

### Filesystem 服务器 - 文件操作
```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/允许访问的目录路径"]
    }
  }
}
```

## 🔧 故障排除

### 常见问题：

1. **服务器无法启动**
   - 确保已安装 `uv` 和 `node.js`
   - 检查配置文件语法是否正确

2. **Claude 无法使用工具**
   - 确认已重启 Claude Desktop
   - 检查配置文件路径是否正确

3. **权限问题**
   - 确保 Claude Desktop 有网络访问权限
   - 检查防火墙设置

### 验证配置：
```bash
# 测试 Time 服务器是否可用
uvx mcp-server-time

# 测试 Memory 服务器是否可用
npx -y @modelcontextprotocol/server-memory
```

## 🌟 进阶使用

### 自定义配置
您可以添加环境变量和自定义参数：

```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time", "--local-timezone=Asia/Shanghai"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {
        "MEMORY_FILE_PATH": "D:/my-claude-memory.json"
      }
    }
  }
}
```

## 📚 下一步

1. 尝试更多 MCP 服务器
2. 查看 [MCP 官方文档](https://modelcontextprotocol.io)
3. 探索社区开发的 MCP 服务器
4. 考虑开发自己的 MCP 服务器

## 🎉 恭喜！

您已经成功配置了第一个 MCP 服务器！Claude 现在可以：
- 🕐 查询世界各地的时间
- 🌍 进行时区转换
- 📅 处理复杂的时间计算

享受您的 MCP 之旅！ 