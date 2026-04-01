from __future__ import annotations

import argparse
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(dotenv_path: str | Path | None = None, override: bool = False, *_args, **_kwargs) -> bool:
        path = Path(dotenv_path) if dotenv_path else Path(".env")
        if not path.exists():
            return False
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if not key:
                continue
            if not override and key in os.environ:
                continue
            os.environ[key] = value
        return True

from .agent import ScaffoldAgent
from .config import load_api_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="智能项目脚手架 Agent")
    parser.add_argument("request", nargs="?", help="用户需求，例如：创建一个带登录的 FastAPI 项目")
    parser.add_argument("--config", help="配置文件路径（.yaml/.yml/.json）")
    parser.add_argument("--workspace", default=".", help="项目生成根目录")
    parser.add_argument("--max-loops", type=int, default=20, help="最大 Agent 循环次数")
    parser.add_argument("--log-file", help="日志文件路径，默认写入 workspace/scaffold_agent.log")
    return parser.parse_args()


def _ask_user(question: str) -> str:
    return input(f"{question}\n> ").strip()


def _setup_logger(log_file: Path) -> logging.Logger:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("scaffold_agent")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.handlers.clear()

    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def main() -> int:
    load_dotenv()
    args = parse_args()
    workspace = Path(args.workspace)
    log_file = Path(args.log_file).expanduser() if args.log_file else workspace / "scaffold_agent.log"
    logger = _setup_logger(log_file.resolve())
    logger.info("Scaffold Agent 启动")

    request = args.request or input("请输入项目需求：\n> ").strip()
    if not request:
        logger.error("错误：请求不能为空")
        return 1

    try:
        config = load_api_config(args.config)
        logger.info(
            "配置加载成功: base_url=%s, model=%s, max_tokens=%s, temperature=%s",
            config.base_url,
            config.model,
            config.max_tokens,
            config.temperature,
        )
        agent = ScaffoldAgent(
            config=config,
            workspace=workspace,
            ask_user_fn=_ask_user,
            max_loops=args.max_loops,
        )
        result = agent.run(request)
    except Exception as exc:
        logger.exception("执行失败: %s", exc)
        print(f"执行失败: {exc}", file=sys.stderr)
        print(f"详细日志: {log_file.resolve()}", file=sys.stderr)
        return 1

    logger.info("Agent 输出:\n%s", result)
    logger.info("日志文件位置: %s", log_file.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
