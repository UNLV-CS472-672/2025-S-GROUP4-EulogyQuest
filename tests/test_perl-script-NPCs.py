# ai-gen start (ChatGPT-4, 0)
import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
from pathlib import Path

# Importing the module dynamically to allow patching __file__ later
import importlib.util
import os

file_path = os.path.abspath("Eulogy-Quest/GPT/perl-script-NPCs.py")
spec = importlib.util.spec_from_file_location("perl_script_NPCs", file_path)
perl_script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(perl_script)


class TestPerlScriptNPCs(unittest.TestCase):

    # Tests executing perl-script-NPCs without any additional arguments
    # When mock-running main, it expects and asserts that the usage message will be printed
    def test_no_arguments(self):
        test_args = ["perl-script-NPCs.py"]
        with patch.object(sys, 'argv', test_args), patch("builtins.print") as mock_print:
            perl_script.main()      # Simulates running perl-script-NPCs
            mock_print.assert_any_call("Usage: python3 perl-script-NPCs.py <honored_target>")

    # Tests running perl-script-NPCs while providing only the first name of the honored target
    # When mock-running main, it expects the error message for not having a string that splits into 2 parts
    def test_single_word_argument(self):
        test_args = ["perl-script-NPCs.py", "OnlyFirst"]
        with patch.object(sys, 'argv', test_args), patch("builtins.print") as mock_print:
            perl_script.main()
            mock_print.assert_any_call("Error: honored_target must consist of two words (first and last name)")

    # Tests perl-script-NPCs.py when the honored_target.txt file is not found
    # Expects an error message
    def test_missing_honored_target_file(self):
        test_args = ["perl-script-NPCs.py", "John Doe"]
        
        with patch.object(sys, 'argv', test_args), \
             patch("pathlib.Path.exists", return_value=False), \
             patch("builtins.print") as mock_print:
            perl_script.main()
            
            # These 2 lines of code allows us to check if the error message is printed
            # without dealing with the path variable in the formatted string
            calls = [args[0][0] for args in mock_print.call_args_list]
            self.assertTrue(any("Error: Could not find honored_target.txt" in call for call in calls))

    # Tests file when ghost_task.txt is not found
    # Expects an error message
    def test_missing_ghost_task_file(self):
        test_args = ["perl-script-NPCs.py", "John Doe"]

        def side_effect(path_obj):
            # Simulate honored_target.txt exists, ghost_task.txt does not
            if "honored_target.txt" in str(path_obj):
                return True
            if "ghost_task.txt" in str(path_obj):
                return False
            return True

        with patch.object(sys, 'argv', test_args), \
             patch("pathlib.Path.exists", side_effect=side_effect, autospec=True), \
             patch("pathlib.Path.read_text", return_value="John Doe"), \
             patch("builtins.print") as mock_print:
            perl_script.main()
            calls = [args[0][0] for args in mock_print.call_args_list]
            self.assertTrue(any("Error: Could not find ghost_task.txt" in call for call in calls))

    # Tests remainder of the file:
    # Reads text from a mock, valid npc text file and adds npc names to the list variable
    # Reads text from a mock, quest text file
    # Mocks making directory
    # Tests iterating through the npc names list for existing files
    # Mocks writing the file and copying it
    @patch("sys.argv", ["perl-script-NPCs.py", "Jane Smith"])
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.read_text", side_effect=["Jane Smith", "default quest text", "Custom NPC text"])
    @patch("pathlib.Path.write_text")
    @patch("shutil.copy")
    @patch("pathlib.Path.glob")
    @patch("builtins.print")
    def test_script_full_unit_flow(self, mock_print, mock_glob, mock_copy, mock_write, mock_read, mock_mkdir):
        with patch("pathlib.Path.exists") as mock_exists, patch("pathlib.Path.read_text") as mock_read_text:
            npc_file_mock = MagicMock()
            npc_file_mock.read_text.return_value = "NPC One"
            mock_glob.return_value = [npc_file_mock]
            perl_script.main()

        # Ensure all major steps were attempted
        mock_mkdir.assert_called()
        self.assertTrue(mock_write.called)
        self.assertTrue(mock_copy.called)
        self.assertTrue(any("Generated:" in str(call) for call in mock_print.call_args_list))
# ai-gen end
