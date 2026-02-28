#!/usr/bin/env python3
"""
Python 客户端示例 - 连接到 HTTP MCP Server

这个示例展示了如何使用 Python 标准库通过 HTTP 请求连接到 MCP 服务器。
不需要安装任何额外依赖。
"""

import json
import urllib.request
import urllib.error

def make_request(url, data, headers=None):
    """发送 JSON-RPC 请求到服务器"""
    if headers is None:
        headers = {}

    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json, text/event-stream'

    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=json_data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            response_headers = dict(response.headers)
            content_type = response_headers.get('Content-Type', '')

            # 读取响应内容
            response_text = response.read().decode('utf-8')

            # 处理 SSE 响应（检查内容是否以 "event:" 开头）
            if response_text.startswith('event:') or 'text/event-stream' in content_type:
                # 解析 SSE 格式: event: message\ndata: {...}\n\n
                lines = response_text.strip().split('\n')
                for line in lines:
                    if line.startswith('data: '):
                        json_data = line[6:]  # 去掉 "data: " 前缀
                        response_data = json.loads(json_data)
                        return response_data, response_headers
                # 如果没有找到 data 行，返回空响应
                return {}, response_headers
            else:
                # 处理 JSON 响应
                if response_text:
                    response_data = json.loads(response_text)
                    return response_data, response_headers
                else:
                    return {}, response_headers
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        raise
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        raise

def main():
    print("🧪 Testing HTTP MCP Server from Python...\n")

    server_url = "http://localhost:3000/mcp"
    headers = {}

    # 测试 1: 初始化连接
    print("📡 Connecting to server...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "python-test-client",
                "version": "1.0.0"
            }
        }
    }

    result, response_headers = make_request(server_url, init_request, headers)
    print("✅ Connected successfully!")
    server_info = result.get('result', {}).get('serverInfo', {})
    print(f"Server: {server_info.get('name')} v{server_info.get('version')}\n")

    # 获取会话 ID
    session_id = response_headers.get('mcp-session-id')
    if session_id:
        headers['mcp-session-id'] = session_id

    # 发送 initialized 通知
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    make_request(server_url, initialized_notification, headers)

    # 测试 2: 列出工具
    print("📋 Test 1: Listing available tools...")
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }

    result, _ = make_request(server_url, list_tools_request, headers)
    tools = result.get('result', {}).get('tools', [])
    print(f"Found {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    print()

    # 测试 3: 调用 echo 工具
    print("🔊 Test 2: Calling echo tool...")
    call_echo_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "echo",
            "arguments": {
                "text": "Hello from Python client!"
            }
        }
    }

    result, _ = make_request(server_url, call_echo_request, headers)
    echo_result = result.get('result', {})
    content = echo_result.get('content', [{}])[0]
    print(f"Echo result: {content.get('text')}\n")

    # 测试 4: 调用 add 工具
    print("➕ Test 3: Calling add tool...")
    call_add_request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "add",
            "arguments": {
                "a": 123,
                "b": 456
            }
        }
    }

    result, _ = make_request(server_url, call_add_request, headers)
    add_result = result.get('result', {})
    content = add_result.get('content', [{}])[0]
    print(f"Add result: {content.get('text')}\n")

    # 测试 5: 列出资源
    print("📚 Test 4: Listing available resources...")
    list_resources_request = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "resources/list",
        "params": {}
    }

    result, _ = make_request(server_url, list_resources_request, headers)
    resources = result.get('result', {}).get('resources', [])
    print(f"Found {len(resources)} resources:")
    for resource in resources:
        print(f"  - {resource['name']}: {resource['uri']}")
    print()

    # 测试 6: 读取资源
    print("📖 Test 5: Reading resource...")
    read_resource_request = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "resources/read",
        "params": {
            "uri": "doc://example"
        }
    }

    result, _ = make_request(server_url, read_resource_request, headers)
    resource_content = result.get('result', {})
    contents = resource_content.get('contents', [{}])[0]
    print(f"Resource content: {contents.get('text')}\n")

    print("✅ All tests passed!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
