import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scaffold_agent.config import APIConfig, create_client, load_api_config


class TestAPIConfig(unittest.TestCase):
    def test_from_env(self) -> None:
        with patch.dict(
            os.environ,
            {
                "ANTHROPIC_API_KEY": "test-key",
                "ANTHROPIC_BASE_URL": "https://proxy.example.com",
                "ANTHROPIC_MODEL": "claude-test-model",
                "ANTHROPIC_MAX_TOKENS": "2048",
                "ANTHROPIC_TEMPERATURE": "0.5",
            },
            clear=False,
        ):
            config = APIConfig.from_env()

        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(config.base_url, "https://proxy.example.com")
        self.assertEqual(config.model, "claude-test-model")
        self.assertEqual(config.max_tokens, 2048)
        self.assertEqual(config.temperature, 0.5)

    def test_from_file_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "api": {
                            "key": "json-key",
                            "base_url": "https://json.example.com",
                            "model": "claude-json-model",
                        },
                        "settings": {"max_tokens": 1024, "temperature": 0.1},
                    }
                ),
                encoding="utf-8",
            )
            config = APIConfig.from_file(config_path)

        self.assertEqual(config.api_key, "json-key")
        self.assertEqual(config.base_url, "https://json.example.com")
        self.assertEqual(config.model, "claude-json-model")
        self.assertEqual(config.max_tokens, 1024)
        self.assertEqual(config.temperature, 0.1)

    def test_load_api_config_from_env(self) -> None:
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "env-key"}, clear=False):
            config = load_api_config()
        self.assertEqual(config.api_key, "env-key")

    def test_create_client_missing_anthropic_dependency(self) -> None:
        config = APIConfig(api_key="test-key")
        with patch("scaffold_agent.config.importlib.import_module", side_effect=ModuleNotFoundError):
            with self.assertRaisesRegex(RuntimeError, "缺少依赖 anthropic"):
                create_client(config)

    def test_create_client_success(self) -> None:
        class FakeAnthropicClient:
            def __init__(self, *, api_key: str, base_url: str) -> None:
                self.api_key = api_key
                self.base_url = base_url

        class FakeAnthropicModule:
            Anthropic = FakeAnthropicClient

        config = APIConfig(api_key="test-key", base_url="https://proxy.example.com")
        with patch("scaffold_agent.config.importlib.import_module", return_value=FakeAnthropicModule()):
            client = create_client(config)

        self.assertEqual(client.api_key, "test-key")
        self.assertEqual(client.base_url, "https://proxy.example.com")


if __name__ == "__main__":
    unittest.main()
