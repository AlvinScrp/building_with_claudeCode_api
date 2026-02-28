import subprocess
import json

def main():
    # 1. 启动子进程，通过 PIPE 接管 stdin 和 stdout
    # text=True 会自动将字节流处理为字符串
    process = subprocess.Popen(
        ["python", "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True 
    )

    # 2. 构造标准的 JSON-RPC 2.0 请求
    request = {
        "jsonrpc": "2.0",
        "method": "add",
        "params": {"a": 10, "b": 20},
        "id": 1 # 客户端生成的唯一 ID
    }

    # 3. 发送请求 (追加换行符，并 flush 确保数据发往子进程)
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()

    # 4. 阻塞并读取服务端返回的一行响应
    response_line = process.stdout.readline()
    
    # 5. 解析响应
    response = json.loads(response_line)
    print(f"服务端返回完整数据: {response}")
    print(f"计算结果: {response.get('result')}")

    # 清理资源退出
    process.stdin.close()
    process.terminate()

if __name__ == "__main__":
    main()