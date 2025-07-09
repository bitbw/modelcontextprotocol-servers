# MCP Filesystem 服务器源码深度分析

## 🎯 总体架构

当您运行 `node D:/bowen/MCP/servers/src/filesystem/dist/index.js test_files` 时，发生了以下过程：

## 📋 第1阶段：启动和初始化

### 1.1 命令行参数解析
```typescript
// 从命令行获取允许访问的目录
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error("Usage: mcp-server-filesystem <allowed-directory> [additional-directories...]");
  process.exit(1);
}
```

**您的命令：** `node dist/index.js test_files`
- `args[0]` = `"test_files"`
- 这就是为什么服务器只能访问 `test_files` 目录

### 1.2 安全目录验证
```typescript
// 标准化并解析所有允许的目录
const allowedDirectories = await Promise.all(
  args.map(async (dir) => {
    const expanded = expandHome(dir);
    const absolute = path.resolve(expanded);
    try {
      const resolved = await fs.realpath(absolute);
      return normalizePath(resolved);
    } catch (error) {
      return normalizePath(absolute);
    }
  })
);
```

**实际效果：**
- 将 `test_files` 转换为绝对路径
- 解析符号链接
- 验证目录存在性

### 1.3 创建 MCP 服务器实例
```typescript
const server = new Server(
  {
    name: "secure-filesystem-server",
    version: "0.2.0",
  },
  {
    capabilities: {
      tools: {},
    },
  },
);
```

## 📋 第2阶段：工具注册

### 2.1 工具列表注册
```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "read_file",
        description: "Read the complete contents of a file...",
        inputSchema: zodToJsonSchema(ReadFileArgsSchema) as ToolInput,
      },
      {
        name: "write_file",
        description: "Create a new file or overwrite...",
        inputSchema: zodToJsonSchema(WriteFileArgsSchema) as ToolInput,
      },
      // ... 其他 10 个工具
    ],
  };
});
```

**这里就是关键！** 当 Claude 问"你能做什么？"时，服务器回答提供了 12 个工具：
1. `read_file` - 读取文件
2. `write_file` - 写入文件
3. `edit_file` - 编辑文件
4. `create_directory` - 创建目录
5. `list_directory` - 列出目录
6. `move_file` - 移动文件
7. `search_files` - 搜索文件
8. `get_file_info` - 获取文件信息
9. ... 等等

### 2.2 工具调用处理
```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  switch (name) {
    case "read_file": {
      const parsed = ReadFileArgsSchema.safeParse(args);
      const validPath = await validatePath(parsed.data.path);
      const content = await fs.readFile(validPath, "utf-8");
      return {
        content: [{ type: "text", text: content }],
      };
    }
    // ... 其他工具的处理
  }
});
```

## 📋 第3阶段：通信建立

### 3.1 Stdio 传输协议
```typescript
async function runServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Secure MCP Filesystem Server running on stdio");
  console.error("Allowed directories:", allowedDirectories);
}
```

**关键点：** 使用 `stdio` 传输协议，这意味着：
- 服务器通过标准输入/输出与 Claude 通信
- JSON-RPC 格式的消息
- 双向通信管道

## 🔒 安全机制详解

### 路径验证核心函数
```typescript
async function validatePath(requestedPath: string): Promise<string> {
  const expandedPath = expandHome(requestedPath);
  const absolute = path.isAbsolute(expandedPath)
    ? path.resolve(expandedPath)
    : path.resolve(process.cwd(), expandedPath);

  const normalizedRequested = normalizePath(absolute);

  // 检查路径是否在允许的目录中
  const isAllowed = isPathWithinAllowedDirectories(normalizedRequested, allowedDirectories);
  if (!isAllowed) {
    throw new Error(`Access denied - path outside allowed directories`);
  }

  return realPath;
}
```

**安全保护：**
- ✅ 防止路径遍历攻击（`../../../etc/passwd`）
- ✅ 只允许访问指定目录
- ✅ 符号链接检查
- ✅ 路径规范化

## 🔄 实际交互流程

### 当您问："请读取 test_files/hello.txt"

1. **Claude 分析**：识别这是文件操作请求
2. **工具选择**：选择 `read_file` 工具
3. **参数构造**：`{"path": "test_files/hello.txt"}`
4. **发送请求**：通过 stdio 发送 JSON-RPC 请求
5. **服务器处理**：
   ```typescript
   case "read_file": {
     const parsed = ReadFileArgsSchema.safeParse(args);  // 验证参数
     const validPath = await validatePath("test_files/hello.txt");  // 安全检查
     const content = await fs.readFile(validPath, "utf-8");  // 读取文件
     return { content: [{ type: "text", text: content }] };  // 返回结果
   }
   ```
6. **返回结果**：`"Hello World"`

### 消息格式示例

**Claude 发送给服务器：**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "test_files/hello.txt"
    }
  }
}
```

**服务器回复给 Claude：**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Hello World"
      }
    ]
  }
}
```

## 💡 为什么 Claude 能执行文件操作？

### 关键原理：
1. **协议标准化**：MCP 定义了统一的工具调用协议
2. **能力声明**：服务器主动告诉 Claude 它能做什么
3. **类型安全**：使用 Zod 进行参数验证
4. **双向通信**：实时的请求-响应机制

### 与传统 API 的区别：
```typescript
// 传统 API：Claude 需要硬编码功能
function readFile(path: string) {
  // 功能固定在 Claude 代码中
}

// MCP 方式：动态发现功能
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: [...] };  // 服务器告诉 Claude 它能做什么
});
```

## 🚀 优势总结

1. **插件化架构**：无需修改 Claude 代码即可添加新功能
2. **安全沙盒**：严格的路径验证和访问控制
3. **类型安全**：完整的参数验证和错误处理
4. **标准化协议**：统一的工具调用接口
5. **实时通信**：高效的双向数据传输

## 🔍 深入理解

MCP 的革命性在于：
- **服务器主动声明能力** - "我能做什么"
- **Claude 动态调用工具** - "我需要使用这个功能"
- **标准化的通信协议** - 任何人都可以开发 MCP 服务器

这就是为什么您只需要修改配置文件，就能让 Claude 获得新的能力！ 