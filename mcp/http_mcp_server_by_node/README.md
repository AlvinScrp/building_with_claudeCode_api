# HTTP MCP Server

基于 Node.js 的 MCP (Model Context Protocol) 服务器，用于本地测试。

## 快速开始

### 1. 安装依赖
```bash
npm install
```

### 2. 启动服务器
```bash
npm start
```

服务器将在 http://localhost:3000 启动。

### 3. 测试

**Node.js 客户端：**
```bash
node test_client.js
```

**Python 客户端：**
```bash
python3 test_client.py
```

**健康检查：**
```bash
curl http://localhost:3000/health
```

## API 端点

- `GET /health` - 健康检查
- `ALL /mcp` - MCP 协议端点（StreamableHTTP）

## 可用工具

### echo
回显输入的文本。

**参数：**
- `text` (string): 要回显的文本

**示例：**
```javascript
{
  name: 'echo',
  arguments: { text: 'Hello World' }
}
```

### add
将两个数字相加。

**参数：**
- `a` (number): 第一个数字
- `b` (number): 第二个数字

**示例：**
```javascript
{
  name: 'add',
  arguments: { a: 10, b: 20 }
}
```

## 可用资源

### doc://example
示例文档资源。

**URI**: `doc://example`
**MIME Type**: `text/plain`

## 扩展开发

### 添加新工具

```javascript
server.registerTool(
  'tool-name',
  {
    description: '工具描述',
    inputSchema: {
      param: z.string().describe('参数描述'),
    },
  },
  async ({ param }) => {
    return {
      content: [{ type: 'text', text: '结果' }],
    };
  }
);
```

### 添加新资源

```javascript
server.registerResource(
  'resource-name',
  'resource://uri',
  {
    title: '资源标题',
    description: '资源描述',
    mimeType: 'text/plain',
  },
  async () => {
    return {
      contents: [{
        uri: 'resource://uri',
        mimeType: 'text/plain',
        text: '资源内容',
      }],
    };
  }
);
```

## 技术栈

- Node.js 20+
- Express 4.21.2
- MCP SDK 1.12.1
- Zod 3.x

## 许可证

MIT
