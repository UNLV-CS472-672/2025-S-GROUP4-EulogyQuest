import os
import sys
import logging
import importlib.util
from pathlib import Path
import pytest

repo_root   = Path(__file__).parent.parent
gpt_dir     = repo_root / "Eulogy-Quest" / "GPT"
module_path = gpt_dir / "base-story.py"

if not module_path.is_file():
    raise FileNotFoundError(f"Cannot find base-story.py at {module_path}")

spec = importlib.util.spec_from_file_location("base_story", module_path)
base_story = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base_story)

def test_parse_args_valid(monkeypatch):
    """parse_args should return an object with the honored_target attribute."""
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    monkeypatch.setattr(sys, "argv", ["prog", "Jane Smith"])
    args = base_story.parse_args()
    assert hasattr(args, "honored_target")
    assert args.honored_target == "Jane Smith"


def test_parse_args_missing(monkeypatch):
    """parse_args with no honored_target should exit with an error."""
    monkeypatch.setattr(sys, "argv", ["prog"])
    with pytest.raises(SystemExit) as exc:
        base_story.parse_args()
    assert exc.value.code == 2


def test_setup_logging_adds_handler_and_info_level():
    """setup_logging should configure root logger at INFO level with at least one handler."""
    # Remove any existing handlers
    for h in logging.root.handlers[:]:
        logging.root.removeHandler(h)

    base_story.setup_logging()

    assert logging.root.level == logging.INFO
    assert len(logging.root.handlers) >= 1


def test_main_missing_api_key(monkeypatch, caplog):
    """If OPENAI_API_KEY isn’t set, main() should log an error and return None."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    caplog.set_level(logging.ERROR)
    result = base_story.main()
    assert result is None
    assert "OPENAI_API_KEY not set" in caplog.text


@pytest.mark.parametrize("honored", [
    "Single",
    "Too Many Names",
])
def test_main_invalid_honored_target(monkeypatch, caplog, honored):
    """
    honored_target must be exactly two words;
    otherwise main() logs an error and returns None.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")
    caplog.set_level(logging.ERROR)
    monkeypatch.setattr(sys, "argv", ["prog", honored])

    result = base_story.main()
    assert result is None
    assert "honored_target must be two words" in caplog.text


class DummyResponse:
    def __init__(self, content):
        choice = type("Choice", (), {
            "message": type("Msg", (), {"content": content})
        })()
        self.choices = [choice]


class DummyClient:
    def __init__(self, api_key=None):
        self.chat = self
        self.completions = self

    def create(self, *, model, messages, temperature):
        return DummyResponse("\n".join([
            "ghost_task.txt",
            "`Do this task`",
            "",
            "ghost_delivery_item.txt",
            "`Magic Sword`",
            "",
            "ghost_delivery_target.txt",
            "`Sir Lancelot`",
            "",
            "ghost_delivery_target_location.txt",
            "`Camelot`",
        ]))


def test_main_catches_api_exceptions(monkeypatch, caplog, tmp_path):
    class BadClient:
        def __init__(self, api_key=None): pass
        def create(self, **kwargs):
            raise RuntimeError("API failure")
    monkeypatch.setenv("OPENAI_API_KEY", "x")
    monkeypatch.setattr(base_story, "load_dotenv", lambda: None)
    monkeypatch.setattr(base_story, "OpenAI", BadClient)
    fake_gpt = tmp_path / "Eulogy-Quest" / "GPT"
    fake_gpt.mkdir(parents=True)
    monkeypatch.setattr(base_story, "__file__", str(fake_gpt / "base-story.py"))
    monkeypatch.chdir(tmp_path)
    caplog.set_level(logging.ERROR)
    monkeypatch.setattr(sys, "argv", ["prog", "Alice Doe"])
    result = base_story.main()
    assert result is None
    assert "ChatCompletion API error" in caplog.text


def test_main_generates_and_cleans_files(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(base_story, "load_dotenv", lambda: None)
    monkeypatch.setattr(base_story, "OpenAI", DummyClient)
    fake_gpt = tmp_path / "Eulogy-Quest" / "GPT"
    fake_gpt.mkdir(parents=True)
    monkeypatch.setattr(base_story, "__file__", str(fake_gpt / "base-story.py"))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "Jane Doe"])
    assert base_story.main() is None
    last_name = "Doe"
    build_dir = fake_gpt / "Eulogies" / f"{last_name}-quest" / "build" / "quest"
    assert build_dir.is_dir()
    expected = {
        "ghost_task.txt",
        "ghost_delivery_item.txt",
        "ghost_delivery_target.txt",
        "ghost_delivery_target_location.txt",
        "npc1_target.txt",
        "honored_target.txt",
    }
    found = {p.name for p in build_dir.glob("*.txt")}
    assert found == expected

    def read_lines(fname):
        return [
            line for line in
            (build_dir / fname).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    assert read_lines("ghost_task.txt") == ["Do this task"]
    assert read_lines("ghost_delivery_item.txt") == ["Magic Sword"]
    assert read_lines("ghost_delivery_target.txt") == ["Sir Lancelot"]
    assert read_lines("ghost_delivery_target_location.txt") == ["Camelot"]
    assert read_lines("npc1_target.txt") == ["Sir Lancelot"]
    assert read_lines("honored_target.txt") == ["Jane Doe"]
