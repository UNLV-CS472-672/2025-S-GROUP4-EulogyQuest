# ai-gen start (ChatGPT-4, 1)
import unittest
from unittest.mock import patch, call
import subprocess
import importlib.util
import os
import sys

file_path = os.path.abspath("Eulogy-Quest/GPT/create-quest.py")
spec = importlib.util.spec_from_file_location("create_quest", file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestCreateQuest(unittest.TestCase):
    def test_missing_arguments(self):
        with patch.object(sys, "argv", ["create-quest.py"]), \
             self.assertRaises(SystemExit) as cm, \
             patch("builtins.print") as mock_print:
            module.main()

        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Usage: python3 create-quest.py <honored_target> [zone]")

    def test_invalid_name_format(self):
        with patch.object(sys, "argv", ["create-quest.py", "OneName"]), \
             self.assertRaises(SystemExit) as cm, \
             patch("builtins.print") as mock_print:
            module.main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: honored_target must be two words (first and last name)")

    def test_invalid_zone(self):
        with patch.object(sys, "argv", ["create-quest.py", "Test User", "invalid_zone"]), \
             self.assertRaises(SystemExit) as cm, \
             patch("builtins.print") as mock_print:
            module.main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: zone must be 'tutorialb' or 'world-wide'")

    @patch("subprocess.run")
    @patch("builtins.print")
    def test_valid_execution_flow(self, mock_print, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)

        with patch.object(sys, "argv", ["create-quest.py", "Test User", "tutorialb"]):
            module.main()

        self.assertEqual(mock_run.call_count, 3)

        # Collect the actual bash command strings
        bash_commands = [call_args[0][0][2] for call_args in mock_run.call_args_list]

        script_dir = module.Path(module.__file__).parent.resolve()
        expected_commands = [
            f"source ../.venv/bin/activate && python3 {script_dir / 'base-story.py'} 'Test User'",
            f"source ../.venv/bin/activate && python3 {script_dir / 'updateNPCs.py'} 'User-quest'",
            f"source ../.venv/bin/activate && python3 {script_dir / 'perl-script-NPCs.py'} 'Test User' 'tutorialb'",
        ]

        for expected, actual in zip(expected_commands, bash_commands):
            self.assertEqual(expected, actual)

        mock_print.assert_any_call("Quest creation pipeline complete.")
# ai-gen end