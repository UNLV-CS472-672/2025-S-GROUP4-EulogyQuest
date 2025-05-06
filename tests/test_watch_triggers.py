# ai-gen start (ChatGPT-4, 1)
import unittest
from unittest.mock import patch, MagicMock
import importlib.util
import os
import sys

file_path = os.path.abspath("Eulogy-Quest/GPT/watch_triggers.py")
spec = importlib.util.spec_from_file_location("watch_triggers", file_path)
watch_triggers = importlib.util.module_from_spec(spec)
sys.modules["watch_triggers"] = watch_triggers
spec.loader.exec_module(watch_triggers)

class TestWatchTriggers(unittest.TestCase):
    def test_extract_name(self):
        self.assertEqual(
            watch_triggers.extract_name("path/to/Eulogyquest_John_Doe.trigger"),
            "John Doe"
        )

    @patch("watch_triggers.subprocess.run")
    def test_run_quest_script_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Success!"
        result = watch_triggers.run_quest_script("John Doe")
        self.assertTrue(result)

    @patch("watch_triggers.subprocess.run")
    def test_run_quest_script_failure(self, mock_run):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Error occurred"
        result = watch_triggers.run_quest_script("John Doe")
        self.assertFalse(result)

    @patch("watch_triggers.os.remove")
    def test_cleanup_trigger_success(self, mock_remove):
        watch_triggers.cleanup_trigger("/fake/path.trigger")
        mock_remove.assert_called_with("/fake/path.trigger")

    @patch("watch_triggers.os.remove", side_effect=OSError("File not found"))
    def test_cleanup_trigger_failure(self, mock_remove):
        watch_triggers.cleanup_trigger("/fake/path.trigger")
        mock_remove.assert_called_with("/fake/path.trigger")

    def test_trigger_handler_enqueue(self):
        mock_queue = MagicMock()
        handler = watch_triggers.TriggerHandler(mock_queue)
        handler.enqueue("/fake/path/Eulogyquest_John_Doe.trigger")
        mock_queue.put_nowait.assert_called_with("/fake/path/Eulogyquest_John_Doe.trigger")
# ai-gen end