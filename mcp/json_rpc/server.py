import sys
import json

# 供客户端调用的方法
def add(a, b):
    return a + b

methods = {"add": add}

# 循环监听标准输入
for line in sys.stdin:
    if not line.strip():
        continue
        
    try:
        # 1. 解析 JSON-RPC 请求
        req = json.loads(line)
        req_id = req.get("id")
        method_name = req.get("method")
        params = req.get("params", {})
        
        # 2. 路由并执行方法
        if method_name in methods:
            result = methods[method_name](**params)
            response = {"jsonrpc": "2.0", "result": result, "id": req_id}
        else:
            # 找不到方法的标准错误
            response = {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req_id}
            
    except Exception as e:
        # 解析异常或执行异常
        response = {"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}, "id": None}
    
    # 3. 返回响应 (必须加上换行符 \n，并立刻 flush 推送数据)
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()