from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional


@dataclass(slots=True)
class ToolExecutionResult:
    success: bool
    output: Any = None
    error: Optional[str] = None

    def to_model_content(self) -> str:
        payload = {"success": self.success, "output": self.output}
        if self.error:
            payload["error"] = self.error
        return json.dumps(payload, ensure_ascii=False)


class ToolExecutor:
    def __init__(
        self,
        workspace: Path | str,
        ask_user_fn: Optional[Callable[[str], str]] = None,
        command_timeout: int = 120,
    ) -> None:
        self.workspace = Path(workspace).expanduser().resolve()
        self.ask_user_fn = ask_user_fn or self._default_ask_user
        self.command_timeout = command_timeout

    @staticmethod
    def schemas() -> list[dict[str, Any]]:
        return [
            {
                "name": "bash",
                "description": "执行 shell 命令。用于创建目录、初始化 git、安装依赖等。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "要执行的 shell 命令"}
                    },
                    "required": ["command"],
                },
            },
            {
                "name": "write_file",
                "description": "创建或覆盖文件。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "文件路径"},
                        "content": {"type": "string", "description": "文件内容"},
                    },
                    "required": ["path", "content"],
                },
            },
            {
                "name": "read_file",
                "description": "读取文件内容。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "文件路径"}
                    },
                    "required": ["path"],
                },
            },
            {
                "name": "list_directory",
                "description": "列出目录中的文件和子目录。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "目录路径"}
                    },
                    "required": ["path"],
                },
            },
            {
                "name": "ask_user",
                "description": "向用户提问以获取更多信息。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "description": "要问用户的问题"}
                    },
                    "required": ["question"],
                },
            },
            {
                "name": "glob",
                "description": "根据模式匹配文件路径。",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string", "description": "glob 模式，如 **/*.py"}
                    },
                    "required": ["pattern"],
                },
            },
        ]

    def execute(self, tool_name: str, tool_input: dict[str, Any]) -> ToolExecutionResult:
        handler = {
            "bash": self._tool_bash,
            "write_file": self._tool_write_file,
            "read_file": self._tool_read_file,
            "list_directory": self._tool_list_directory,
            "ask_user": self._tool_ask_user,
            "glob": self._tool_glob,
        }.get(tool_name)

        if handler is None:
            return ToolExecutionResult(False, error=f"未知工具: {tool_name}")

        try:
            return handler(tool_input)
        except Exception as exc:
            return ToolExecutionResult(False, error=str(exc))

    def execute_for_model(self, tool_name: str, tool_input: dict[str, Any]) -> str:
        return self.execute(tool_name, tool_input).to_model_content()

    def _resolve_path(self, raw_path: str) -> Path:
        candidate = Path(raw_path).expanduser()
        path = candidate if candidate.is_absolute() else self.workspace / candidate
        resolved = path.resolve()
        if resolved != self.workspace and self.workspace not in resolved.parents:
            raise ValueError(f"路径越界: {raw_path}")
        return resolved

    def _tool_bash(self, tool_input: dict[str, Any]) -> ToolExecutionResult:
        command = str(tool_input.get("command", "")).strip()
        if not command:
            raise ValueError("command 不能为空")

        completed = subprocess.run(
            command,
            shell=True,
            cwd=self.workspace,
            text=True,
            capture_output=True,
            timeout=self.command_timeout,
        )
        output = {
            "command": command,
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
        return ToolExecutionResult(completed.returncode == 0, output=output)

    def _tool_write_file(self, tool_input: dict[str, Any]) -> ToolExecutionResult:
        path = self._resolve_path(str(tool_input.get("path", "")).strip())
        content = str(tool_input.get("content", ""))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return ToolExecutionResult(True, output={"path": str(path), "bytes": len(content.encode("utf-8"))})

    def _tool_read_file(self, tool_input: dict[str, Any]) -> ToolExecutionResult:
        path = self._resolve_path(str(tool_input.get("path", "")).strip())
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        return ToolExecutionResult(True, output={"path": str(path), "content": path.read_text(encoding="utf-8")})

    def _tool_list_directory(self, tool_input: dict[str, Any]) -> ToolExecutionResult:
        path = self._resolve_path(str(tool_input.get("path", ".")).strip() or ".")
        if not path.exists():
            raise FileNotFoundError(f"目录不存在: {path}")
        if not path.is_dir():
            raise NotADirectoryError(f"不是目录: {path}")

        entries = []
        for item in sorted(path.iterdir(), key=lambda value: (value.is_file(), value.name.lower())):
            entries.append(
                {
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "path": str(item.relative_to(self.workspace)),
                }
            )
        return ToolExecutionResult(True, output={"path": str(path), "entries": entries})

    def _tool_ask_user(self, tool_input: dict[str, Any]) -> ToolExecutionResult:
        question = str(tool_input.get("question", "")).strip()
        if not question:
            raise ValueError("question 不能为空")
        answer = self.ask_user_fn(question)
        return ToolExecutionResult(True, output={"question": question, "answer": answer})

    def _tool_glob(self, tool_input: dict[str, Any]) -> ToolExecutionResult:
        pattern = str(tool_input.get("pattern", "")).strip()
        if not pattern:
            raise ValueError("pattern 不能为空")

        root_pattern = str((self.workspace / pattern).resolve()) if not Path(pattern).is_absolute() else pattern
        matches = []
        for path in self.workspace.glob(pattern):
            resolved = path.resolve()
            if resolved == self.workspace or self.workspace in resolved.parents:
                matches.append(str(resolved.relative_to(self.workspace)))
        matches.sort()
        return ToolExecutionResult(True, output={"pattern": pattern, "matches": matches, "expanded_pattern": root_pattern})

    @staticmethod
    def _default_ask_user(question: str) -> str:
        return input(f"{question}\n> ").strip()
