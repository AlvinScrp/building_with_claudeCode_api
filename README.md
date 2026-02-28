# Anthropic API 调用示例

这是一个使用 Anthropic API 调用 Claude Sonnet 4.0 模型的简单示例项目。

## 安装步骤

1. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置 API 密钥和自定义 URL（可选）**
   
   创建 `.env` 文件，并添加你的 Anthropic API 密钥：
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
   
   如果需要使用自定义的 API 端点（例如通过代理服务器），可以添加：
   ```
   ANTHROPIC_BASE_URL=https://your-custom-endpoint.com
   ```
   
   你可以从 [Anthropic Console](https://console.anthropic.com/) 获取 API 密钥。

3. **运行示例**
   ```bash
   python main.py
   ```

## 代码说明

- `main.py`: 包含基本的 API 调用示例
- `requirements.txt`: 项目依赖包列表
- `.env`: 环境变量文件（需要自己创建，包含 API 密钥）

## 注意事项

- 请确保 `.env` 文件已添加到 `.gitignore` 中，不要将 API 密钥提交到版本控制系统
- API 密钥需要从 Anthropic Console 获取
