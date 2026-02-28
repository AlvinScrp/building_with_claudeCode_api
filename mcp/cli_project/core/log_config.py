"""统一日志配置：所有 core 模块写入同一日志文件。"""
import logging
import os

_LOG_PATH = os.environ.get("MCP_CLI_LOG", "mcp_cli.log")
_ROOT_LOGGER_NAME = "mcp_cli"

_configured = False


def setup_logging() -> None:
    """配置根 logger，使所有 getLogger(__name__) 的日志写入同一文件。"""
    global _configured
    if _configured:
        return
    root = logging.getLogger(_ROOT_LOGGER_NAME)
    root.setLevel(logging.DEBUG)
    if not root.handlers:
        handler = logging.FileHandler(_LOG_PATH, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
        )
        root.addHandler(handler)
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """返回子 logger，日志会 propagate 到 mcp_cli 的 handler。"""
    setup_logging()
    return logging.getLogger(f"{_ROOT_LOGGER_NAME}.{name}")
