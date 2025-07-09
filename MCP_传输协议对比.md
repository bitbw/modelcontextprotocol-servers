# MCP 传输协议深度对比

## 🎯 答案：不是 HTTP 服务！

**Filesystem 服务器使用的是 Stdio 传输协议，不是 HTTP 服务。**

## 📡 三种 MCP 传输协议对比

### 1. Stdio 传输（Filesystem 服务器使用）

```typescript
// src/filesystem/index.ts
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

async function runServer() {
  const transport = new StdioServerTransport();  // ← 关键代码
  await server.connect(transport);
  console.error("Secure MCP Filesystem Server running on stdio");
}
```

**工作原理：**
- 通过标准输入/输出（stdin/stdout）通信
- Claude Desktop 启动子进程
- 使用进程管道传输 JSON-RPC 消息
- 无需网络端口

### 2. HTTP 传输（Everything 服务器支持）

```typescript
// src/everything/streamableHttp.ts (假设的代码结构)
import express from 'express';

const app = express();
app.listen(3000, () => {
  console.log('MCP server running on HTTP port 3000');
});
```

**工作原理：**
- 启动 HTTP 服务器（如端口 3000）
- Claude 通过 HTTP POST 请求调用工具
- 返回 HTTP Response

### 3. SSE 传输（Everything 服务器支持）

```typescript
// src/everything/sse.ts (假设的代码结构)
app.get('/sse', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  });
});
```

**工作原理：**
- Server-Sent Events 实时推送
- 保持长连接
- 支持服务器主动推送消息

## 📊 对比表格

| 特性 | Stdio 传输 | HTTP 传输 | SSE 传输 |
|------|------------|-----------|----------|
| **网络端口** | ❌ 无需端口 | ✅ 需要端口 | ✅ 需要端口 |
| **进程模型** | 子进程 | 独立服务 | 独立服务 |
| **通信方式** | 进程管道 | HTTP 请求 | 事件流 |
| **实时推送** | ❌ | ❌ | ✅ |
| **安全性** | 🔒 进程隔离 | 🔓 网络暴露 | 🔓 网络暴露 |
| **配置复杂度** | 简单 | 中等 | 复杂 |
| **调试难度** | 困难 | 容易 | 中等 |

## 🔍 实际通信演示

### Stdio 传输消息流

**Claude Desktop 配置：**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["dist/index.js", "test_files"]
    }
  }
}
```

**实际进程：**
```bash
# Claude Desktop 启动子进程
$ node dist/index.js test_files

# 通过 stdin 发送消息
{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {...}}

# 通过 stdout 接收响应
{"jsonrpc": "2.0", "id": 1, "result": {...}}
```

### HTTP 传输（如果是 HTTP 服务）

**假设的 HTTP 配置：**
```json
{
  "mcpServers": {
    "filesystem": {
      "url": "http://localhost:3000",
      "method": "http"
    }
  }
}
```

**HTTP 请求：**
```bash
# Claude 发送 HTTP 请求
POST http://localhost:3000/mcp/tools/call
Content-Type: application/json

{
  "name": "read_file",
  "arguments": {"path": "test_files/hello.txt"}
}

# 服务器 HTTP 响应
HTTP/1.1 200 OK
Content-Type: application/json

{
  "content": [{"type": "text", "text": "Hello World"}]
}
```

## 🎯 为什么 Filesystem 使用 Stdio？

### 优势：
1. **安全性更高** - 无网络暴露
2. **配置简单** - 无需管理端口
3. **进程隔离** - 自动生命周期管理
4. **无依赖** - 不需要额外的网络库

### 劣势：
1. **调试困难** - 无法直接测试
2. **单一客户端** - 只能被启动它的进程使用

## 🔧 验证传输协议

### 检查 Filesystem 服务器：
```bash
# 运行服务器看输出
$ node dist/index.js test_files
Secure MCP Filesystem Server running on stdio  # ← 明确说明 stdio
Allowed directories: [ '...' ]

# 没有监听端口信息
```

### 检查 Everything 服务器（HTTP 模式）：
```bash
$ npm run start:streamableHttp
MCP server running on HTTP port 3000  # ← 会显示端口信息
```

## 💡 总结

**Filesystem 服务器：**
- ✅ 使用 Stdio 传输协议
- ❌ 不是 HTTP 服务
- 🔒 通过进程管道通信
- 📁 专注于安全的文件操作

**Everything 服务器：**
- ✅ 支持多种传输协议
- 🌐 可以运行 HTTP 服务
- 🧪 用于测试不同的 MCP 功能

这就是为什么您在配置中使用 `"command": "node"` 而不是 `"url": "http://..."`！ 