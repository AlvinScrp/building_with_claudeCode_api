import tempfile
import unittest
from pathlib import Path

from scaffold_agent.tools import ToolExecutor


class TestToolExecutor(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)
        self.executor = ToolExecutor(workspace=self.workspace, ask_user_fn=lambda _: "yes")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_write_read_list_glob(self) -> None:
        write_result = self.executor.execute(
            "write_file",
            {"path": "demo/main.py", "content": "status = 'ok'\n"},
        )
        self.assertTrue(write_result.success)

        read_result = self.executor.execute("read_file", {"path": "demo/main.py"})
        self.assertTrue(read_result.success)
        self.assertIn("status = 'ok'", read_result.output["content"])

        list_result = self.executor.execute("list_directory", {"path": "demo"})
        self.assertTrue(list_result.success)
        names = [entry["name"] for entry in list_result.output["entries"]]
        self.assertIn("main.py", names)

        glob_result = self.executor.execute("glob", {"pattern": "**/*.py"})
        self.assertTrue(glob_result.success)
        self.assertIn("demo/main.py", glob_result.output["matches"])

    def test_ask_user(self) -> None:
        result = self.executor.execute("ask_user", {"question": "继续吗？"})
        self.assertTrue(result.success)
        self.assertEqual(result.output["answer"], "yes")

    def test_bash(self) -> None:
        result = self.executor.execute("bash", {"command": "echo hello"})
        self.assertTrue(result.success)
        self.assertEqual(result.output["exit_code"], 0)
        self.assertIn("hello", result.output["stdout"])

    def test_block_workspace_escape(self) -> None:
        result = self.executor.execute(
            "write_file",
            {"path": "../outside.txt", "content": "x"},
        )
        self.assertFalse(result.success)
        self.assertIn("路径越界", result.error)


if __name__ == "__main__":
    unittest.main()
