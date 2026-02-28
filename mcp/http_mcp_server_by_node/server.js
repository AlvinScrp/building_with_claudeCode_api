import express from 'express';
import cors from 'cors';
import { randomUUID } from 'node:crypto';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import * as z from 'zod';

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Store active transports by session ID
const transports = new Map();

// Create MCP Server instance
const createServer = () => {
  const server = new McpServer({
    name: 'http-mcp-server',
    version: '1.0.0',
  });

  // Register echo tool
  server.registerTool(
    'echo',
    {
      description: 'Echoes back the input text',
      inputSchema: {
        text: z.string().describe('Text to echo back'),
      },
    },
    async ({ text }) => {
      return {
        content: [
          {
            type: 'text',
            text: `Echo: ${text}`,
          },
        ],
      };
    }
  );

  // Register add tool
  server.registerTool(
    'add',
    {
      description: 'Adds two numbers together',
      inputSchema: {
        a: z.number().describe('First number'),
        b: z.number().describe('Second number'),
      },
    },
    async ({ a, b }) => {
      const result = a + b;
      return {
        content: [
          {
            type: 'text',
            text: `Result: ${a} + ${b} = ${result}`,
          },
        ],
      };
    }
  );

  // Register example resource
  server.registerResource(
    'example-doc',
    'doc://example',
    {
      title: 'Example Document',
      description: 'A simple example document',
      mimeType: 'text/plain',
    },
    async () => {
      return {
        contents: [
          {
            uri: 'doc://example',
            mimeType: 'text/plain',
            text: 'This is an example document from the HTTP MCP Server.',
          },
        ],
      };
    }
  );

  return server;
};

// Handle all MCP requests via StreamableHTTP
app.all('/mcp', async (req, res) => {
  const sessionId = req.headers['mcp-session-id'];

  // Reuse existing transport or create new one
  let transport = sessionId ? transports.get(sessionId) : undefined;

  if (!transport) {
    transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: () => randomUUID(),
      onsessioninitialized: (id) => {
        console.log(`[${id}] Session initialized`);
        transports.set(id, transport);
      },
    });

    // Create a new server per session and connect it to the transport
    const server = createServer();
    await server.connect(transport);
  }

  await transport.handleRequest(req, res, req.body);
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    activeSessions: transports.size,
    timestamp: new Date().toISOString(),
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`\n🚀 HTTP MCP Server running on http://localhost:${PORT}`);
  console.log(`\nEndpoints:`);
  console.log(`  - ALL  /mcp      - MCP protocol endpoint (StreamableHTTP)`);
  console.log(`  - GET  /health   - Health check\n`);
  console.log(`Available tools: echo, add`);
  console.log(`Available resources: doc://example\n`);
});
