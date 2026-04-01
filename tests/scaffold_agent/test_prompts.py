import unittest

from scaffold_agent.prompts import build_system_prompt
from scaffold_agent.templates import SUPPORTED_TEMPLATES


class TestPrompts(unittest.TestCase):
    def test_system_prompt_contains_template_catalog(self) -> None:
        prompt = build_system_prompt()
        self.assertIn("你是一个专业的项目脚手架 Agent", prompt)
        for template in SUPPORTED_TEMPLATES:
            self.assertIn(template.name, prompt)


if __name__ == "__main__":
    unittest.main()
