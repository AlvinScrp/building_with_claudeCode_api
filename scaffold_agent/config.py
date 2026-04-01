from __future__ import annotations

import importlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    import anthropic


@dataclass(slots=True)
class APIConfig:
    api_key: str
    base_url: str = "https://api.anthropic.com"
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    temperature: float = 0.2

    @classmethod
    def from_env(cls) -> "APIConfig":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY 环境变量未设置")

        max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "4096"))
        temperature = float(os.getenv("ANTHROPIC_TEMPERATURE", "0.2"))
        return cls(
            api_key=api_key,
            base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
            max_tokens=max_tokens,
            temperature=temperature,
        )

    @classmethod
    def from_file(cls, path: str | Path) -> "APIConfig":
        file_path = Path(path).expanduser()
        if not file_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {file_path}")

        suffix = file_path.suffix.lower()
        if suffix in {".yaml", ".yml"}:
            try:
                import yaml
            except ImportError as exc:
                raise RuntimeError("读取 YAML 配置需要安装 PyYAML") from exc
            config_data: dict[str, Any] = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
        elif suffix == ".json":
            config_data = json.loads(file_path.read_text(encoding="utf-8"))
        else:
            raise ValueError("仅支持 .yaml/.yml/.json 配置文件")

        api_config = config_data.get("api", {})
        settings = config_data.get("settings", {})
        api_key = api_config.get("key") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("配置文件和环境变量中都未提供 API Key")

        return cls(
            api_key=api_key,
            base_url=api_config.get("base_url", os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")),
            model=api_config.get("model", os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")),
            max_tokens=int(settings.get("max_tokens", os.getenv("ANTHROPIC_MAX_TOKENS", "4096"))),
            temperature=float(settings.get("temperature", os.getenv("ANTHROPIC_TEMPERATURE", "0.2"))),
        )


def load_api_config(path: Optional[str] = None) -> APIConfig:
    if path:
        return APIConfig.from_file(path)
    return APIConfig.from_env()


def create_client(config: Optional[APIConfig] = None) -> "anthropic.Anthropic":
    if config is None:
        config = APIConfig.from_env()
    try:
        anthropic_module = importlib.import_module("anthropic")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "缺少依赖 anthropic。请先执行 `pip install anthropic` 或 `pip install -r requirements.txt`。"
        ) from exc
    return anthropic_module.Anthropic(api_key=config.api_key, base_url=config.base_url)
