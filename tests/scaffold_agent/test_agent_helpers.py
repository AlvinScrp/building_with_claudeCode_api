import unittest

from scaffold_agent.agent import ScaffoldAgent


class BlockLike:
    def __init__(self) -> None:
        self.type = "text"
        self.text = "hello"


class TestAgentHelpers(unittest.TestCase):
    def test_normalize_block_dict(self) -> None:
        block = {"type": "text", "text": "ok"}
        normalized = ScaffoldAgent._normalize_block(block)
        self.assertEqual(normalized["type"], "text")
        self.assertEqual(normalized["text"], "ok")

    def test_normalize_block_object(self) -> None:
        block = BlockLike()
        normalized = ScaffoldAgent._normalize_block(block)
        self.assertEqual(normalized["type"], "text")
        self.assertEqual(normalized["text"], "hello")

    def test_collect_text(self) -> None:
        blocks = [
            {"type": "text", "text": "第一行"},
            {"type": "tool_use", "name": "bash", "input": {"command": "ls"}},
            {"type": "text", "text": "第二行"},
        ]
        text = ScaffoldAgent._collect_text(blocks)
        self.assertEqual(text, "第一行\n第二行")


if __name__ == "__main__":
    unittest.main()
