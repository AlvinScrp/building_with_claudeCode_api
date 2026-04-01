from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class TemplateInfo:
    name: str
    stack: str
    structure: str


SUPPORTED_TEMPLATES: tuple[TemplateInfo, ...] = (
    TemplateInfo("fastapi_api", "FastAPI + Uvicorn", "app/, app/models/, app/routers/"),
    TemplateInfo("flask_web", "Flask + Jinja2", "app/, templates/, static/"),
    TemplateInfo("python_cli", "Typer / Click", "cli/, commands/, tests/"),
    TemplateInfo("python_package", "setuptools", "src/, tests/, pyproject.toml"),
    TemplateInfo("express_api", "Express.js", "routes/, controllers/, models/"),
    TemplateInfo("react_vite", "React + Vite", "src/components/, src/pages/"),
    TemplateInfo("vue2_app", "Vue 2 + Vue CLI", "src/components/, src/views/, src/router/"),
    TemplateInfo("vue3_app", "Vue 3 + Vite", "src/components/, src/views/, src/composables/"),
    TemplateInfo("vue3_ts_app", "Vue 3 + Vite + TS", "src/components/, src/views/, src/types/"),
)


def render_template_catalog(templates: Iterable[TemplateInfo] = SUPPORTED_TEMPLATES) -> str:
    lines = ["支持的模板列表："]
    for item in templates:
        lines.append(f"- {item.name}: {item.stack} | 结构: {item.structure}")
    return "\n".join(lines)
