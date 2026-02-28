import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';

const SERVER_URL = 'http://localhost:3000/mcp';

async function testMcpServer() {
  console.log('🧪 Testing MCP Server...\n');

  // Create client
  const client = new Client(
    {
      name: 'test-client',
      version: '1.0.0',
    },
    {
      capabilities: {},
    }
  );

  // Create transport
  const transport = new StreamableHTTPClientTransport(new URL(SERVER_URL));

  try {
    // Connect to server
    console.log('📡 Connecting to server...');
    await client.connect(transport);
    console.log('✅ Connected successfully!\n');

    // Test 1: List available tools
    console.log('📋 Test 1: Listing available tools...');
    const toolsResult = await client.listTools();
    console.log('Available tools:', JSON.stringify(toolsResult.tools, null, 2));
    console.log('');

    // Test 2: Call echo tool
    console.log('🔊 Test 2: Calling echo tool...');
    const echoResult = await client.callTool({
      name: 'echo',
      arguments: { text: 'Hello from test client!' },
    });
    console.log('Echo result:', JSON.stringify(echoResult, null, 2));
    console.log('');

    // Test 3: Call add tool
    console.log('➕ Test 3: Calling add tool...');
    const addResult = await client.callTool({
      name: 'add',
      arguments: { a: 42, b: 58 },
    });
    console.log('Add result:', JSON.stringify(addResult, null, 2));
    console.log('');

    // Test 4: List available resources
    console.log('📚 Test 4: Listing available resources...');
    const resourcesResult = await client.listResources();
    console.log('Available resources:', JSON.stringify(resourcesResult.resources, null, 2));
    console.log('');

    // Test 5: Read a resource
    console.log('📖 Test 5: Reading resource...');
    const readResult = await client.readResource({
      uri: 'doc://example',
    });
    console.log('Resource content:', JSON.stringify(readResult, null, 2));
    console.log('');

    console.log('✅ All tests passed!\n');

    // Close connection
    await client.close();
    console.log('👋 Connection closed');

  } catch (error) {
    console.error('❌ Error:', error.message);
    console.error(error);
    process.exit(1);
  }
}

// Run tests
testMcpServer();
