import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scaffold_agent.agent import ScaffoldAgent
from scaffold_agent.config import APIConfig


class FakeMessagesAPI:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(deepcopy(kwargs))
        if not self._responses:
            raise RuntimeError("No more fake responses")
        return self._responses.pop(0)


class FakeClient:
    def __init__(self, responses):
        self.messages = FakeMessagesAPI(responses)


class FakeStreamManager:
    def __init__(self, response):
        self._response = response

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        return None

    def get_final_message(self):
        return self._response


class StreamingRequiredMessagesAPI:
    def __init__(self, stream_response):
        self.stream_response = stream_response
        self.create_calls = []
        self.stream_calls = []

    def create(self, **kwargs):
        self.create_calls.append(deepcopy(kwargs))
        raise ValueError(
            "Streaming is required for operations that may take longer than 10 minutes. "
            "See docs for more details"
        )

    def stream(self, **kwargs):
        self.stream_calls.append(deepcopy(kwargs))
        return FakeStreamManager(self.stream_response)


class TestScaffoldAgentRunWithMock(unittest.TestCase):
    def setUp(self) -> None:
        self.config = APIConfig(api_key="test-key", model="claude-test-model")

    def test_run_with_tool_use_and_text_response(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            responses = [
                SimpleNamespace(
                    content=[
                        {
                            "type": "tool_use",
                            "id": "tool_1",
                            "name": "write_file",
                            "input": {"path": "demo/main.py", "content": "value = 'mock'\n"},
                        }
                    ]
                ),
                SimpleNamespace(content=[{"type": "text", "text": "项目脚手架创建完成"}]),
            ]
            fake_client = FakeClient(responses)

            with patch("scaffold_agent.agent.create_client", return_value=fake_client):
                agent = ScaffoldAgent(config=self.config, workspace=workspace)
                result = agent.run("创建一个 Python 项目")

            self.assertEqual(result, "项目脚手架创建完成")
            self.assertTrue((workspace / "demo/main.py").exists())
            self.assertIn("value = 'mock'", (workspace / "demo/main.py").read_text(encoding="utf-8"))

            self.assertEqual(len(fake_client.messages.calls), 2)
            second_call_messages = fake_client.messages.calls[1]["messages"]
            tool_result_block = second_call_messages[-1]["content"][0]
            self.assertEqual(tool_result_block["type"], "tool_result")
            parsed = json.loads(tool_result_block["content"])
            self.assertTrue(parsed["success"])

    def test_run_with_direct_text(self) -> None:
        fake_client = FakeClient([SimpleNamespace(content=[{"type": "text", "text": "无需工具调用"}])])
        with patch("scaffold_agent.agent.create_client", return_value=fake_client):
            agent = ScaffoldAgent(config=self.config, workspace=".")
            result = agent.run("给我一个建议")
        self.assertEqual(result, "无需工具调用")

    def test_run_hit_max_loops(self) -> None:
        fake_client = FakeClient(
            [
                SimpleNamespace(
                    content=[
                        {
                            "type": "tool_use",
                            "id": "tool_1",
                            "name": "list_directory",
                            "input": {"path": "."},
                        }
                    ]
                )
            ]
        )
        with patch("scaffold_agent.agent.create_client", return_value=fake_client):
            agent = ScaffoldAgent(config=self.config, workspace=".", max_loops=1)
            result = agent.run("检查目录")
        self.assertIn("达到最大循环次数", result)

    def test_run_falls_back_to_stream_when_required(self) -> None:
        stream_response = SimpleNamespace(content=[{"type": "text", "text": "通过流式返回"}])
        messages_api = StreamingRequiredMessagesAPI(stream_response=stream_response)
        fake_client = SimpleNamespace(messages=messages_api)

        with patch("scaffold_agent.agent.create_client", return_value=fake_client):
            agent = ScaffoldAgent(config=self.config, workspace=".")
            result = agent.run("生成项目")

        self.assertEqual(result, "通过流式返回")
        self.assertEqual(len(messages_api.create_calls), 1)
        self.assertEqual(len(messages_api.stream_calls), 1)


if __name__ == "__main__":
    unittest.main()
